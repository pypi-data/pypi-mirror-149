'''
Basic chemical objects

Matter
├── Substance
│   ├── Element
│   └── Compound
└── Mixture
'''

import re
from copy import deepcopy
import numpy as np
from scipy.constants import physical_constants
from scipy.constants import N_A
from scipy.constants import calorie
from scipy.constants import kilo
from scipy.constants import R
from scipy.constants import atm

__all__ = [
    'Thermochemistry',
    'Structure',
    'Substance',
    'Mixture'
]

standard_temperature = 298.15

si_energy_factor = {
    'E_h': physical_constants['Hartree energy'][0],
    'eV': physical_constants['electron volt'][0],
    'J': 1,
    'kJ': kilo,
    'J/mol': 1 / N_A,
    'kJ/mol': kilo / N_A,
    'cal': calorie,
    'cal/mol': calorie / N_A,
    'kcal': kilo * calorie,
    'kcal/mol': kilo * calorie / N_A
}


def convert_energy(value, old_unit, new_unit):
    if np.isnan(value):
        return np.nan
    else:
        return value * si_energy_factor[old_unit] / si_energy_factor[new_unit]


class Thermochemistry:
    def __init__(self):
        self.zero_point_energy = 0
        self.thermal_correction_to_enthalpy = 0
        self.thermal_correction_to_gibbs_energy = 0
        self.entropy = 0
        self.temperature = 0


scf_pattern = re.compile(r'SCF Done:\s+E\(\w+\)\s*=\s*([-+]?[0-9]+\.[0-9]+)')
gibbs_pattern = re.compile(r'Thermal correction to Gibbs Free Energy='
                            r'\s*([-+]?[0-9]+\.[0-9]+)')
entalpy_pattern = re.compile(r'Thermal correction to Enthalpy='
                            r'\s*([-+]?[0-9]+\.[0-9]+)')
temp_pattern = re.compile(r'Temperature\s+([0-9]+\.[0-9]+)')
state_pattern = re.compile(r'Charge\s*=\s*([-+]?[0-9]+)\s+Multiplicity\s*=\s*([0-9]+)')


def struct_from_gaussian_log(spc_log_files, freq_log_files):
    struct = Structure()
    for model, file in spc_log_files.items():
        with open(file, 'r') as stream:
            content = stream.read()
            try:
                energy = float(scf_pattern.findall(content)[-1])
                energy = convert_energy(energy, 'E_h', 'kcal/mol')
                struct.energy[model] = energy
            except IndexError:
                return None

    for model, file in freq_log_files.items():
        with open(file, 'r') as stream:
            content = stream.read()
            try:
                thermo = Thermochemistry()
                thermo.temperature = float(temp_pattern.findall(content)[-1])
                # Gibbs energy
                correction = float(gibbs_pattern.findall(content)[-1])
                # Standard state correction
                correction += 0.00302
                correction = convert_energy(correction, 'E_h', 'kcal/mol')
                thermo.thermal_correction_to_gibbs_energy = correction
                # Enthalpy
                correction = float(entalpy_pattern.findall(content)[-1])
                correction = convert_energy(correction, 'E_h', 'kcal/mol')
                thermo.thermal_correction_to_enthalpy = correction
                # Entropy
                thermo.entropy = (thermo.thermal_correction_to_enthalpy - thermo.thermal_correction_to_gibbs_energy) / thermo.temperature
                struct.thermochemistry[model] = thermo
                # Set electronic state
                charge, multiplicity = map(int, state_pattern.findall(content)[-1])
                struct.total_charge = charge
                struct.total_spin = (multiplicity - 1) / 2
            except IndexError:
                return None
    return struct


class Structure:
    '''Chemical structure object
    '''
    def __init__(self):
        self.sign = +1
        self.total_spin = 0
        self.total_charge = 0
        self.energy = {}
        self.thermochemistry = {}

    def get_gibbs_energy(self, scf_model, thermo_model):
        output = self.energy[scf_model]
        output += (self.thermochemistry[thermo_model].
                   thermal_correction_to_gibbs_energy)
        return self.sign * output

    def get_energy(self, scf_model):
        output = self.energy[scf_model]
        return self.sign * output

    def get_enthalpy(self, scf_model, thermo_model):
        output = self.energy[scf_model]
        output += (self.thermochemistry[thermo_model].
                   thermal_correction_to_enthalpy)
        return self.sign * output

    def get_entropy(self, thermo_model):
        output = self.thermochemistry[thermo_model].entropy
        return self.sign * output
    
    def get_models(self):
        output = []
        for scf_model in self.energy:
            for thermo_model in self.thermochemistry:
                yield (scf_model, thermo_model)

    def __add__(self, other):
        if isinstance(other, Mixture):
            return other.__add__(self)
        else:
            return Mixture(self, other)
    
    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __neg__(self):
        output = deepcopy(self)
        output.sign *= -1
        return output


class Mixture:
    '''Chemical mixture object
    '''
    def __init__(self, *substances):
        self.substances = list(substances)

    def get_gibbs_energy(self, scf_model, thermo_model):
        output = 0
        for substance in self:
            output += substance.get_gibbs_energy(scf_model, thermo_model)
        return output

    def get_enthalpy(self, scf_model, thermo_model):
        output = 0
        for substance in self:
            output += substance.get_enthalpy(scf_model, thermo_model)
        return output

    def get_entropy(self, thermo_model):
        output = 0
        for substance in self:
            output += substance.get_entropy(thermo_model)
        return output

    def get_energy(self, scf_model):
        output = 0
        for substance in self:
            output += substance.get_energy(scf_model)
        return output

    def get_models(self):
        return self.substances[0].get_models()

    def __iter__(self):
        return iter(self.substances)

    def __add__(self, other):
        output = deepcopy(self)
        output.__iadd__(other)
        return output

    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self.substances += other.substances
        else:
            self.substances.append(other)
        return self
        
    def __sub__(self, other):
        return self.__add__(other.__neg__())
    
    def __neg__(self):
        output = deepcopy(self)
        output.substances = [s.__neg__() for s in self.substances]
        return output


class Substance:
    '''Pure chemical substance object
    '''
    def __init__(self):
        self.atoms = []
        self.conformers = []


