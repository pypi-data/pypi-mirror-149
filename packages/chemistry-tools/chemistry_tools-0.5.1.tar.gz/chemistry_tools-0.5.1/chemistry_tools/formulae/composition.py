#!/usr/bin/env python3
#
#  composition.py
"""
Elemental composition of a :class:`~chemistry_tools.formulae.formula.Formula`.
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

# stdlib
from enum import Enum
from typing import Any, Dict, List

# this package
from chemistry_tools import formulae
from chemistry_tools.elements import ELEMENTS

# this package
from ._parser_core import _make_isotope_string
from .dataarray import DataArray
from .unicode import string_to_unicode
from .utils import split_isotope

__all__ = ["CompositionSort", "Composition"]


class CompositionSort(Enum):
	"""
	Lookup for sorting elemental composition output.
	"""

	symbol = "symbol"
	count = "count"
	rel_mass = "rel_mass"
	mass_fraction = "mass_fraction"
	Symbol = "symbol"
	Count = "count"
	Rel_mass = "rel_mass"
	Mass_fraction = "mass_fraction"
	Rel_Mass = "rel_mass"
	Mass_Fraction = "mass_fraction"

	def __str__(self) -> str:
		return str(self.value)


class Composition(DataArray):
	"""
	Class to represent the elemental composition of a :class:`~chemistry_tools.formulae.formula.Formula`.

	:param formula: A :class:`~chemistry_tools.formulae.formula.Formula` object to create the composition for
	"""

	def __init__(self, formula: "formulae.Formula"):
		data: Dict[str, Dict] = {}

		for isymbol, count in formula.items():
			symbol, isotope = split_isotope(isymbol)
			element = ELEMENTS[symbol]
			mass = element.mass * count
			mass_fraction = mass / formula.mass

			data[isymbol] = dict(
					element=element,
					isotope=isotope,
					count=count,
					rel_mass=mass,
					mass_fraction=mass_fraction,
					)

		super().__init__(formula=formula.hill_formula, data=data)

		self._total_mass: float = formula.mass

	@property
	def total_mass(self) -> float:
		"""
		The total mass of the composition.
		"""

		return self._total_mass

	@property
	def n_elements(self) -> int:
		"""
		The number of elements in the composition.
		"""

		return len(self)

	_as_array_kwargs = {"sort_by", "reverse"}
	_as_table_alignment = ["left", "right", "right", "right"]
	_as_table_float_format = [None, None, ".4f", ".4f"]

	def as_array(
			self,
			sort_by: CompositionSort = CompositionSort.symbol,
			reverse: bool = False,
			) -> List[List[Any]]:
		"""
		Returns the elemental composition as a list of lists.

		:param sort_by: The column to sort by.
		:param reverse: Whether the isotopologues should be sorted in reverse order.
		"""

		output = []
		sorted_data = []

		if sort_by not in CompositionSort:
			raise ValueError(f"Unrecognised value for 'sort_by': {sort_by}")
		elif sort_by == CompositionSort.symbol:
			iterable = sorted(self.keys(), reverse=reverse)
		else:
			iterable = sorted(self.keys(), key=lambda key: self[key][sort_by.value], reverse=reverse)

		for symbol in iterable:
			sorted_data.append(self[symbol])

		for data in sorted_data:
			symbol = _make_isotope_string(data["element"].symbol, data["isotope"])
			rel_mass = f"{data['rel_mass']:0.4f}"
			mass_fraction = f"{data['mass_fraction']:0.4f}"

			output.append([symbol, data["count"], rel_mass, mass_fraction])

		output.insert(0, ["Element", "Count", "Relative Mass", "Mass Fraction"])

		return output

	def __str__(self) -> str:
		table = self.as_table(sort_by=CompositionSort.symbol, reverse=True, tablefmt="fancy_grid")
		return f"\n Elemental Composition for {string_to_unicode(self.formula)}\n{table}"
