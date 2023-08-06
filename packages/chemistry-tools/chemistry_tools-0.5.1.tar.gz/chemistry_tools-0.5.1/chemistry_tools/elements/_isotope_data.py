#!/usr/bin/env python3
#
#  isotope_masses.py
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

# stdlib
from typing import Dict, Tuple

# this package
from chemistry_tools.elements import ELEMENTS

isotopes_dict = Dict[int, Tuple[float, float]]

h_plus: isotopes_dict = {0: (1.00727646677, 1.0), 1: (1.00727646677, 1.0)}
electron: isotopes_dict = {0: (0.00054857990943, 1.0)}

isotope_data = dict()

for element in ELEMENTS:

	# if element.symbol in undefined_isotopes:
	# 	element_isotopes = undefined_isotopes[element.symbol]
	# else:
	element_isotopes = {}

	for massnumber, isotope in element.isotopes.items():
		element_isotopes[massnumber] = (isotope.mass, isotope.abundance)
		element_isotopes[0] = (element.mass, 1.0)

	isotope_data[element.symbol] = element_isotopes
	assert isotope_data[element.symbol][0]

isotope_data["H+"] = h_plus
isotope_data["e*"] = electron
