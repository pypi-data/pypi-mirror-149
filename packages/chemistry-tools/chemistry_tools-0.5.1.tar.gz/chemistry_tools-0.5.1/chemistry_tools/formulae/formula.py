#!/usr/bin/env python3
#
#  formula.py
"""
Parse formulae into a Python object.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Also based on Pyteomics (https://github.com/levitsky/pyteomics)
#  |  Copyright (c) 2011-2015, Anton Goloborodko & Lev Levitsky
#  |  Licensed under the Apache License, Version 2.0 (the "License");
#  |  you may not use this file except in compliance with the License.
#  |  You may obtain a copy of the License at
#  |
#  |    http://www.apache.org/licenses/LICENSE-2.0
#  |
#  |  Unless required by applicable law or agreed to in writing, software
#  |  distributed under the License is distributed on an "AS IS" BASIS,
#  |  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  |  See the License for the specific language governing permissions and
#  |  limitations under the License.
#  |
#  |  See also:
#  |  Goloborodko, A.A.; Levitsky, L.I.; Ivanov, M.V.; and Gorshkov, M.V. (2013)
#  |  "Pyteomics - a Python Framework for Exploratory Data Analysis and Rapid Software
#  |  Prototyping in Proteomics", Journal of The American Society for Mass Spectrometry,
#  |  24(2), 301–304. DOI: `10.1007/s13361-012-0516-6 <http://dx.doi.org/10.1007/s13361-012-0516-6>`_
#  |
#  |  Levitsky, L.I.; Klein, J.; Ivanov, M.V.; and Gorshkov, M.V. (2018)
#  |  "Pyteomics 4.0: five years of development of a Python proteomics framework",
#  |  Journal of Proteome Research.
#  |  DOI: `10.1021/acs.jproteome.8b00717 <http://dx.doi.org/10.1021/acs.jproteome.8b00717>`_
#
#  Also based on molmass (https://github.com/cgohlke/molmass)
#  |  Copyright (c) 1990-2020, Christoph Gohlke
#  |  All rights reserved.
#  |  Licensed under the BSD 3-Clause License
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  1. Redistributions of source code must retain the above copyright notice,
#  |     this list of conditions and the following disclaimer.
#  |
#  |  2. Redistributions in binary form must reproduce the above copyright notice,
#  |     this list of conditions and the following disclaimer in the documentation
#  |     and/or other materials provided with the distribution.
#  |
#  |  3. Neither the name of the copyright holder nor the names of its
#  |     contributors may be used to endorse or promote products derived from
#  |     this software without specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  |  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  |  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  |  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  |  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  |  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  |  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  |  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  |  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  |  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  |  POSSIBILITY OF SUCH DAMAGE.
#  |

# stdlib
import math
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
from typing import Dict, Iterator, List, Optional, Sequence, Tuple, Type, TypeVar

# 3rd party
from domdf_python_tools.doctools import prettify_docstrings
from mathematical.utils import gcd_array  # nodep

# this package
from chemistry_tools.elements import ELEMENTS, D, T, isotope_data
from chemistry_tools.formulae.parser import string_to_composition

# this package
from ._parser_core import _make_isotope_string
from .composition import Composition
from .iso_dist import IsotopeDistribution
from .utils import GROUPS, hill_order, split_isotope

__all__ = ["Formula", 'F']

F = TypeVar('F', bound="Formula")


@prettify_docstrings
class Formula(defaultdict, Counter):
	"""
	A Formula object stores a chemical composition of a compound.
	It is based on :class:`dict`, with the symbols of chemical elements
	as keys and the values equal to the number of atoms of the corresponding
	element in the compound.

	:param composition: A :class:`~chemistry_tools.formulae.formula.Formula` object with the elemental
		composition of a substance, or a :class:`python:dict` representing the same.
		If :py:obj:`None` an empty object is created
	:param charge:

	.. autosummary-widths:: 55/100
	"""

	# TODO: option to convert D and T to H[2] and H[3] ("heavy hydrogen")

	def __init__(self, composition: Optional[Dict[str, int]] = None, charge: int = 0):
		defaultdict.__init__(self, int)

		self.charge = 0

		if composition is not None:
			for isotope_string, num_atoms in composition.items():
				element_name, isotope_num = split_isotope(isotope_string)

				# Remove explicitly undefined isotopes (e.g. X[0]).
				self[_make_isotope_string(element_name, isotope_num)] = num_atoms

			if isinstance(composition, Formula):
				if composition.charge:
					if charge and composition.charge:
						if charge != composition.charge:
							# No point raising error if the charges are the same
							raise ValueError(
									"Charge is specified in both the composition and with the "
									f"'charge' keyword argument. {charge}, {self.charge}"
									)

					charge = composition.charge

		self._set_charge(charge)

	def _set_charge(self, charge: int):
		# Get charge
		if charge and self.charge:
			if charge != self.charge:
				# No point raising error if the charges are the same
				raise ValueError(
						"Charge is specified in both the formula and with the "
						f"'charge' keyword argument. {charge}, {self.charge}"
						)
		elif charge:
			self.charge = charge

	@classmethod
	def from_string(cls: Type['F'], formula: str, charge: int = 0) -> F:
		"""
		Create a new :class:`~chemistry_tools.formulae.formula.Formula` object by parsing a string.

		.. latex:vspace:: -5px

		.. note:: Isotopes cannot (currently) be parsed using this method

		.. latex:vspace:: -5px

		:param formula: A string with a chemical formula
		:param charge:

		.. TODO:: should throw error for unrecognised elements CGCGAATTCGCG
		"""

		_class = cls()

		formula = str(formula)
		formula = formula.strip().replace(' ', '')

		# Substitute abbreviations of common chemical groups
		for grp in reversed(sorted(GROUPS)):
			formula = formula.replace(grp, f"({GROUPS[grp]})")

		comp_and_charge = string_to_composition(formula)
		# print(comp_and_charge)

		if 0 in comp_and_charge:
			if charge:
				if comp_and_charge[0] != charge:
					raise ValueError("Cannot supply 'charge' when the formula already has a charge!")

			charge = comp_and_charge[0]

		for symbol, number in comp_and_charge.items():
			if number == 0:
				raise ValueError(f"Unrecognised formula: {formula}")
			# isotope = 0
			if symbol == 0:
				continue

			# isotope_re_1 = re.match(r"([A-z]+)(\[[0-9]*\])", symbol)
			# isotope_re_2 = re.findall(r"(\[[A-z]+)([0-9]*\])", symbol)
			#
			# if isotope_re_1:
			# 	elem, isotope = isotope_re_1[0]
			# 	isotope = re.findall(r"(\[)([0-9]+)(\])", isotope)[0][1]
			# 	if not isotope:
			# 		isotope = 0
			# elif isotope_re_2:
			# 	elem, isotope = isotope_re_2[0]
			# 	elem = elem.lstrip("[")
			# 	isotope = isotope.rstrip("]")
			# elif symbol not in ELEMENTS:
			# 	raise ValueError(f'Unknown chemical element with symbol {symbol}')
			# else:
			# 	elem = ELEMENTS[symbol].symbol
			elem, isotope = split_isotope(symbol)

			iso_str = _make_isotope_string(elem, int(isotope) if isotope else 0)
			_class[iso_str] += int(number) if number else 1

		_class._set_charge(charge)
		return _class

	@classmethod
	def from_mass_fractions(
			cls: Type['F'],
			fractions: Dict[str, float],
			charge: int = 0,
			maxcount: int = 10,
			precision: float = 1e-4,
			) -> "Formula":
		"""
		Create a new :class:`~chemistry_tools.formulae.formula.Formula` object
		from elemental mass fractions by parsing a string.

		.. latex:vspace:: -5px

		.. note:: Isotopes cannot (currently) be parsed using this method

		.. latex:vspace:: -5px

		:param fractions: A dictionary of elements and mass fractions
		:param charge:
		:param maxcount:
		:param precision:

		:bold-title:`Examples:`

		.. code-block:: python

			>>> Formula.from_mass_fractions({'H': 0.112, 'O': 0.888})
			'H2O'
			>>> Formula.from_mass_fractions({'D': 0.2, 'O': 0.8})
			'O[2H]2'
			>>> Formula.from_mass_fractions({'H': 8.97, 'C': 59.39, 'O': 31.64})
			'C5H9O2'
			>>> Formula.from_mass_fractions({'O': 0.26, '30Si': 0.74})
			'O2[30Si]3'
		"""  # noqa: D400

		# divide normalized fractions by element/isotope mass
		numbers = {}
		sumfractions = sum(fractions.values())
		for symbol, fraction in fractions.items():
			if symbol[0].isupper():
				try:
					mass = ELEMENTS[symbol].mass
				except KeyError as exc:
					raise ValueError(f"Unknown element '{symbol}'") from exc
			else:
				if symbol.startswith('['):
					symbol = symbol[1:-1]
				i = 0
				while symbol[i].isdigit():
					i += 1
				massnum = int(symbol[:i])
				symbol = symbol[i:]
				try:
					mass = ELEMENTS[symbol].isotopes[massnum].mass
				except KeyError as exc:
					raise ValueError(f"Unknown isotope '[{massnum}{symbol}]'") from exc
				symbol = f"[{massnum}{symbol}]"
			numbers[symbol] = fraction / (sumfractions * mass)

		# divide numbers by smallest number
		smallest = min(numbers.values())
		for symbol in numbers:
			numbers[symbol] /= smallest

		# find smallest factor that turns all numbers into integers
		precision *= len(numbers)
		best = 1e6
		factor = 1
		for i in range(1, maxcount):
			x = sum(abs((i * n) - round(i * n)) for n in numbers.values())
			if x < best:
				best = x
				factor = i
				if best < i * precision:
					break

		formula = []
		for symbol, number in sorted(numbers.items()):
			count = int(round(factor * number))
			if count > 1:
				formula.append(f'{symbol}{count}')
			else:
				formula.append(symbol)

		return cls.from_string(''.join(formula), charge=charge)

	@classmethod
	def from_kwargs(cls: Type['F'], *, charge: int = 0, **kwargs) -> F:
		"""
		Create a new :class:`~chemistry_tools.formulae.formula.Formula` object from
		keyword arguments representing the elements in the compound.

		:param charge:

		:rtype:

		.. latex:clearpage::
		"""  # noqa: D400

		return cls(kwargs, charge=charge)

	@property
	def monoisotopic_mass(self) -> float:
		"""
		Calculate the monoisotopic mass of a :class:`~chemistry_tools.formulae.formula.Formula`.
		If any isotopes are already present in the formula, the mass of these will be preserved
		"""

		# Calculate mass
		mass = 0.0

		for element, count in self.items():
			if element == 'D':
				iso_mass = D.mass
			elif element == 'T':
				iso_mass = T.mass
			else:
				symbol, isotope = split_isotope(element)

				if isotope:
					iso_mass = ELEMENTS[symbol].isotopes[isotope].mass
				else:
					iso_mass = ELEMENTS[symbol].isotopes[ELEMENTS[symbol].nominalmass].mass

			mass += iso_mass * count

		return mass

	@property
	def nominal_mass(self) -> float:
		"""
		Calculate the monoisotopic mass of a :class:`~chemistry_tools.formulae.formula.Formula`.
		If any isotopes are already present in the formula, the mass of these will be preserved
		"""

		return self.monoisotopic_mass

	@property
	def exact_mass(self) -> float:
		"""
		Calculate the monoisotopic mass of a :class:`~chemistry_tools.formulae.formula.Formula`.
		If any isotopes are already present in the formula, the mass of these will be preserved
		"""

		return self.monoisotopic_mass

	@property
	def mass(self) -> float:
		"""
		Calculate the average mass of a :class:`~chemistry_tools.formulae.formula.Formula`.

		Note that mass is not averaged for elements with specified isotopes.
		"""

		# Calculate mass
		mass = 0.0

		for element, count in self.items():
			if element == 'D':
				iso_mass = D.mass
			elif element == 'T':
				iso_mass = T.mass
			else:
				symbol, isotope = split_isotope(element)

				if isotope:
					iso_mass = ELEMENTS[symbol].isotopes[isotope].mass
				else:
					iso_mass = ELEMENTS[symbol].mass

			mass += iso_mass * count

		return mass

	@property
	def average_mass(self) -> float:
		"""
		Calculate the average mass of a :class:`~chemistry_tools.formulae.formula.Formula`.

		Note that mass is not averaged for elements with specified isotopes.
		"""

		return self.mass

	@property
	def mz(self) -> float:
		"""
		The mass to charge ratio of the formula.
		"""

		return self.get_mz(average=False)

	@property
	def average_mz(self) -> float:
		"""
		The average mass to charge ratio of the formula.
		"""

		return self.get_mz(average=True)

	def get_mz(self, average: bool = True, charge: Optional[int] = None) -> float:
		"""
		Calculate the average mass:charge ratio (*m/z*) of a :class:`~chemistry_tools.formulae.formula.Formula`.

		:param average: If :py:obj:`True` then the average *m/z* is calculated. Note that the mass
			is not averaged for elements with specified isotopes.
		:param charge: The charge of the compound. If :py:obj:`None` then the existing charge of the Formula is used
		"""

		if average:
			mass = self.mass
		else:
			mass = self.monoisotopic_mass

		# Calculate m/z
		if charge:
			mass /= charge
		elif self.charge:
			mass /= self.charge

		return mass

	def most_probable_isotopic_composition(
			self,
			elements_with_isotopes: Optional[Sequence[str]] = None,
			) -> Tuple["Formula", float]:
		"""
		Calculate the most probable isotopic composition of a molecule/ion.

		For each element, only two most abundant isotopes are considered.
		Any isotopes already in the Formula will be changed to the most abundant isotope

		:param elements_with_isotopes: A set of elements to be considered in isotopic distribution
			(by default, every element has an isotopic distribution).

		:return: A tuple with the most probable isotopic composition and its
			relative abundance.
		"""

		# Removing isotopes from the composition.
		for isotope_string in self:
			element_name, isotope_num = split_isotope(isotope_string)
			if isotope_num:
				self[element_name] += self.pop(isotope_string)

		isotopic_composition = Formula()

		for element_name in self:
			if not elements_with_isotopes or (element_name in elements_with_isotopes):
				# Take the two most abundant isotopes.
				first_iso, second_iso = sorted(
					[(i[0], i[1][1]) for i in isotope_data[element_name].items() if i[0]],
					key=lambda x: -x[1]
					)[:2]

				# Write the number of isotopes of the most abundant type.
				first_iso_str = _make_isotope_string(element_name, first_iso[0])
				isotopic_composition[first_iso_str] = int(math.ceil(self[element_name])) * first_iso[1]

				# Write the number of the second isotopes.
				second_iso_str = _make_isotope_string(element_name, second_iso[0])
				isotopic_composition[second_iso_str] = self[element_name] - isotopic_composition[first_iso_str]
			else:
				isotopic_composition[element_name] = self[element_name]

		return isotopic_composition, isotopic_composition.isotopic_composition_abundance

	@property
	def isotopic_composition_abundance(self) -> float:
		"""
		Calculate the relative abundance of the current isotopic composition of this molecule.

		:returns: The relative abundance of the current isotopic composition.
		"""

		isotopic_composition: defaultdict = defaultdict(dict)

		# Check if there are default and non-default isotopes of the same
		# element and rearrange the elements.
		for element in self:
			element_name, isotope_num = split_isotope(element)

			# If there is already an entry for this element and either it
			# contains a default isotope or newly added isotope is default
			# then raise an exception.
			if (
					element_name in isotopic_composition
					and (isotope_num == 0 or 0 in isotopic_composition[element_name])
					):
				raise ValueError(
						"Please specify the isotopic states of all atoms of "
						f"{element_name} or do not specify them at all."
						)
			else:
				isotopic_composition[element_name][isotope_num] = (self[element])

		# Calculate relative abundance.
		num1, num2, denom = 1, 1, 1

		for element_name, isotope_dict in isotopic_composition.items():
			num1 *= math.factorial(sum(isotope_dict.values()))
			for isotope_num, isotope_content in isotope_dict.items():
				denom *= math.factorial(isotope_content)
				if isotope_num:
					num2 *= (isotope_data[element_name][isotope_num][1]**isotope_content)

		return num2 * (num1 / denom)

	def iter_isotopologues(
			self,
			report_abundance: bool = False,
			elements_with_isotopes: Optional[Sequence[str]] = None,
			isotope_threshold: float = 5e-4,
			overall_threshold: float = 0,
			) -> Iterator:  # TODO: of what?
		"""
		Iterate over possible isotopic states of the molecule.

		The space of possible isotopic compositions is restrained by parameters
		``elements_with_isotopes``, ``isotope_threshold``, ``overall_threshold``.

		:param report_abundance: If :py:obj:`True`, the output will contain 2-tuples: `(composition, abundance)`.
			Otherwise, only compositions are yielded.
		:param elements_with_isotopes: A set of elements to be considered in isotopic distributions
			(by default, every element has an isotopic distribution).
		:param isotope_threshold: The threshold abundance of a specific isotope to be considered.
		:param overall_threshold: The threshold abundance of the calculated isotopic composition.

		:return: Iterator over possible isotopic compositions.
		"""

		dict_elem_isotopes = {}
		for element in self:
			if elements_with_isotopes is None or element in elements_with_isotopes:
				element_name, isotope_num = split_isotope(element)
				isotopes = {
					k: v
					for k, v in isotope_data[element_name].items()
					if k != 0 and v[1] >= isotope_threshold}  # yapf: disable
				list_isotopes = [_make_isotope_string(element_name, k) for k in isotopes]
				dict_elem_isotopes[element] = list_isotopes
			else:
				dict_elem_isotopes[element] = [element]

		all_isotoplogues = []
		for element, list_isotopes in dict_elem_isotopes.items():
			n = self[element]
			list_comb_element_n = []
			for elementXn in combinations_with_replacement(list_isotopes, n):
				list_comb_element_n.append(elementXn)
			all_isotoplogues.append(list_comb_element_n)

		for isotopologue in product(*all_isotoplogues):
			flat_isotopologue = [atom for element in isotopologue for atom in element]
			ic = Formula(Counter(flat_isotopologue))
			if report_abundance or overall_threshold > 0.0:
				abundance = ic.isotopic_composition_abundance
				if abundance > overall_threshold:
					if report_abundance:
						yield ic, abundance
					else:
						yield ic
			else:
				yield ic

	def isotope_distribution(self) -> IsotopeDistribution:
		"""
		Returns an :class:`~.IsotopeDistribution` object representing the distribution of the
		isotopologues of the formula.
		"""  # noqa: D400

		return IsotopeDistribution(self)

	def copy(self: F) -> F:
		"""
		Returns a copy of the :class:`~.Formula`.
		"""

		return self.__class__(self, charge=self.charge)

	def __missing__(self, key):
		# override default behavior: we don't want to add 0's to the dictionary
		return 0

	def __setitem__(self, key, value):
		if isinstance(value, float):
			value = int(round(value))
		elif not isinstance(value, int):
			raise TypeError(f"Only integers allowed as values in Formula, got {type(value).__name__}.")
		if value:  # reject 0's
			super(defaultdict, self).__setitem__(key, value)
		elif key in self:
			del self[key]

	def __add__(self, other):
		result = self.copy()
		for elem, count in other.items():
			result[elem] += count
		return result

	def __iadd__(self, other):
		for elem, count in other.items():
			self[elem] += count
		return self

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		result = self.copy()
		for elem, count in other.items():
			result[elem] -= count
		return result

	def __isub__(self, other):
		for elem, count in other.items():
			self[elem] -= count
		return self

	def __rsub__(self, other):
		return (self - other) * (-1)

	def __mul__(self, other):
		if not isinstance(other, int):
			raise TypeError(f'Cannot multiply Formula by non-integer "{other}"')
		return type(self)({k: v * other for k, v in self.items()})

	def __imul__(self, other):
		if not isinstance(other, int):
			raise TypeError(f'Cannot multiply Formula by non-integer "{other}"')
		for elem in self:
			self[elem] *= other
		return self

	def __rmul__(self, other):
		return self * other

	def __eq__(self, other) -> bool:
		if isinstance(other, (dict, Formula)):
			self_items = {i for i in self.items() if i[1]}
			other_items = {i for i in other.items() if i[1]}

			if isinstance(other, Formula):
				return self_items == other_items and self.charge == other.charge
			else:
				return self_items == other_items
		else:
			return NotImplemented

	def __str__(self) -> str:
		return self.hill_formula

	def _repr_elements(self) -> List[str]:
		elements = [str(dict.__repr__(self))]

		if self.charge:
			elements.append(f"charge={self.charge}")

		return elements

	def __repr__(self) -> str:
		return f'{type(self).__name__}({", ".join(self._repr_elements())})'

	@property
	def hill_formula(self) -> str:
		"""
		Returns the formula in Hill notation.

		:bold-title:`Example:`

		.. code-block:: python

			>>> Formula.from_string('BrC2H5').hill_formula
			'C2H5Br'
			>>> Formula.from_string('HBr').hill_formula
			'BrH'
			>>> Formula.from_string('[(CH3)3Si2]2NNa').hill_formula
			'C6H18NNaSi4'
		"""

		hill = []

		for symbol in hill_order(self.elements):
			hill.append(symbol)
			count = self[symbol]
			if count > 1:
				hill.append(str(count))

		# alphabet = sorted(ELEMENTS.symbols)
		#
		# if "C" in self:
		# 	hill.append("C")
		# 	alphabet.remove("C")
		# 	count = self["C"]
		# 	if count > 1:
		# 		hill.append(str(count))
		# 	if "H" in self:
		# 		hill.append("H")
		# 		alphabet.remove("H")
		# 		count = self["H"]
		# 		if count > 1:
		# 			hill.append(str(count))
		#
		# for element in alphabet:
		# 	if element in self:
		# 		hill.append(element)
		# 		count = self[element]
		# 		if count > 1:
		# 			hill.append(str(count))
		#
		return ''.join(hill)

	@property
	def no_isotope_hill_formula(self) -> str:
		"""
		Returns formula in Hill notation, without any isotopes specified.

		:bold-title:`Example:`

		.. code-block:: python

			>>> Formula.from_string('BrC2H5').no_isotope_hill_formula
			'C2H5Br'
			>>> Formula.from_string('HBr').no_isotope_hill_formula
			'BrH'
			>>> Formula.from_string('[(CH3)3Si2]2NNa').no_isotope_hill_formula
			'C6H18NNaSi4'
		"""

		hill = []

		ordered_symbols: Dict[str, int] = dict()

		for symbol in hill_order(self.elements):
			count = self[symbol]
			symbol, _ = split_isotope(symbol)
			if symbol in ordered_symbols:
				ordered_symbols[symbol] += count
			else:
				ordered_symbols[symbol] = count

		for symbol, count in ordered_symbols.items():
			hill.append(symbol)
			if count > 1:
				hill.append(str(count))

		return ''.join(hill)

	@property
	def empirical_formula(self) -> str:
		"""
		Returns the empirical formula in Hill notation.

		The empirical formula has the simplest whole number ratio of atoms
		of each element present in the formula.

		:bold-title:`Examples:`

		.. code-block:: python

			>>> Formula.from_string('H2O').empirical_formula
			'H2O'
			>>> Formula.from_string('S4').empirical_formula
			'S'
			>>> Formula.from_string('C6H12O6').empirical_formula
			'CH2O'
		"""

		hill = []
		values = list(self.values())
		if len(values) > 1:
			divisor = gcd_array(values)
		else:
			divisor = values[0]

		for symbol in hill_order(self.elements):
			hill.append(symbol)
			count = self[symbol] // divisor
			if count > 1:
				hill.append(str(count))

		return ''.join(hill)

	@property
	def n_atoms(self) -> int:
		"""
		Return the number of atoms in the formula.

		:bold-title:`Example:`

		.. code-block:: python

			>>> Formula.from_string('CH3COOH').n_atoms
			8
		"""

		return sum(list(self.values()))

	@property
	def n_elements(self) -> int:
		"""
		Return the number of elements in the formula.

		:rtype:

		:bold-title:`Example:`

		.. code-block:: python

			>>> Formula.from_string('CH3COOH').n_elements
			3


		.. latex:clearpage::
		"""

		return len(self)

	@property
	def elements(self) -> List[str]:  # type: ignore
		"""
		A list of the element symbols in the formula.
		"""

		return list(self.keys())

	@property
	def composition(self) -> "Composition":
		"""
		A :class:`~.Composition` object representing the elemental composition of the Formula.
		"""

		return Composition(self)
