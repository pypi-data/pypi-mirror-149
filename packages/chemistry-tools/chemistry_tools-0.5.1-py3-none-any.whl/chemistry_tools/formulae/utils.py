#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
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
import re
from functools import lru_cache
from typing import Dict, Iterator, List, Sequence, Tuple

# this package
from chemistry_tools.elements import ELEMENTS

__all__ = [
		"GROUPS",
		"split_isotope",
		"hill_order",
		]

#: Common chemical groups
GROUPS: Dict[str, str] = {
		"Abu": "C4H7NO",
		"Acet": "C2H3O",
		"Acm": "C3H6NO",
		"Adao": "C10H15O",
		"Aib": "C4H7NO",
		"Ala": "C3H5NO",
		"Arg": "C6H12N4O",
		"Argp": "C6H11N4O",
		"Asn": "C4H6N2O2",
		"Asnp": "C4H5N2O2",
		"Asp": "C4H5NO3",
		"Aspp": "C4H4NO3",
		"Asu": "C8H13NO3",
		"Asup": "C8H12NO3",
		"Boc": "C5H9O2",
		"Bom": "C8H9O",
		"Bpy": "C10H8N2",  # Bipyridine
		"Brz": "C8H6BrO2",
		"Bu": "C4H9",
		"Bum": "C5H11O",
		"Bz": "C7H5O",
		"Bzl": "C7H7",
		"Bzlo": "C7H7O",
		"Cha": "C9H15NO",
		"Chxo": "C6H11O",
		"Cit": "C6H11N3O2",
		"Citp": "C6H10N3O2",
		"Clz": "C8H6ClO2",
		"Cp": "C5H5",
		"Cy": "C6H11",
		"Cys": "C3H5NOS",
		"Cysp": "C3H4NOS",
		"Dde": "C10H13O2",
		"Dnp": "C6H3N2O4",
		"Et": "C2H5",
		"Fmoc": "C15H11O2",
		"For": "CHO",
		"Gln": "C5H8N2O2",
		"Glnp": "C5H7N2O2",
		"Glp": "C5H5NO2",
		"Glu": "C5H7NO3",
		"Glup": "C5H6NO3",
		"Gly": "C2H3NO",
		"Hci": "C7H13N3O2",
		"Hcip": "C7H12N3O2",
		"His": "C6H7N3O",
		"Hisp": "C6H6N3O",
		"Hser": "C4H7NO2",
		"Hserp": "C4H6NO2",
		"Hx": "C6H11",
		"Hyp": "C5H7NO2",
		"Hypp": "C5H6NO2",
		"Ile": "C6H11NO",
		"Ivdde": "C14H21O2",
		"Leu": "C6H11NO",
		"Lys": "C6H12N2O",
		"Lysp": "C6H11N2O",
		"Mbh": "C15H15O2",
		"Me": "CH3",
		"Mebzl": "C8H9",
		"Meobzl": "C8H9O",
		"Met": "C5H9NOS",
		"Mmt": "C20H17O",
		"Mtc": "C14H19O3S",
		"Mtr": "C10H13O3S",
		"Mts": "C9H11O2S",
		"Mtt": "C20H17",
		"Nle": "C6H11NO",
		"Npys": "C5H3N2O2S",
		"Nva": "C5H9NO",
		"Odmab": "C20H26NO3",
		"Orn": "C5H10N2O",
		"Ornp": "C5H9N2O",
		"Pbf": "C13H17O3S",
		"Pen": "C5H9NOS",
		"Penp": "C5H8NOS",
		"Ph": "C6H5",
		"Phe": "C9H9NO",
		"Phepcl": "C9H8ClNO",
		"Phg": "C8H7NO",
		"Pmc": "C14H19O3S",
		"Ppa": "C8H7O2",
		"Pro": "C5H7NO",
		"Prop": "C3H7",
		"Py": "C5H5N",
		"Pyr": "C5H5NO2",
		"Sar": "C3H5NO",
		"Ser": "C3H5NO2",
		"Serp": "C3H4NO2",
		"Sta": "C8H15NO2",
		"Stap": "C8H14NO2",
		"Tacm": "C6H12NO",
		"Tbdms": "C6H15Si",
		"Tbu": "C4H9",
		"Tbuo": "C4H9O",
		"Tbuthio": "C4H9S",
		"Tfa": "C2F3O",
		"Thi": "C7H7NOS",
		"Thr": "C4H7NO2",
		"Thrp": "C4H6NO2",
		"Tips": "C9H21Si",
		"Tms": "C3H9Si",
		"Tos": "C7H7O2S",
		"Trp": "C11H10N2O",
		"Trpp": "C11H9N2O",
		"Trt": "C19H15",
		"Tyr": "C9H9NO2",
		"Tyrp": "C9H8NO2",
		"Val": "C5H9NO",
		"Valoh": "C5H9NO2",
		"Valohp": "C5H8NO2",
		"Xan": "C13H9O",
		}

_isotope_regex_1 = re.compile(r"^([A-z]+)(\[\d*])$")
_isotope_regex_2 = re.compile(r"^(\[[A-z]+)(\d*])$")
_isotope_regex_3 = re.compile(r"^(\[\d*)([A-z]+])$")
_iso_bracket_regex = re.compile(r"^(\[)(\d+)(])$")
_hill_carbon_re = re.compile(r"(C(?:\[[0-9]+])?|\[[0-9]+C])")
_hill_hydrogen_re = re.compile(r"(H(?:\[[0-9]+])?|\[[0-9]+H])")


@lru_cache()
def split_isotope(string: str) -> Tuple[str, int]:
	"""
	Returns the symbol and mass number for the isotope represented by ``string``.

	Valid isotopes include ``'[C12]'``, ``'C[12]'`` and ``'[12C]'``.

	:param string:

	:return: Tuple representing the element and the isotope number.
	"""

	isotope = '0'

	iso_re_1 = _isotope_regex_1.findall(string)
	iso_re_2 = _isotope_regex_2.findall(string)
	iso_re_3 = _isotope_regex_3.findall(string)

	if iso_re_1:
		elem, isotope = iso_re_1[0]
		isotope = _iso_bracket_regex.findall(isotope)[0][1]
	elif iso_re_2:
		elem, isotope = iso_re_2[0]
		elem = elem.lstrip('[')
		isotope = isotope.rstrip(']')
	elif iso_re_3:
		isotope, elem = iso_re_3[0]
		isotope = isotope.lstrip('[')
		elem = elem.rstrip(']')
	else:
		elem = string

	if elem not in ELEMENTS:
		raise ValueError(f"Unknown chemical element with symbol {elem}")

	return ELEMENTS[elem].symbol, int(isotope)


def hill_order(symbols: Sequence[str]) -> Iterator[str]:
	"""
	Returns an iterator over the given element symbols in order of Hill notation.

	:bold-title:`Example:`

	.. code-block:: python

		>>> for i in hill_order("H", "C[12]", "O"): print(i, end='')
		CHO
	"""

	symbols_list: List[str] = list(set(symbols))

	carbon_isotopes = list(filter(_hill_carbon_re.findall, symbols_list))
	print(carbon_isotopes)

	if carbon_isotopes:
		for isotope in sorted(carbon_isotopes):
			symbols_list.remove(isotope)
			yield isotope

		hydrogen_isotopes = list(filter(_hill_hydrogen_re.findall, symbols_list))
		for isotope in sorted(hydrogen_isotopes):
			symbols_list.remove(isotope)
			yield isotope

	yield from sorted(symbols_list)
