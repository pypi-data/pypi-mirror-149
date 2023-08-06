#!/usr/bin/env python3
#
#  _elements.py
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

# stdlib
from typing import Dict

# this package
from . import classes
from .actinides import *
from .alkali_metals import *
from .alkaline_earth_metals import *
from .chalcogens import *
from .halogens import *
from .lanthanides import *
from .noble_gases import *
from .pnictogens import *
from .tetrels import *
from .transition_metals import *
from .triels import *

__all__ = ("ELEMENTS", 'H', 'D', 'T')

# TODO: nominal mass (massnumber) and monoisotopic mass

H = classes.Element(
		1,
		'H',
		"Hydrogen",
		group=1,
		period=1,
		block='s',
		series=1,
		mass=1.007941,
		eleneg=2.2,
		eleaffin=0.75420375,
		covrad=0.32,
		atmrad=0.79,
		vdwrad=1.2,
		tboil=20.28,
		tmelt=13.81,
		density=0.084,
		eleconfig="1s",
		oxistates="1*, -1",
		ionenergy=(13.5984, ),
		isotopes={
				1: (1.00782503207, 0.999885),
				2: (2.0141017778, 0.000115),
				3: (3.0160492777, 0.0),
				4: (4.02781, 0.0),
				5: (5.03531, 0.0),
				6: (6.04494, 0.0),
				7: (7.05275, 0.0),
				},
		description=(
				"Colourless, odourless gaseous chemical element. Lightest and most "
				"abundant element in the universe. Present in water and in all "
				"organic compounds. Chemically reacts with most elements. Discovered "
				"by Henry Cavendish in 1776."
				)
		)

D = classes.HeavyHydrogen(
		1,
		'D',
		"Deuterium",
		mass=2.0141017778,
		isotopes={
				1: (1.00782503207, 0.999885),
				2: (2.0141017778, 0.000115),
				3: (3.0160492777, 0.0),
				4: (4.02781, 0.0),
				5: (5.03531, 0.0),
				6: (6.04494, 0.0),
				7: (7.05275, 0.0),
				},
		)

T = classes.HeavyHydrogen(
		1,
		'T',
		"Tritium",
		mass=3.0160492777,
		isotopes={
				1: (1.00782503207, 0.999885),
				2: (2.0141017778, 0.000115),
				3: (3.0160492777, 0.0),
				4: (4.02781, 0.0),
				5: (5.03531, 0.0),
				6: (6.04494, 0.0),
				7: (7.05275, 0.0),
				},
		)

ELEMENTS = classes.Elements(
		H,
		He,
		Li,
		Be,
		B,
		C,
		N,
		O,
		F,
		Ne,
		Na,
		Mg,
		Al,
		Si,
		P,
		S,
		Cl,
		Ar,
		K,
		Ca,
		Sc,
		Ti,
		V,
		Cr,
		Mn,
		Fe,
		Co,
		Ni,
		Cu,
		Zn,
		Ga,
		Ge,
		As,
		Se,
		Br,
		Kr,
		Rb,
		Sr,
		Y,
		Zr,
		Nb,
		Mo,
		Tc,
		Ru,
		Rh,
		Pd,
		Ag,
		Cd,
		In,
		Sn,
		Sb,
		Te,
		I,
		Xe,
		Cs,
		Ba,
		La,
		Ce,
		Pr,
		Nd,
		Pm,
		Sm,
		Eu,
		Gd,
		Tb,
		Dy,
		Ho,
		Er,
		Tm,
		Yb,
		Lu,
		Hf,
		Ta,
		W,
		Re,
		Os,
		Ir,
		Pt,
		Au,
		Hg,
		Tl,
		Pb,
		Bi,
		Po,
		At,
		Rn,
		Fr,
		Ra,
		Ac,
		Th,
		Pa,
		U,
		Np,
		Pu,
		Am,
		Cm,
		Bk,
		Cf,
		Es,
		Fm,
		Md,
		No,
		Lr,
		Rf,
		Db,
		Sg,
		Bh,
		Hs,
		Mt,
		Ds,
		Rg,
		Cn,
		Nh,
		Fl,
		Mc,
		Lv,
		Ts,
		Og,
		)

# ELEMENTS = Elements(
# H,                                                                                                                          He,
# Li, Be,                                                                                                 B,  C,  N,  O,  F,  Ne,
# Na, Mg,                                                                                                 Al, Si, P,  S,  Cl, Ar,
# K,  Ca,                                                         Sc, Ti, V,  Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Br, Kr,
# Rb, Sr,                                                         Y,  Zr, Nb, Mo, Tc, Ru, Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I,  Xe,
# Cs, Ba, La, Ce, Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf, Ta, W,  Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Po, At, Rn,
# Fr, Ra, Ac, Th, Pa, U,  Np, Pu, Am, Cm, Bk, Cf, Es, Fm, Md, No, Lr, Rf, Db, Sg, Bh, Hs, Mt, Ds, Rg, Cn, Nh, Fl, Mc, Lv, Ts, Og,
# )

alternate_spellings: Dict[str, str] = {
		"Caesium": "Cesium",  # AmE
		"Aluminium": "Aluminum",  # AmE
		"Sulfur": "Sulphur",  # Not IUPAC and not etymologically correct, but widely used in BrE
		}

for symbol, spelling in alternate_spellings.items():
	ELEMENTS.add_alternate_spelling(ELEMENTS[symbol], spelling)

for element in [D, T]:
	ELEMENTS.add_alternate_spelling(element, element.name)
	ELEMENTS._dict[element.symbol] = element
	# ELEMENTS._list.append(element)
