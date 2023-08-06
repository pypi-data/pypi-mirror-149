#!/usr/bin/env python3
#
#  constants.py
"""
Scientific constants.
"""
#
#  Copyright (c) 2019-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Dict, NamedTuple, Optional

# 3rd party
import quantities  # type: ignore

__all__ = [
		"Constant",
		"avogadro_number",
		"plancks_constant",
		"speed_of_light",
		"electron_radius",
		"neutron_mass",
		"atomic_mass_constant",
		"faraday_constant",
		"vacuum_permittivity",
		"boltzmann_constant",
		"molar_gas_constant",
		"prefixes",
		]


_anions = {  # Incomplete
		"F-": "fluoride",
		"Cl-": "chloride",
		"Br-": "bromide",
		"I-": "iodide",
		"OH-": "hydroxide",
		"CN-": "cyanide",
		"SCN-": "thiocyanate",
		"CO3-2": "carbonate",
		"C2O4-2": "oxalate",
		"HCO3-": "hydrogencarbonate",
		"NO3-": "nitrate",
		"NO2-": "nitrite",
		"PO4-3": "phospahte",
		"HPO4-2": "hydrogenphospahte",
		"H2PO4-": "dihydrogenphospahte",
		"P-3": "phosphide",
		"SO4-2": "sulphate",
		"HSO4-": "hydrogensulphate",
		"SO3-2": "sulphite",
		"HSO3-": "hydrogensulphite",
		"S-2": "sulfide",
		"ClO-": "hypochlorite",
		"ClO2-": "chlorite",
		"ClO3-": "chlorate",
		"ClO4-": "perchlorate",
		"CrO4-2": "chromate(VI)",
		"Cr2O7-2": "dichromate(VI)",
		"MnO4-2": "manganate(VI)",
		"MnO4-": "permanganate(VII)",
		"FeO4-2": "ferrate(VI)",
		"OsO4-2": "osmate(VI)",
		"Bo3-3": "borate",
		"BiO3-": "bismuthate(V)",
		}

_cations = {  # Incomplete
		"H3O+": "hydronium",
		}

_cation_oxidation_states = {  # This needs to be reviewed, just from the top of my head
		"Cr": (2, 3),
		"Fe": (2, 3),
		"Mn": (2,),
		"Co": (2, 3),
		"Ni": (2, 3),
		"Cu": (1, 2, 3),
		"Ag": (1, 2),
		"Au": (3,),
		"Zn": (2,),
		"Cd": (2,),
		"Hg": (1, 2),  # Tricky: Hg2+2
		"Al": (3,),
		"Ga": (3,),
		"In": (3,),
		"Tl": (1, 3),
		"Sn": (2, 4),
		"Pb": (2, 4),
		"Bi": (3,),
		"Sb": (3,),
		}


class Constant(NamedTuple):
	"""
	Represents a scientific constant.
	"""

	#: The name of the constant.
	name: str

	#: The value of the constant.
	value: float

	#: The constant's unit.
	unit: quantities.quantity.Quantity

	#: An optional symbol for the constant. Default :py:obj:`None`.
	symbol: Optional[str] = None

	def as_quantity(self) -> quantities.quantity.Quantity:
		"""
		Returns the constant as a :class:`quantities.quantity.Quantity` object.
		"""

		return self.value * self.unit

	def __float__(self) -> float:
		"""
		Returns the constant as a float (without the unit).
		"""

		return float(self.value)

	def __int__(self) -> int:
		"""
		Returns the constant as an integer (without the unit).
		"""

		return int(self.value)


# The following from periodictable
# Public Domain data
# Author: Paul Kienzle

#: Avogadro's constant (Avogadro's number)
avogadro_number = avogadro_constant = Constant(
		name="Avogadro constant", value=6.02214179e23, unit=1 / quantities.mol, symbol="N<sub>A</sub>"
		)  # (30)

#: Planck's constant
plancks_constant = planck_constant = Constant(
		name="Planck's constant",
		value=4.13566733e-15 * (10**34),
		unit=quantities.electron_volt / quantities.second,
		symbol='h'
		)  # (10)

#: The speed of light in a vacuum.
speed_of_light = Constant(
		name="Speed of light", value=299792458, unit=quantities.m / quantities.second, symbol='c'
		)  # (exact)

#: Electron Radius
electron_radius = Constant(name="Electron radius", value=2.8179402894e-15, unit=quantities.m, symbol="rₑ")  # (58)

# From NIST Reference on Constants, Units, and Uncertainty
#   http://physics.nist.gov/cuu/index.html
# neutron mass = 1.008 664 915 97(43) u
# atomic mass constant m_u = 1.660 538 782(83) x 10-27 kg

#: Neutron mass
neutron_mass = Constant(
		name="Neutron mass", value=1.00866491597, unit=quantities.atomic_mass_unit, symbol="n<sup>o</sup>"
		)  # (43)

#: The atomic mass constant.
atomic_mass_constant = float(quantities.atomic_mass_unit.rescale(quantities.kg))

#: Faraday constant
faraday_constant = Constant(
		name="Faraday constant",
		value=96485.3321233100184,
		unit=quantities.coulomb * (1 / quantities.mol),
		symbol='F'
		)

#: Vacuum permittivity
vacuum_permittivity = Constant(
		"Vacuum permittivity", value=8.8541878128e-12, unit=quantities.farad / quantities.metre, symbol="ε₀"
		)

#: Boltzmann constant
boltzmann_constant = Constant(
		name="Boltzmann constant",
		value=1.380649e-23,
		unit=quantities.joule / quantities.kelvin,
		symbol="k<sub>B</sub>"
		)

#: Molar gas constant
molar_gas_constant = Constant(
		name="Molar gas constant",
		value=8.31446261815324,
		unit=quantities.joule / quantities.kelvin / quantities.mol,
		symbol='R'
		)

#: Numerical IUPAC prefixes (e.g. **mono-**).
prefixes: Dict[int, str] = {
		1: "mono",
		2: "di",
		3: "tri",
		4: "tetra",
		5: "penta",
		6: "hexa",
		7: "hepta",
		8: "octa",
		9: "nona",
		10: "deca",
		11: "undeca",
		12: "dodeca",
		13: "trideca",
		14: "tetradeca",
		15: "pentadeca",
		16: "hexadeca",
		17: "heptadeca",
		18: "octadeca",
		19: "nonadeca",
		20: "icosa",
		21: "henicosa",
		22: "docosa",
		23: "tricosa",
		30: "triaconta",
		31: "hentriaconta",
		32: "dotriaconta",
		40: "tetraconta",
		50: "pentaconta",
		60: "hexaconta",
		70: "heptaconta",
		80: "octaconta",
		90: "nonaconta",
		100: "hecta",
		200: "dicta",
		300: "tricta",
		400: "tetracta",
		500: "pentacta",
		600: "hexacta",
		700: "heptacta",
		800: "octacta",
		900: "nonacta",
		1000: "kilia",
		2000: "dilia",
		3000: "trilia",
		4000: "tetralia",
		5000: "pentalia",
		6000: "hexalia",
		7000: "heptalia",
		8000: "octalia",
		9000: "nonalia",
		}
