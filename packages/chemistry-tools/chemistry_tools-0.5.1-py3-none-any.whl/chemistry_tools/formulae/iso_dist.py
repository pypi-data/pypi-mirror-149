#!/usr/bin/env python3
#
#  iso_dist.py
"""
Isotope Distributions.
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
from collections import OrderedDict
from typing import Any, List, Union

# 3rd party
from domdf_python_tools.doctools import prettify_docstrings
from enum_tools import IntEnum
from enum_tools.documentation import document_enum

# this package
from chemistry_tools import formulae

# this package
from .dataarray import DataArray
from .unicode import string_to_unicode

__all__ = ["IsoDistSort", "IsotopeDistribution"]


@document_enum
class IsoDistSort(IntEnum):
	"""
	Lookup for sorting isotope distribution output.
	"""

	Formula = formula = 0  # doc: Sort the isosope distribution by the formulae.
	Mass = mass = 1  # doc: Sort the isotope distribution by the masses.
	Abundance = abundance = 2  # doc: Sort the isotope distribution by the abundances.
	Relative_Abundance = Relative_abundance = relative_abundance = 3  # doc: Sort the isotope distribution by the relative abundances.


@prettify_docstrings
class IsotopeDistribution(DataArray):
	"""
	An isotope distribution.

	:param formula: A :class:`~chemistry_tools.formulae.formula.Formula` object to create the distribution for

	Each composition can be accessed with their hill formulae like a dictionary
	(e.g. ``iso_dict['H[1]2O[16]']``)
	"""

	# TODO: as_mass_spec

	def __init__(self, formula: "formulae.Formula"):
		iso_compositions = list(formula.iter_isotopologues())
		compositions = OrderedDict()
		max_abundance: float = 0

		for comp in iso_compositions:
			compositions[comp.hill_formula] = comp
			abundance = comp.isotopic_composition_abundance
			if abundance > max_abundance:
				max_abundance = abundance

		super().__init__(formula=iso_compositions[0].no_isotope_hill_formula, data=compositions)

		self.max_abundance: float = max_abundance

	_as_array_kwargs = {"sort_by", "reverse", "format_percentage"}
	_as_table_alignment = ["left", "right", "right", "right"]
	_as_table_float_format = [None, ".4f", ".6f", ".6f"]

	def as_array(
			self,
			sort_by: Union[int, IsoDistSort] = IsoDistSort.formula,
			reverse: bool = False,
			format_percentage: bool = True
			) -> List[List[Any]]:
		"""
		Returns the isotope distribution data as a list of lists.

		:param sort_by: The column to sort by.
		:param reverse: Whether the isotopologues should be sorted in reverse order.
		:param format_percentage: Whether the abundances should be formatted as percentages or not.
		"""

		if sort_by == IsoDistSort.formula:
			sort_key = lambda comp: comp.hill_formula
		elif sort_by == IsoDistSort.mass:
			sort_key = lambda comp: comp.mass
		elif sort_by == IsoDistSort.abundance:
			sort_key = lambda comp: comp.isotopic_composition_abundance
		elif sort_by == IsoDistSort.relative_abundance:
			sort_key = lambda comp: comp.isotopic_composition_abundance / self.max_abundance
		else:
			raise ValueError(f"Unrecognised value for 'sort_by': {sort_by}")

		output = []

		for comp in sorted(self.values(), key=sort_key, reverse=reverse):
			abundance = comp.isotopic_composition_abundance
			rel_abund = abundance / self.max_abundance
			row = [comp.hill_formula, f"{comp.mass:0.4f}"]
			if format_percentage:
				row += [f"{abundance:0.2%}", f"{rel_abund:0.2%}"]
			else:
				row += [f"{abundance:0.6f}", f"{rel_abund:0.6f}"]
			output.append(row)
			# TODO: Unicode, latex, html representations of formulae

		output.insert(0, ["Formula", "Mass", "Abundance", "Relative Abundance"])

		return output

	def __str__(self) -> str:
		table = self.as_table(sort_by=IsoDistSort.relative_abundance, reverse=True, tablefmt="fancy_grid")
		return f"\n Isotope Distribution for {string_to_unicode(self.formula)}\n{table}"
