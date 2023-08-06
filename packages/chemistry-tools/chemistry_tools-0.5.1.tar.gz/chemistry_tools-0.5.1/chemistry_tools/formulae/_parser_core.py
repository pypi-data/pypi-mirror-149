#!/usr/bin/env python3
#
#  _parser_core.py
"""
Core functions and constants for parsing formulae.
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
#  Based on Pyteomics (https://github.com/levitsky/pyteomics)
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
#  Also based on ChemPy (https://github.com/bjodah/chempy)
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
import re
import warnings
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

__all__ = ["replace_substrings"]

_greek_letters: Tuple[str, ...] = (
		"alpha",
		"beta",
		"gamma",
		"delta",
		"epsilon",
		"zeta",
		"eta",
		"theta",
		"iota",
		"kappa",
		"lambda",
		"mu",
		"nu",
		"xi",
		"omicron",
		"pi",
		"rho",
		"sigma",
		"tau",
		"upsilon",
		"phi",
		"chi",
		"psi",
		"omega",
		)

_greek_u = "αβγδεζηθικλμνξοπρστυφχψω"


def _formula_to_format(
		sub: Callable,
		sup: Callable,
		formula: str,
		prefixes: Dict[str, str],
		infixes: Dict[str, str],
		suffixes: Sequence[str] = ("(s)", "(l)", "(g)", "(aq)"),
		) -> str:
	"""

	:param sub: The function to call to subscript a string.
	:param sup: The function to call to superscript a string.
	:param formula: The formula to format
	:param prefixes: Mapping of prefixes to their equivalents in the desired format
	:param infixes: Mapping of infixes to their equivalents in the desired format
	:param suffixes: Suffixes to keep, e.g. ("(g)", "(s)")

	:return: The formatted formula
	"""

	# TODO: make isotope square brackets be superscript
	parts = _formula_to_parts(formula, prefixes.keys(), suffixes)
	stoichs = parts[0].split('.')
	string = ''

	for idx, stoich in enumerate(stoichs):
		if idx == 0:
			m = 1
		else:
			m, stoich = _get_leading_integer(stoich)
			string += replace_substrings('.', infixes)
		if m != 1:
			string += str(m)

		string += re.sub(r"([0-9]+)(?![^\[]*\])", lambda m: sub(m.group(1)), stoich)

	if parts[1] is not None:
		chg = _get_charge(parts[1])
		if chg < 0:
			token = '-' if chg == -1 else f"{-chg:d}-"
		if chg > 0:
			token = '+' if chg == 1 else f"{chg:d}+"
		string += sup(token)

	if len(parts) > 4:
		raise ValueError("Incorrect formula")

	pre_str = ''.join(map(lambda x: replace_substrings(x, prefixes), parts[2]))

	return pre_str + string + ''.join(parts[3])


def _formula_to_parts(
		formula: str,
		prefixes: Iterable[str],
		suffixes: Sequence[str] = ("(s)", "(l)", "(g)", "(aq)"),
		) -> List[Any]:
	"""

	:param formula: The formula to split into parts.
	:param prefixes: Mapping of prefixes to their HTML equivalents. Default greek letters and ``.``
	:param suffixes: Suffixes to keep, e.g. ("(g)", "(s)")
	"""

	# Drop prefixes and suffixes
	drop_pref, drop_suff = [], []

	for ign in prefixes:
		if formula.startswith(ign):
			drop_pref.append(ign)
			formula = formula[len(ign):]

	for ign in suffixes:
		if formula.endswith(ign):
			drop_suff.append(ign)
			formula = formula[:-len(ign)]

	parts: Tuple[Optional[str], ...]

	# Extract charge
	for token in "+-":
		if token in formula:
			if formula.count(token) > 1:
				raise ValueError(f"Multiple tokens: {token}")
			parts_: List[str] = formula.split(token)
			parts = (parts_[0], token + parts_[1], *parts_[2:])
			break
	else:
		parts = (formula, None)

	return [*parts, tuple(drop_pref), tuple(drop_suff[::-1])]


def replace_substrings(string: str, patterns: Dict[str, str]) -> str:
	"""
	Replace substrings in a string.

	:param string: The string to replace substrings in.
	:param patterns: A dictionary mapping substrings to their replacements.

	:return: The resulting string.
	"""

	for patt, repl in patterns.items():
		string = string.replace(patt, repl)

	return string


def _get_leading_integer(s: str) -> Tuple[int, str]:
	"""
	Returns the leading integer from the string. If no leading integer is found it is assumed to be ``1``.

	:param s: The string to parse

	:return: A tuple comprising the leading integer and the remainder of the string
	"""

	matches = re.findall(r"^\d+", s)

	if len(matches) == 0:
		integer = 1
	elif len(matches) == 1:
		s = s[len(matches[0]):]
		integer = int(matches[0])
	else:
		raise ValueError(f"Failed to parse: {s}")

	return integer, s


def _get_charge(charge_str: str) -> int:
	"""
	Parses a string representing a charge.

	:param charge_str:

	:return: The charge

	:raises ValueError: If the charge string cannot be parsed.
	"""

	if charge_str == '+':
		return 1
	elif charge_str == '-':
		return -1

	for token, anti, sign in zip("+-", "-+", (1, -1)):
		if token in charge_str:
			if anti in charge_str:
				raise ValueError("Invalid charge description (+ & - present)")

			before, after = charge_str.split(token)

			if len(before) > 0 and len(after) > 0:
				raise ValueError("Values both before and after charge token")

			if len(before) > 0:
				# will_be_missing_in="0.8.0'
				warnings.warn("'Fe/3+' deprecated, use e.g. 'Fe+3'", DeprecationWarning, stacklevel=3)
				return sign * int(1 if before == '' else before)

			if len(after) > 0:
				return sign * int(1 if after == '' else after)

	raise ValueError("Invalid charge description (+ or - missing)")


def _make_isotope_string(element_name: str, isotope_num: Union[str, int]) -> str:
	"""
	Form a string label for an isotope. If ``isotope_num`` = 0 ``element_name`` is returned unchanged.

	:param element_name: The name or symbol of the element
	:param isotope_num: The isotope number

	:return: The isotope string
	"""

	if isotope_num in {0, '0'}:
		return element_name
	else:
		return f"[{isotope_num}{element_name}]"


_isotope_string = re.compile(r"^([A-Z][a-z+]*)(?:\[(\d+)])?$")


# TODO: merge with split_isotope
def _parse_isotope_string(label: str) -> Tuple[str, int]:
	"""
	Parse an string with an isotope label and return the element name and the isotope number.

	>>> _parse_isotope_string("C")
	("C", 0)
	>>> _parse_isotope_string("C[12]")
	("C", 12)

	:param label: The isotope label to parse

	:return: The name/symbol of the element, and the isotope number
	"""

	matches = _isotope_string.match(label)
	if matches:
		element_name, num = matches.groups()
		isotope_num = int(num) if num else 0
		return element_name, isotope_num
	else:
		raise ValueError(f"Failed to parse: {label}")
