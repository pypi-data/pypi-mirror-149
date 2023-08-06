#!/usr/bin/env python3
#
#  __init__.py
"""
Properties of the chemical elements.

Each chemical element is represented as an object instance. Physicochemical
and descriptive properties of the elements are stored as instance attributes.

Originally created by Christoph Gohlke <https://www.lfd.uci.edu/~gohlke/>`_
Licensed under the BSD 3-Clause license


References
----------
1. https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses
2. https://en.wikipedia.org/wiki/{element.name}


Examples
--------
>>> from chemistry_tools.elements import ELEMENTS
>>> ele = ELEMENTS['C']
>>> ele.number
6
>>> ele.symbol
'C'
>>> ele.name
'Carbon'
>>> ele.description[:21]
'Carbon is a member of'
>>> ele.eleconfig
'[He] 2s2 2p2'
>>> ele.eleconfig_dict
{(1, 's'): 2, (2, 's'): 2, (2, 'p'): 2}
>>> str(ELEMENTS[6])
'Carbon'
>>> len(ELEMENTS)
109
>>> sum(ele.mass for ele in ELEMENTS)
14693.181589001004
>>> for ele in ELEMENTS:
... 	ele.validate()

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
#  Based on molmass (https://github.com/cgohlke/molmass)
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
#  Isotope data from http://www.nist.gov/pml/data/comp.cfm
#

# this package
from ._elements import ELEMENTS, D, H, T
from ._isotope_data import isotope_data  # , undefined_isotopes
from ._table import BLOCKS, GROUPS, PERIODS, SERIES
from .actinides import Ac, Am, Bk, Cf, Cm, Es, Fm, Lr, Md, No, Np, Pa, Pu, Th, U
from .alkali_metals import Cs, Fr, K, Li, Na, Rb
from .alkaline_earth_metals import Ba, Be, Ca, Mg, Ra, Sr
from .chalcogens import Lv, O, Po, S, Se, Te
from .classes import Element, Elements, Isotope
from .halogens import At, Br, Cl, F, I, Ts
from .lanthanides import Ce, Dy, Er, Eu, Gd, Ho, La, Lu, Nd, Pm, Pr, Sm, Tb, Tm, Yb
from .noble_gases import Ar, He, Kr, Ne, Og, Rn, Xe
from .pnictogens import As, Bi, Mc, N, P, Sb
from .tetrels import C, Fl, Ge, Pb, Si, Sn
from .transition_metals import (
		Ag,
		Au,
		Bh,
		Cd,
		Cn,
		Co,
		Cr,
		Cu,
		Db,
		Ds,
		Fe,
		Hf,
		Hg,
		Hs,
		Ir,
		Mn,
		Mo,
		Mt,
		Nb,
		Ni,
		Os,
		Pd,
		Pt,
		Re,
		Rf,
		Rg,
		Rh,
		Ru,
		Sc,
		Sg,
		Ta,
		Tc,
		Ti,
		V,
		W,
		Y,
		Zn,
		Zr
		)
from .triels import Al, B, Ga, In, Nh, Tl

__all__ = (
		"Element",
		"Isotope",
		"PERIODS",
		"BLOCKS",
		"GROUPS",
		"SERIES",
		"ELEMENTS",
		"period_lengths",
		"accum_period_lengths",  # "groups",
		'H',
		'D',
		'T',
		"Li",  # Alkali Metals
		"Na",
		'K',
		"Rb",
		"Cs",
		"Fr",
		"Be",  # Alkaline Earth Metals
		"Mg",
		"Ca",
		"Sr",
		"Ba",
		"Ra",
		'B',  # Triels
		"Al",
		"Ga",
		"In",
		"Tl",
		"Nh",
		'C',  # Tetrels
		"Si",
		"Ge",
		"Sn",
		"Pb",
		"Fl",
		'N',  # pnictogens
		'P',
		"As",
		"Sb",
		"Bi",
		"Mc",
		'O',  # chalcogens
		'S',
		"Se",
		"Te",
		"Po",
		"Lv",
		'F',  # halogens
		"Cl",
		"Br",
		'I',
		"At",
		"Ts",
		"He",  # noble_gases
		"Ne",
		"Ar",
		"Kr",
		"Xe",
		"Rn",
		"Og",
		"La",  # lanthanides
		"Ce",
		"Pr",
		"Nd",
		"Pm",
		"Sm",
		"Eu",
		"Gd",
		"Tb",
		"Dy",
		"Ho",
		"Er",
		"Tm",
		"Yb",
		"Lu",
		"Ac",  # actinides
		"Th",
		"Pa",
		'U',
		"Np",
		"Pu",
		"Am",
		"Cm",
		"Bk",
		"Cf",
		"Es",
		"Fm",
		"Md",
		"No",
		"Lr",
		"Sc",  # transition_metals
		"Ti",
		'V',
		"Cr",
		"Mn",
		"Fe",
		"Co",
		"Ni",
		"Cu",
		"Zn",
		'Y',
		"Zr",
		"Nb",
		"Mo",
		"Tc",
		"Ru",
		"Rh",
		"Pd",
		"Ag",
		"Cd",
		"Hf",
		"Ta",
		'W',
		"Re",
		"Os",
		"Ir",
		"Pt",
		"Au",
		"Hg",
		"Rf",
		"Db",
		"Sg",
		"Bh",
		"Hs",
		"Mt",
		"Ds",
		"Rg",
		"Cn",
		)

period_lengths = (2, 8, 8, 18, 18, 32, 32)
accum_period_lengths = (2, 10, 18, 36, 54, 86, 118)

# icosagens, crystallogens, pnictogens, chalcogens, halogens
groups = {g: tuple(x - 18 + g for x in accum_period_lengths[1:]) for g in range(13, 18)}
groups[1] = (1, ) + tuple(x + 1 for x in accum_period_lengths[:-1])  # alkali metals
groups[2] = tuple(x + 2 for x in accum_period_lengths[:-1])  # alkaline earth metals
groups[18] = accum_period_lengths  # noble gases

if __name__ == "__main__":
	# stdlib
	import doctest

	print(f"ELEMENTS = {repr(ELEMENTS)}")
	doctest.testmod(verbose=False)
