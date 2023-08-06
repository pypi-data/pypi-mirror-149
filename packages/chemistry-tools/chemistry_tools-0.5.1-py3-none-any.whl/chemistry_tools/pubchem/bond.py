#!/usr/bin/env python
#
#  bond.py
"""
Represents a bond between atoms in a :class:`~chemistry_tools.pubchem.compound.Compound`.
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
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
#  Based on PubChemPy https://github.com/mcs07/PubChemPy/blob/master/LICENSE
#  |  Copyright 2014 Matt Swain <m.swain@me.com>
#  |  Licensed under the MIT License
#  |
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# stdlib
from typing import Any, Dict, FrozenSet, Optional, Union

# 3rd party
from domdf_python_tools.doctools import prettify_docstrings
from enum_tools import IntEnum

# this package
from chemistry_tools.pubchem.errors import ResponseParseError

__all__ = ["BondType", "Bond", "parse_bonds"]


class BondType(IntEnum):
	"""
	Enumeration of possible bond types.
	"""

	SINGLE = 1
	DOUBLE = 2
	TRIPLE = 3
	QUADRUPLE = 4
	DATIVE = 5
	COMPLEX = 6
	IONIC = 7
	UNKNOWN = 255


@prettify_docstrings
class Bond:
	"""
	Class to represent a bond between two atoms in a
	:class:`~chemistry_tools.pubchem.compound.Compound`.

	:param aid1: ID of the begin atom of this bond
	:param aid2: ID of the end atom of this bond
	:param order: Bond order
	:param style: Bond style annotation.
	"""  # noqa: D400

	def __init__(
			self,
			aid1: int,
			aid2: int,
			order: Union[int, BondType] = BondType.SINGLE,
			style=None,
			):
		self.aid1: int = aid1
		self.aid2: int = aid2
		self.order: BondType = BondType(order)
		self.style = style

	def __repr__(self) -> str:
		return f"Bond({self.aid1}, {self.aid2}, {self.order!r})"

	def __eq__(self, other) -> bool:
		return (
			isinstance(other, type(self))
			and self.aid1 == other.aid1
			and self.aid2 == other.aid2
			and self.order == other.order
			and self.style == other.style
			)  # yapf: disable

	def to_dict(self) -> Dict[str, Any]:
		"""
		Return a dictionary containing Bond data.
		"""

		data = {"aid1": self.aid1, "aid2": self.aid2, "order": self.order}

		if self.style is not None:
			data["style"] = self.style

		return data


def parse_bonds(
		bonds_dict: Dict[str, Any],
		coords_dict: Optional[Dict] = None,
		) -> Dict[FrozenSet[int], Bond]:
	"""
	Parse bonds from the given dictionary.

	:param bonds_dict:
	:param coords_dict:
	"""

	bonds: Dict[FrozenSet[int], Bond] = {}

	if not bonds_dict:
		return bonds

	# Create bonds
	aid1s = bonds_dict["aid1"]
	aid2s = bonds_dict["aid2"]
	orders = bonds_dict["order"]

	if not len(aid1s) == len(aid2s) == len(orders):
		raise ResponseParseError("Error parsing bonds")

	for aid1, aid2, order in zip(aid1s, aid2s, orders):
		bonds[frozenset((aid1, aid2))] = Bond(aid1=aid1, aid2=aid2, order=order)

	# Add styles
	if coords_dict and "style" in coords_dict[0]["conformers"][0]:
		aid1s = coords_dict[0]["conformers"][0]["style"]["aid1"]
		aid2s = coords_dict[0]["conformers"][0]["style"]["aid2"]
		styles = coords_dict[0]["conformers"][0]["style"]["annotation"]
		for aid1, aid2, style in zip(aid1s, aid2s, styles):
			bonds[frozenset((aid1, aid2))].style = style

	return bonds
