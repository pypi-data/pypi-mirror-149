#!/usr/bin/env python
#
#  atom.py
"""
Represents an atom in a :class:`~chemistry_tools.pubchem.compound.Compound`.
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
from itertools import zip_longest
from typing import Any, Dict, FrozenSet, Optional

# 3rd party
from domdf_python_tools.doctools import prettify_docstrings

# this package
from chemistry_tools.elements import ELEMENTS
from chemistry_tools.pubchem.errors import ResponseParseError

__all__ = ["Atom", "parse_atoms"]


@prettify_docstrings
class Atom:
	"""
	Class to represent an atom in a :class:`~chemistry_tools.pubchem.compound.Compound`.

	:param aid: The Atom ID within the owning Compound.
	:param number: The Atomic number for this atom.
	:param x: The x coordinate for this atom.
	:param y: The y coordinate for this atom.
	:param z: The z coordinate for this atom. Will be :py:obj:`None` in 2D Compound records.
	:param charge: Formal charge on atom.

	.. latex:clearpage::
	"""

	def __init__(
			self,
			aid: int,
			number: int,
			x: Optional[float] = None,
			y: Optional[float] = None,
			z: Optional[float] = None,
			charge: int = 0,
			):
		self.aid: int = aid
		self.number: int = number
		self.x: Optional[float] = x
		self.y: Optional[float] = y
		self.z: Optional[float] = z
		self.charge: int = charge

	def __repr__(self) -> str:
		return f"Atom({self.aid}, {self.element})"

	def __eq__(self, other) -> bool:
		return (
			isinstance(other, type(self))
			and self.aid == other.aid
			and self.element == other.element
			and self.x == other.x
			and self.y == other.y
			and self.z == other.z
			and self.charge == other.charge
			)  # yapf: disable

	@property
	def element(self) -> str:
		"""
		The element symbol for this atom.
		"""

		return ELEMENTS[self.number].symbol

	def to_dict(self) -> Dict[str, Any]:
		"""
		Return a dictionary containing Atom data.
		"""

		data = {"aid": self.aid, "number": self.number, "element": self.element}

		for coord in {'x', 'y', 'z'}:
			if getattr(self, coord) is not None:
				data[coord] = getattr(self, coord)

		if self.charge != 0:
			data["charge"] = self.charge

		return data

	def set_coordinates(self, x: float, y: float, z: Optional[float] = None) -> None:
		"""
		Set all coordinate dimensions at once.
		"""

		self.x = x
		self.y = y
		self.z = z

	@property
	def coordinate_type(self) -> str:
		"""
		Returns whether this atom has 2D or 3D coordinates.
		"""

		if self.z is None:
			return "2d"
		else:
			return "3d"


def parse_atoms(
		atoms_dict: Dict[str, Any],
		coords_dict: Optional[Dict] = None,
		) -> Dict[FrozenSet[int], Atom]:
	"""
	Parse atoms from the given dictionary.

	:param atoms_dict:
	:param coords_dict:
	"""

	atoms: Dict[FrozenSet[int], Atom] = {}

	# Create atoms
	aids = atoms_dict["aid"]
	elements = atoms_dict["element"]

	if not len(aids) == len(elements):
		raise ResponseParseError("Error parsing atom elements")

	for aid, element in zip(aids, elements):
		atoms[aid] = Atom(aid=aid, number=element)

	# Add coordinates
	if coords_dict:
		coord_ids = coords_dict[0]["aid"]

		xs = coords_dict[0]["conformers"][0]['x']
		ys = coords_dict[0]["conformers"][0]['y']
		zs = coords_dict[0]["conformers"][0].get('z', [])

		if not len(coord_ids) == len(xs) == len(ys) == len(atoms) or (zs and not len(zs) == len(coord_ids)):
			raise ResponseParseError("Error parsing atom coordinates")

		for aid, x, y, z in zip_longest(coord_ids, xs, ys, zs):
			atoms[aid].set_coordinates(x, y, z)

	# Add charges
	if "charge" in atoms_dict:
		for charge in atoms_dict["charge"]:
			atoms[charge["aid"]].charge = charge["value"]

	return atoms
