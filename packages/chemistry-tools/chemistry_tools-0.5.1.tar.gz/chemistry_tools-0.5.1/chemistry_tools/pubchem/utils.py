#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
"""
#
#  Copyright (c) 2019-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import Any, Dict, Iterable, List, Sequence, Set, Union

# 3rd party
from apeye.requests_url import RequestsURL

# this package
from chemistry_tools.pubchem import API_BASE
from chemistry_tools.pubchem.enums import PubChemNamespace

__all__ = ["format_string"]


def format_string(stringwithmarkup: Dict[str, Any]) -> str:
	"""
	Convert a PubChem formatted string into an HTML formatted string.

	:param stringwithmarkup:
	"""

	string = list(stringwithmarkup["String"])
	try:
		markup_list = stringwithmarkup["Markup"]
	except KeyError:
		markup_list = []

	for markup in markup_list:
		style = None
		start = markup["Start"]
		end = markup["Length"] + start - 1
		if markup["Type"] == "Italics":
			style = 'i'
		# handle Other formats

		if style is None:
			print(markup)
			continue

		string[start] = f"<{style}>{string[start]}"
		string[end] = f"{string[end]}</{style}>"

	return ''.join(string)


def _force_sequence_or_csv(
		value: Union[str, int, Iterable[Union[str, int]]],
		name: str,
		) -> List[str]:
	"""
	Coerce ``value`` into a list of strings, including splitting comma-separated values.
	If that is not possible a :exc:`ValueError` is raised.

	:param value: The value to coerce to a list of strings.
	:param name: The name of the property. Used for error messages.
	"""

	err_msg = f"Please supply one or more {name}, either as a comma-separated string or a Sequence of strings."

	if not value:
		raise ValueError(err_msg)

	# --

	err_msg = f"'{name}' must be either a comma-separated string or a Sequence of strings"

	parsed_value: List[str]

	if isinstance(value, str):
		parsed_value = value.split(',')

	elif isinstance(value, int):
		parsed_value = [str(value)]

	elif isinstance(value, (Sequence, Set)):

		output: List[str] = []

		for idx, val in enumerate(value):
			if isinstance(val, str):
				output.append(val)
			elif isinstance(val, int):
				output.append(str(val))
			else:
				raise ValueError(err_msg)

		parsed_value = output

	else:
		raise ValueError(err_msg)

	return [val.strip() for val in parsed_value]


def _make_base_url(
		namespace: Union[PubChemNamespace, str],
		identifier: Union[str, int, Iterable[Union[str, int]]],
		) -> RequestsURL:
	"""
	Constructs the base URL for accessing data about a compound.

	:param namespace:
	:param identifier:

	.. versionchanged:: 0.5.0  Now returns a :class:`apeye.requests_url.RequestsURL`.
	"""

	identifier = _force_sequence_or_csv(identifier, "identifier")
	namespace = str(namespace)
	return API_BASE / f"compound/{namespace}/{','.join(identifier)}"
