#!/usr/bin/env python3
#
#  images.py
"""
Functions for handling images.
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

# stdlib
from io import BytesIO
from typing import Sequence, Union

# 3rd party
from PIL import Image  # type: ignore  # nodep

# this package
from .enums import PubChemNamespace
from .pug_rest import do_rest_get

__all__ = ["get_structure_image"]


def get_structure_image(
		identifier: Union[str, int, Sequence[Union[str, int]]],
		namespace: Union[PubChemNamespace, str] = PubChemNamespace.name,
		width: int = 300,
		height: int = 300
		) -> Image.Image:
	"""
	Returns an image of the structure of the compound with the given name.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:param namespace: The type of identifier to look up. Valid values are in :class:`~.PubChemNamespace`.
	:param width: The image width in pixels.
	:param height: The image height in pixels.

	:return: Pillow Image data
	"""

	r = do_rest_get(namespace, identifier, "PNG", png_width=width, png_height=height)
	return Image.open(BytesIO(r.content))


rest_get_structure_image = get_structure_image
