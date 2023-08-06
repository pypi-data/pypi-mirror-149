#!/usr/bin/env python3
#
#  html.py
"""
Functions and constants for converting formulae to HTML.
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
from typing import Dict, Optional, Sequence, Union

# this package
from ._parser_core import _formula_to_format, _greek_letters

__all__ = ["string_to_html", "html_subscript", "html_superscript"]

_html_mapping: Dict[str, str] = {k + '-': '&' + k + ";-" for k in _greek_letters}
_html_mapping['.'] = "&sdot;"
_html_infix_mapping = _html_mapping


def string_to_html(
		formula: str,
		prefixes: Optional[Dict[str, str]] = None,
		infixes: Optional[Dict[str, str]] = None,
		suffixes: Sequence[str] = ("(s)", "(l)", "(g)", "(aq)"),
		) -> str:
	"""
	Convert formula string to HTML string representation.

	:bold-title:`Examples:`

	.. code-block:: python

		>>> string_to_html("NH4+")
		'NH<sub>4</sub><sup>+</sup>'
		>>> string_to_html("Fe(CN)6+2")
		'Fe(CN)<sub>6</sub><sup>2+</sup>'
		>>> string_to_html("Fe(CN)6+2(aq)")
		'Fe(CN)<sub>6</sub><sup>2+</sup>(aq)'
		>>> string_to_html(".NHO-(aq)")
		'&sdot;NHO<sup>-</sup>(aq)'
		>>> string_to_html("alpha-FeOOH(s)")
		'&alpha;-FeOOH(s)'

	:param formula: Chemical formula, e.g. ``'H2O'``, ``'Fe+3'``, ``'Cl-'``
	:param prefixes: Mapping of prefixes to their HTML equivalents. Default greek letters and ``.``
	:no-default prefixes:
	:param infixes: Mapping of infixes to their HTML equivalents.
	:param suffixes: Suffixes to keep.

	:return: The HTML representation of the formula
	"""

	if prefixes is None:
		prefixes = _html_mapping

	if infixes is None:
		infixes = _html_infix_mapping

	return _formula_to_format(html_subscript, html_superscript, formula, prefixes, infixes, suffixes)


def html_subscript(val: Union[str, float]) -> str:
	"""
	Returns the HTML subscript of the given value.

	:param val: The value to superscript
	"""

	return f"<sub>{val}</sub>"


def html_superscript(val: Union[str, float]) -> str:
	"""
	Returns the HTML superscript of the given value.

	:param val: The value to subscript
	"""

	return f"<sup>{val}</sup>"
