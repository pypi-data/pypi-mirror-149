import inspect
import sys

from weaveio.hierarchy import Optional, Multiple, Hierarchy
from weaveio.opr3.hierarchy import Spectrum, Single, FibreTarget, Stack, \
    OBStack, OB, ArmConfig, Superstack, OBSpec, Supertarget, WeaveTarget, RawSpectrum, _predicate, Spectrum1D, MeanFlux, WavelengthHolder


class L1(Hierarchy):
    is_template = True


class L1Spectrum(Spectrum1D, L1):
    is_template = True
    children = [Optional('self', idname='adjunct')]
    parents = [WavelengthHolder]
    products = ['flux', 'ivar', 'sensfunc']
    factors = Spectrum.factors + ['nspec', 'snr'] + MeanFlux.as_factors('g', 'r', 'i', 'gg', 'bp', 'rp')


class NoSS(Spectrum1D):
    plural_name = 'nosses'
    singular_name = 'noss'
    products = ['flux', 'ivar']
    parents = [L1Spectrum]
    children = [Optional('self', idname='adjunct')]


class L1SingleSpectrum(L1Spectrum, Single):
    """
    A single spectrum row processed from a raw spectrum, belonging to one fibretarget and one run.
    """
    singular_name = 'l1single_spectrum'
    plural_name = 'l1single_spectra'
    parents = L1Spectrum.parents + [RawSpectrum, FibreTarget]
    version_on = ['raw_spectrum', 'fibre_target']
    factors = L1Spectrum.factors + [
        'rms_arc1', 'rms_arc2', 'resol', 'helio_cor',
        'wave_cor1', 'wave_corrms1', 'wave_cor2', 'wave_corrms2',
        'skyline_off1', 'skyline_rms1', 'skyline_off2', 'skyline_rms2',
        'sky_shift', 'sky_scale']


class L1StackSpectrum(L1Spectrum, Stack):
    is_template = True
    singular_name = 'l1stack_spectrum'
    plural_name = 'l1stack_spectra'


class L1OBStackSpectrum(L1StackSpectrum, OBStack):
    """
    A stacked spectrum row processed from > 1 single spectrum, belonging to one fibretarget but many runs within the same OB.
    """
    singular_name = 'l1obstack_spectrum'
    plural_name = 'l1obstack_spectra'
    parents = L1StackSpectrum.parents + [Multiple(L1SingleSpectrum, 2, constrain=(OB, FibreTarget, ArmConfig))]
    version_on = ['l1single_spectra']


class L1SuperstackSpectrum(L1StackSpectrum, Superstack):
    """
    A stacked spectrum row processed from > 1 single spectrum, belonging to one fibretarget but many runs within the same OBSpec.
    """
    singular_name = 'l1superstack_spectrum'
    plural_name = 'l1superstack_spectra'
    parents = L1StackSpectrum.parents + [Multiple(L1SingleSpectrum, 2, constrain=(OBSpec, FibreTarget, ArmConfig))]
    # version_on = ['l1single_spectra', 'fibre_target']


class L1SupertargetSpectrum(L1Spectrum, Supertarget):
    """
    A stacked spectrum row processed from > 1 single spectrum, belonging to one weavetarget over many different OBSpecs.
    """
    singular_name = 'l1supertarget_spectrum'
    plural_name = 'l1supertarget_spectra'
    parents = L1Spectrum.parents + [Multiple(L1SingleSpectrum, 2, constrain=(WeaveTarget, ArmConfig))]
    # version_on = ['l1single_spectra', 'weave_target']


hierarchies = [i[-1] for i in inspect.getmembers(sys.modules[__name__], _predicate)]