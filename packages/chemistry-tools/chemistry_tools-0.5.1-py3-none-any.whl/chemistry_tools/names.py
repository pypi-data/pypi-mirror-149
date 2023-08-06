#!/usr/bin/env python3
#
#  names.py
"""
Functions for working with IUPAC names for chemicals.
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
import re
from typing import Any, Dict, List, Pattern, Sequence, Tuple

# 3rd party
from pandas import DataFrame  # type: ignore

# this package
from chemistry_tools import cached_requests
from chemistry_tools.constants import prefixes
from chemistry_tools.pubchem.errors import HTTP_ERROR_CODES

__all__ = [
		"get_IUPAC_parts",
		"sort_IUPAC_names",
		"get_IUPAC_sort_order",
		"get_sorted_parts",
		"sort_array_by_name",
		"sort_dataframe_by_name",
		"iupac_name_from_cas",
		"cas_from_iupac_name",
		"multiplier_regex",
		"re_strings",
		]

#: Regular expression to match "multiple" prefixes such as **mono-**.
multiplier_regex = re.compile('*'.join([f"({prefix})" for prefix in prefixes.values()]) + '*')

#: List of regular expressions to decompose an IUPAC name.
re_strings: List[Pattern] = [
		re.compile(r"((\d+),?)+(\d+)-"),
		multiplier_regex,
		re.compile(r"nitro"),
		re.compile(r"phenyl"),
		re.compile(r"aniline"),
		re.compile(r"anisole"),
		re.compile(r"benzene"),
		re.compile(r"centralite"),
		re.compile(r"formamide"),
		re.compile(r"glycerine"),
		re.compile(r"nitrate"),
		re.compile(r"glycol"),
		re.compile(r"phthalate"),
		re.compile(r"picrate"),
		re.compile(r"toluene"),
		re.compile(r"methyl"),
		re.compile(r"(?<!m)ethyl"),
		re.compile(r"propyl"),
		re.compile(r"butyl"),
		re.compile(r" "),
		re.compile(r"\("),
		re.compile(r"\)"),
		re.compile(r"hydroxyl"),
		re.compile(r"amin[oe]"),
		re.compile(r"amide"),
		]

_iupac_subs: List[Tuple[Pattern, str]] = [
		# (Regex, replacement)

		# e.g. Bis(2-Nitrophenyl)Amine -> 2,2'-Dinitrophenylamine
		(re.compile(r"^(bis)(\()(\d)(-)(.*)(phenyl)(\))"), r"\3,\3'-Di\5di\6"),
		# e.g. 2-Nitro-N-(4-nitrophenyl)aniline -> 2,4'-Dinitrophenylaniline
		(re.compile(r"^(\d)(-nitro-n-\()(\d)(-nitro)(.*)(\))"), r"\1,\3'-Dinitro-N-\5"),
		(re.compile(r"-?[Nn]-phenylaniline"), "diphenylamine"),
		(re.compile(r"carbanilide"), "-1,3-diphenylurea"),
		(re.compile(r"(glycerol)(-)(\d)(-nitrate)"), r"\3-mononitroglycerin"),
		(re.compile(r"n,n'-"), "1,3-"),
		(re.compile(r"dipicryl"), "hexanitrodiphenyl"),
		(re.compile(r"picryl$"), "-1,3,5-trinitrobenzene"),
		(re.compile(r"picryl"), "-1,3,5-trinitrophenyl"),
		]

_hyphen_digit_hyphen = re.compile(r"(-)(\d)(-)")


def get_IUPAC_parts(string: str) -> List[str]:
	"""
	Splits an IUPAC name for a compound into its constituent parts.

	:param string: The IUPAC name to split.

	:returns: A list of constituent parts.
	"""

	string = string.lower()

	for regex, sub in _iupac_subs:
		string = regex.sub(sub.lower(), string)

	split_points = set()

	for regex in re_strings:
		for match in list(regex.finditer(string.lower())):
			start, end = match.span()
			if start != end:
				split_points.add(start)
				split_points.add(end)

	for match in _hyphen_digit_hyphen.finditer(string.lower()):
		start, end = match.span()
		if start != end:
			split_points.add(start + 1)

	split_points.discard(0)
	split_points_list = sorted(split_points)
	start_point = 0

	string_chars = list(string)
	elements = []
	for point in split_points_list:
		elements.append(''.join(string_chars[start_point:point]))
		start_point = point

	elements.append(''.join(string_chars[start_point:]))

	# Fixups
	fixups = [
			["guani", "di", "ne"],
			]

	for fixup in fixups:
		length = len(fixup)
		for i in range(len(elements)):
			if elements[i:i + length] == fixup:
				elements = elements[:i] + [''.join(fixup)] + elements[i + length:]

	# Remove null elements
	null_elements = {' ', ''}

	elements = [x for x in elements if x not in null_elements]

	while not elements[-1]:
		elements = elements[:-1]

	return elements


#
# from string import ascii_letters
# alphabet = ascii_letters + "0123456789" + ",'" + "- " + '!"#$%&()*+./:;<=>?@[\\]^_`{|}~'


def sort_IUPAC_names(iupac_names: Sequence[str]) -> List[str]:
	"""
	Sort a list of IUPAC names into order.

	:param iupac_names: The list of IUPAC names to sort

	:return: The list of sorted IUPAC names.
	"""

	sort_order = get_IUPAC_sort_order(iupac_names)

	# return [iupac_names[split_names.index(name)] for name in sorted_names]
	return sorted(iupac_names, key=lambda x: sort_order[x])


def get_IUPAC_sort_order(iupac_names: Sequence[str]) -> Dict[str, int]:
	"""
	Returns the order the given IUPAC names should be sorted in.

	Useful when sorting arrays containing data in addition to the name.
	e.g.

	.. code-block:: python

		>>> sort_order = get_IUPAC_sort_order([row[0] for row in data])
		>>> sorted_data = sorted(data, key=lambda row: sort_order[row[0]])

	where row[0] would be the name of the compound

	:param iupac_names: The list of IUPAC names to sort.

	:return: Dictionary mapping the IUPAC names to the order in which they should be sorted.
	"""

	split_names, sorted_names = _get_split_and_sorted_lists(iupac_names)

	sort_order = {}
	for index, name in enumerate(sorted_names):
		sort_order[iupac_names[split_names.index(name)]] = index

	return sort_order


def get_sorted_parts(iupac_names: Sequence[str]) -> List[List[str]]:
	"""
	Returns the constituent parts of the IUPAC names sorted into order.

	The parts returned are in reverse order
	(i.e. ``'diphenylamine'`` becomes ``['amine', 'phenyl', 'di']``).

	:param iupac_names:
	"""

	split_names, sorted_names = _get_split_and_sorted_lists(iupac_names)

	return [split_names[split_names.index(name)] for name in sorted_names]


def _get_split_and_sorted_lists(iupac_names: Sequence[str]) -> Tuple[List[List[str]], List[List[str]]]:
	split_names = []

	for name in iupac_names:
		split_name = get_IUPAC_parts(name.lower())

		if split_name[0].lower() in prefixes.values():
			# no positional information at beginning
			split_name = [' ', *split_name]

		split_names.append(split_name[::-1])

	sorted_names = sorted(split_names)

	return split_names, sorted_names


def sort_array_by_name(array: List[List[Any]], name_col: int = 0, reverse: bool = False) -> List[List[Any]]:
	"""
	Sort a list of lists by the IUPAC name in each row.

	:param array:
	:param name_col: The index of the column containing the IUPAC names
	:param reverse: Whether the names should be sorted in reverse order. Default is :py:obj:`False`, which sorts from A-Z.
	:no-default reverse:

	:return: The sorted array
	"""

	names = [row[name_col] for row in array]
	sort_order = get_IUPAC_sort_order(names)
	sorted_array = sorted(array, key=lambda row: sort_order[row[name_col]], reverse=reverse)
	return sorted_array


def sort_dataframe_by_name(df: DataFrame, name_col: str, reverse: bool = False) -> DataFrame:
	"""
	Sorts a :class:`pandas.DataFrame` by the IUPAC name in each row.

	:param df:
	:param name_col: The name of the column containing the IUPAC names
	:param reverse: Whether the names should be sorted in reverse order. Default is :py:obj:`False`, which sorts from A-Z
	:no-default reverse:

	:return: The sorted :class:`~pandas.DataFrame`
	"""

	names = df[name_col]
	sort_order = get_IUPAC_sort_order(names)
	sorted_df = df.loc[df[name_col].map(sort_order).sort_values(ascending=(not reverse)).index]
	return sorted_df


def iupac_name_from_cas(cas_number: str) -> str:
	"""
	Returns the corresponding IUPAC name for the given CAS registry number.

	:param cas_number: The cas number to search

	:return: The IUPAC name
	"""

	r = cached_requests.get(f"https://cactus.nci.nih.gov/chemical/structure/{cas_number}/iupac_name")
	if r.status_code in HTTP_ERROR_CODES:
		raise ValueError(f"No compound found for CAS registry number {cas_number}.")

	return r.text


def cas_from_iupac_name(iupac_name: str) -> str:
	"""
	Returns the corresponding CAS registry number for the given IUPAC name.

	:param iupac_name: The IUPAC name to search.

	:return: The CAS registry number.
	"""

	r = cached_requests.get(f"https://cactus.nci.nih.gov/chemical/structure/{iupac_name}/cas")
	if r.status_code in HTTP_ERROR_CODES:
		raise ValueError(f"No compound found for name {iupac_name}.")

	return r.text.split('\n')[0]
