import logging
import time
from contextlib import contextmanager
from typing import Tuple, List, Dict, Any, Union, TYPE_CHECKING

from .parser import QueryGraph
from .results import Table
from .utilities import safe_name

if TYPE_CHECKING:
    from .objects import ObjectQuery, Query, AttributeQuery
    from ..data import Data


class AmbiguousPathError(Exception):
    pass


class CardinalityError(Exception):
    pass


@contextmanager
def logtime(name):
    start = time.perf_counter()
    yield
    logging.info(f"{name} took {time.perf_counter() - start: .3f} seconds")


class BaseQuery:
    one_row = False
    one_column = False

    def __repr__(self):
        return f'<{self.__class__.__name__}({self._previous._obj}-{self._obj})>'

    def _precompile(self) -> 'BaseQuery':
        return self

    def _to_cypher(self) -> Tuple[List[str], Dict[str, Any]]:
        """
        returns the cypher lines, cypher parameters, names of columns, expect_one_row, expect_one_column
        """
        return self._G.cypher_lines(self._node), self._G.parameters

    def _compile(self) -> Tuple[List[str], Dict[str, Any]]:
        with logtime('compiling'):
            return self._precompile()._to_cypher()

    def _execute(self, skip=0, limit=None):
        with logtime('executing'):
            lines, params = self._compile()
            if skip > 0:
                lines.append(f"SKIP {skip}")
            if limit is not None:
                lines.append(f"LIMIT {limit}")
            return self._data.graph.execute('\n'.join(lines), **{k.replace('$', ''): v for k,v in params.items()})

    def _iterate(self, skip=0, limit=None):
        yield from self._post_process_row(self._data.rowparser.iterate_cursor(self._execute(skip, limit), list(map(safe_name, self._names)), self._is_products))

    def __iter__(self):
        yield from self._iterate()

    def _to_table(self, skip=0, limit=None) -> Table:
        with logtime('total streaming'):
            cursor = self._execute(skip, limit)
            return self._data.rowparser.parse_to_table(cursor, list(map(safe_name, self._names)), self._is_products)

    def _post_process_table(self, result):
        if self.one_column:
            return result[result.colnames[0]].data
        return result

    def _post_process_row(self, row):
        if self.one_column:
            return row[row.colnames[0]]
        return row

    def __call__(self, skip=0, limit=None, **kwargs):
        return self._post_process_table(self._to_table(skip, limit))


    def __init__(self, data: 'Data', G: QueryGraph = None, node=None, previous: Union['Query', 'AttributeQuery', 'ObjectQuery'] = None,
                 obj: str = None, start: 'Query' = None, index_node = None,
                 single=False, names=None, is_products=None, attrs=None, dtype=None, *args, **kwargs) -> None:
        from .objects import ObjectQuery
        self._single = single
        self._data = data
        if G is None:
            self._G = QueryGraph()
        else:
            self._G = G
        if node is None:
            self._node = self._G.start
        else:
            self._node = node
        self._previous = previous
        self.__cypher = None
        self._index_node = index_node
        self._obj = obj
        if previous is not None:
            if self._index_node is None:
                if isinstance(previous, ObjectQuery):
                    self._index_node = previous._node
                elif self._index_node != 'start':
                    self._index_node = previous._index_node
            if obj is None:
                self._obj = previous._obj
        if start is None:
            self._start = self
        else:
            self._start = start
        if self._obj is not None:
            self._obj = self._normalise_object(self._obj)[0]
        self._names = [] if names is None else names
        self._is_products = [False]*len(self._names) if is_products is None else is_products
        self.attrs = attrs
        self.dtype = dtype

    def _get_object_of(self, maybe_attribute: str) -> Tuple[str, bool, bool]:
        """
        Given a str that might refer to an attribute, return the object that contains that attribute
        and also whether the attribute and the object are singular
        inferred obj | attr
            s        |  s      (i.e. run.obid -> run.ob.obid)
            p        |  p      (i.e. ...-> run.l1specs.snrs) - cannot be inferred just from a name
            s        |  p      (i.e. run.obids -> run.ob.obids)
            p        |  s      (i.e. run.snr -> run.l1spec.snr) - is not allowed
         :return: obj, obj_is_singular, attr_is_singular
        """
        single_name = self._data.singular_name(maybe_attribute)
        hs = {h.__name__ for h in self._data.factor_hierarchies[single_name]}
        if self._obj in hs:
            return self._obj, True, self._data.is_singular_name(maybe_attribute)
        if len(hs) > 1:
            raise AmbiguousPathError(f"There are multiple attributes called {maybe_attribute} with the following parent objects: {hs}."
                                     f" Please be specific e.g. `{hs.pop()}.{maybe_attribute}`")
        obj = hs.pop()
        if self._obj is None:
            return obj, True, False
        if not self._data.is_factor_name(maybe_attribute):
            raise ValueError(f"{maybe_attribute} is not a valid attribute name")
        path, obj_is_singular = self._data.path_to_hierarchy(self._obj, obj, False)
        attr_is_singular = self._data.is_singular_name(maybe_attribute)
        if obj_is_singular and attr_is_singular:
            pass  # run.obid -> run.ob.obid
        elif not obj_is_singular and not attr_is_singular:
            pass
        elif obj_is_singular and not attr_is_singular:
            pass  # run.obids -> run.ob.obids
        else:
            # ob.runid -> Error
            plural_name = self._data.plural_name(obj)
            original = self._data.singular_name(self._obj)
            raise CardinalityError(f"Requested one `{single_name}` from `{original}` "
                                   f"when `{original}` has several `{plural_name}`")
        return obj, obj_is_singular, attr_is_singular

    def _normalise_object(self, obj: str):
        """
        returns the __name__ of the respective class of the obj and whether it is plural/singular.
        If not a class, raise KeyError
        """
        if obj in self._data.class_hierarchies:
            return obj, True
        singular = self._data.singular_name(obj)
        if singular not in self._data.singular_hierarchies:
            raise KeyError(f"{obj} is not a valid object name")
        try:
            h = self._data.plural_hierarchies[obj.lower()]
            singular = False
        except KeyError:
            h = self._data.singular_hierarchies[obj.lower()]
            singular = True
        return h.__name__, singular

    @property
    def _cypher(self):
        if self.__cypher is None:
            self.__cypher = self._G.cypher_lines(self._node)
        return self.__cypher

    @property
    def _result_graph(self):
        return self._G.restricted(self._node)

    def _plot_graph(self, fname):
        return self._G.export(fname, self._node)

    @classmethod
    def _spawn(cls, parent: 'BaseQuery', node, obj=None, index_node=None, single=False, *args, **kwargs):
        return cls(parent._data, parent._G, node, parent, obj, parent._start, index_node, single, *args, **kwargs)

    def _get_path_to_object(self, obj, want_single) -> Tuple[str, bool]:
        return self._data.path_to_hierarchy(self._obj, obj, want_single)

    def _slice(self, slc):
        """
        obj[slice]
        filter, shrinks, destructive
        filter by using HEAD/TAIL/SKIP/LIMIT
        e.g. obs.runs[:10] will return the first 10 runs for each ob (in whatever order they were in)
        you must use query(skip, limit) to request a specific number of rows in total since this is unrelated to the actual query
        """
        raise NotImplementedError

    def _filter_by_mask(self, mask):
        """
        obj[boolean_filter]
        filter, shrinks, destructive
        filters based on a list of True/False values constructed beforehand, parentage of the booleans must be derived from the obj
        e.g. `ob.l1stackedspectra[ob.l1stackedspectra.camera == 'red']` gives only the red stacks
             `ob.l1stackedspectra[ob.l1singlespectra == 'red']` is invalid since the lists will not be the same size or have the same parentage
        """
        try:
            n = self._G.add_filter(self._node, mask._node, direct=False)
        except SyntaxError:
            raise SyntaxError(f"SyntaxError: {self} cannot be filtered by {mask} since there is no direct path between them")
        return self.__class__._spawn(self, n, single=self._single)

    def _aggregate(self, wrt, string_op, predicate=False, expected_dtype=None, returns_dtype=None, remove_infs=None):
        if wrt is None:
            wrt = self._start
        try:
            if predicate:
                n = self._G.add_predicate_aggregation(self._node, wrt._node, string_op)
            else:
                n = self._G.add_aggregation(self._node, wrt._node, string_op, remove_infs, expected_dtype, self.dtype)
        except SyntaxError:
            raise SyntaxError(f"Cannot aggregate {self} into {wrt} since they don't share a parent query")
        from .objects import AttributeQuery
        return AttributeQuery._spawn(self, n, wrt._obj, wrt._node, dtype=returns_dtype, single=True)
