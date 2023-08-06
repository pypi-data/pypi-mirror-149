#!/usr/bin/env python3
#
#  actinides.py
r"""
Actinides (or actinoids) in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: Ac

	:class:`~chemistry_tools.elements.classes.Element` representing Actinium

.. data:: Th

	:class:`~chemistry_tools.elements.classes.Element` representing Thorium

.. data:: Pa

	:class:`~chemistry_tools.elements.classes.Element` representing Protactinium

.. data:: U

	:class:`~chemistry_tools.elements.classes.Element` representing Uranium

.. data:: Np

	:class:`~chemistry_tools.elements.classes.Element` representing Neptunium

.. data:: Pu

	:class:`~chemistry_tools.elements.classes.Element` representing Plutonium

.. data:: Am

	:class:`~chemistry_tools.elements.classes.Element` representing Americium

.. data:: Cm

	:class:`~chemistry_tools.elements.classes.Element` representing Curium

.. data:: Bk

	:class:`~chemistry_tools.elements.classes.Element` representing Berkelium

.. data:: Cf

	:class:`~chemistry_tools.elements.classes.Element` representing Californium

.. data:: Es

	:class:`~chemistry_tools.elements.classes.Element` representing Einsteinium

.. data:: Fm

	:class:`~chemistry_tools.elements.classes.Element` representing Fermium

.. data:: Md

	:class:`~chemistry_tools.elements.classes.Element` representing Mendelevium

.. data:: No

	:class:`~chemistry_tools.elements.classes.Element` representing Nobelium

.. data:: Lr

	:class:`~chemistry_tools.elements.classes.Element` representing Lawrencium

.. raw:: latex

	\end{multicols}
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
#  Isotope data from http://www.nist.gov/pml/data/comp.cfm .

# this package
from . import classes

__all__ = ("Ac", "Th", "Pa", 'U', "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

Element = classes.Element

Ac = Element(
		89,
		"Ac",
		"Actinium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=227.0278,
		eleneg=1.1,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=3470.0,
		tmelt=1324.0,
		density=10.07,
		eleconfig="[Rn] 6d 7s2",
		oxistates="3*",
		ionenergy=(5.17, 12.1),
		isotopes={
				206: (206.0145, 0.0),
				207: (207.01195, 0.0),
				208: (208.01155, 0.0),
				209: (209.00949, 0.0),
				210: (210.00944, 0.0),
				211: (211.00773, 0.0),
				212: (212.00781, 0.0),
				213: (213.00661, 0.0),
				214: (214.006902, 0.0),
				215: (215.006454, 0.0),
				216: (216.00872, 0.0),
				217: (217.009347, 0.0),
				218: (218.01164, 0.0),
				219: (219.01242, 0.0),
				220: (220.014763, 0.0),
				221: (221.01559, 0.0),
				222: (222.017844, 0.0),
				223: (223.019137, 0.0),
				224: (224.021723, 0.0),
				225: (225.02323, 0.0),
				226: (226.026098, 0.0),
				227: (227.0277521, 0.0),
				228: (228.0310211, 0.0),
				229: (229.03302, 0.0),
				230: (230.03629, 0.0),
				231: (231.03856, 0.0),
				232: (232.04203, 0.0),
				233: (233.04455, 0.0),
				234: (234.04842, 0.0),
				235: (235.05123, 0.0),
				236: (236.0553, 0.0),
				},
		description=(
				"Silvery radioactive metallic element, belongs to group 3 of the "
				"periodic table. The most stable isotope, Ac-227, has a half-life of "
				"217 years. Ac-228 (half-life of 6.13 hours) also occurs in nature. "
				"There are 22 other artificial isotopes, all radioactive and having "
				"very short half-lives. Chemistry similar to lanthanumpy. Used as a "
				"source of alpha particles. Discovered by A. Debierne in 1899."
				)
		)

Th = Element(
		90,
		"Th",
		"Thorium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=232.0377,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=1.65,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=5060.0,
		tmelt=2028.0,
		density=11.72,
		eleconfig="[Rn] 6d2 7s2",
		oxistates="4*",
		ionenergy=(6.3067, 11.5, 20.0, 28.8),
		isotopes={
				209: (209.01772, 0.0),
				210: (210.015075, 0.0),
				211: (211.01493, 0.0),
				212: (212.01298, 0.0),
				213: (213.01301, 0.0),
				214: (214.0115, 0.0),
				215: (215.01173, 0.0),
				216: (216.011062, 0.0),
				217: (217.013114, 0.0),
				218: (218.013284, 0.0),
				219: (219.01554, 0.0),
				220: (220.015748, 0.0),
				221: (221.018184, 0.0),
				222: (222.018468, 0.0),
				223: (223.020811, 0.0),
				224: (224.021467, 0.0),
				225: (225.023951, 0.0),
				226: (226.024903, 0.0),
				227: (227.0277041, 0.0),
				228: (228.0287411, 0.0),
				229: (229.031762, 0.0),
				230: (230.0331338, 0.0),
				231: (231.0363043, 0.0),
				232: (232.0380553, 1.0),
				233: (233.0415818, 0.0),
				234: (234.043601, 0.0),
				235: (235.04751, 0.0),
				236: (236.04987, 0.0),
				237: (237.05389, 0.0),
				238: (238.0565, 0.0),
				},
		description=(
				"Grey radioactive metallic element. Belongs to actinoids. Found in "
				"monazite sand in Brazil, India and the US. Thorium-232 has a "
				"half-life of 1.39x10^10 years. Can be used as a nuclear fuel for "
				"breeder reactors. Thorium-232 captures slow Neutrons and breeds "
				"uranium-233. Discovered by Jons J. Berzelius in 1829."
				)
		)

Pa = Element(
		91,
		"Pa",
		"Protactinium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=231.03588,
		eleneg=1.5,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=4300.0,
		tmelt=1845.0,
		density=15.37,
		eleconfig="[Rn] 5f2 6d 7s2",
		oxistates="5*, 4",
		ionenergy=(5.89, ),
		isotopes={
				212: (212.0232, 0.0),
				213: (213.02111, 0.0),
				214: (214.02092, 0.0),
				215: (215.01919, 0.0),
				216: (216.01911, 0.0),
				217: (217.01832, 0.0),
				218: (218.020042, 0.0),
				219: (219.01988, 0.0),
				220: (220.02188, 0.0),
				221: (221.02188, 0.0),
				222: (222.02374, 0.0),
				223: (223.02396, 0.0),
				224: (224.025626, 0.0),
				225: (225.02613, 0.0),
				226: (226.027948, 0.0),
				227: (227.028805, 0.0),
				228: (228.031051, 0.0),
				229: (229.0320968, 0.0),
				230: (230.034541, 0.0),
				231: (231.035884, 1.0),
				232: (232.038592, 0.0),
				233: (233.0402473, 0.0),
				234: (234.043308, 0.0),
				235: (235.04544, 0.0),
				236: (236.04868, 0.0),
				237: (237.05115, 0.0),
				238: (238.0545, 0.0),
				239: (239.05726, 0.0),
				240: (240.06098, 0.0),
				},
		description=(
				"Radioactive metallic element, belongs to the actinoids. The most "
				"stable isotope, Pa-231 has a half-life of 2.43*10^4 years. At least "
				"10 other radioactive isotopes are known. No practical applications "
				"are known. Discovered in 1917 by Lise Meitner and Otto Hahn."
				)
		)
U = Element(
		92,
		'U',
		"Uranium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=238.02891,
		eleneg=1.38,
		eleaffin=0.0,
		covrad=1.42,
		atmrad=0.0,
		vdwrad=1.86,
		tboil=4407.0,
		tmelt=1408.0,
		density=18.97,
		eleconfig="[Rn] 5f3 6d 7s2",
		oxistates="6*, 5, 4, 3",
		ionenergy=(6.1941, ),
		isotopes={
				217: (217.02437, 0.0),
				218: (218.02354, 0.0),
				219: (219.02492, 0.0),
				220: (220.02472, 0.0),
				221: (221.0264, 0.0),
				222: (222.02609, 0.0),
				223: (223.02774, 0.0),
				224: (224.027605, 0.0),
				225: (225.029391, 0.0),
				226: (226.029339, 0.0),
				227: (227.031156, 0.0),
				228: (228.031374, 0.0),
				229: (229.033506, 0.0),
				230: (230.03394, 0.0),
				231: (231.036294, 0.0),
				232: (232.0371562, 0.0),
				233: (233.0396352, 0.0),
				234: (234.0409521, 5.4e-05),
				235: (235.0439299, 0.007204),
				236: (236.045568, 0.0),
				237: (237.0487302, 0.0),
				238: (238.0507882, 0.992742),
				239: (239.0542933, 0.0),
				240: (240.056592, 0.0),
				241: (241.06033, 0.0),
				242: (242.06293, 0.0),
				},
		description=(
				"White radioactive metallic element belonging to the actinoids. "
				"Three natural isotopes, U-238, U-235 and U-234. Uranium-235 is used "
				"as the fuel for nuclear reactors and weapons. Discovered by Martin "
				"H. Klaproth in 1789."
				)
		)

Np = Element(
		93,
		"Np",
		"Neptunium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=237.0482,
		eleneg=1.36,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=4175.0,
		tmelt=912.0,
		density=20.48,
		eleconfig="[Rn] 5f4 6d 7s2",
		oxistates="6, 5*, 4, 3",
		ionenergy=(6.2657, ),
		isotopes={
				225: (225.03391, 0.0),
				226: (226.03515, 0.0),
				227: (227.03496, 0.0),
				228: (228.03618, 0.0),
				229: (229.03626, 0.0),
				230: (230.03783, 0.0),
				231: (231.03825, 0.0),
				232: (232.04011, 0.0),
				233: (233.04074, 0.0),
				234: (234.042895, 0.0),
				235: (235.0440633, 0.0),
				236: (236.04657, 0.0),
				237: (237.0481734, 0.0),
				238: (238.0509464, 0.0),
				239: (239.052939, 0.0),
				240: (240.056162, 0.0),
				241: (241.05825, 0.0),
				242: (242.06164, 0.0),
				243: (243.06428, 0.0),
				244: (244.06785, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element, belongs to the "
				"actinoids. Np-237, the most stable isotope, has a half-life of "
				"2.2*10^6 years and is a by product of nuclear reactors. The other "
				"known isotopes have mass numbers 229 through 236, and 238 through "
				"241. Np-236 has a half-life of 5*10^3 years. First produced by "
				"Edwin M. McMillan and P.H. Abelson in 1940."
				)
		)

Pu = Element(
		94,
		"Pu",
		"Plutonium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=244.0642,
		eleneg=1.28,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=3505.0,
		tmelt=913.0,
		density=19.74,
		eleconfig="[Rn] 5f6 7s2",
		oxistates="6, 5, 4*, 3",
		ionenergy=(6.026, ),
		isotopes={
				228: (228.03874, 0.0),
				229: (229.04015, 0.0),
				230: (230.03965, 0.0),
				231: (231.041101, 0.0),
				232: (232.041187, 0.0),
				233: (233.043, 0.0),
				234: (234.043317, 0.0),
				235: (235.045286, 0.0),
				236: (236.046058, 0.0),
				237: (237.0484097, 0.0),
				238: (238.0495599, 0.0),
				239: (239.0521634, 0.0),
				240: (240.0538135, 0.0),
				241: (241.0568515, 0.0),
				242: (242.0587426, 0.0),
				243: (243.062003, 0.0),
				244: (244.064204, 0.0),
				245: (245.067747, 0.0),
				246: (246.070205, 0.0),
				247: (247.07407, 0.0),
				},
		description=(
				"Dense silvery radioactive metallic transuranic element, belongs to "
				"the actinoids. Pu-244 is the most stable isotope with a half-life "
				"of 7.6*10^7 years. Thirteen isotopes are known. Pu-239 is the most "
				"important, it undergoes nuclear fission with slow neutrons and is "
				"hence important to nuclear weapons and reactors. Plutonium "
				"production is monitored down to the gram to prevent military "
				"misuse. First produced by Gleen T. Seaborg, Edwin M. McMillan, J.W. "
				"Kennedy and A.C. Wahl in 1940."
				)
		)

Am = Element(
		95,
		"Am",
		"Americium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=243.0614,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=2880.0,
		tmelt=1449.0,
		density=13.67,
		eleconfig="[Rn] 5f7 7s2",
		oxistates="6, 5, 4, 3*",
		ionenergy=(5.9738, ),
		isotopes={
				231: (231.04556, 0.0),
				232: (232.04659, 0.0),
				233: (233.04635, 0.0),
				234: (234.04781, 0.0),
				235: (235.04795, 0.0),
				236: (236.04958, 0.0),
				237: (237.05, 0.0),
				238: (238.05198, 0.0),
				239: (239.0530245, 0.0),
				240: (240.0553, 0.0),
				241: (241.0568291, 0.0),
				242: (242.0595492, 0.0),
				243: (243.0613811, 0.0),
				244: (244.0642848, 0.0),
				245: (245.066452, 0.0),
				246: (246.069775, 0.0),
				247: (247.07209, 0.0),
				248: (248.07575, 0.0),
				249: (249.07848, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element, belongs to the "
				"actinoids. Ten known isotopes. Am-243 is the most stable isotope, "
				"with a half-life of 7.95*10^3 years. Discovered by Glenn T. Seaborg "
				"and associates in 1945, it was obtained by bombarding Uranium-238 "
				"with alpha particles."
				)
		)

Cm = Element(
		96,
		"Cm",
		"Curium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=247.0704,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1620.0,
		density=13.51,
		eleconfig="[Rn] 5f7 6d 7s2",
		oxistates="4, 3*",
		ionenergy=(5.9914, ),
		isotopes={
				233: (233.05077, 0.0),
				234: (234.05016, 0.0),
				235: (235.05143, 0.0),
				236: (236.05141, 0.0),
				237: (237.0529, 0.0),
				238: (238.05303, 0.0),
				239: (239.05496, 0.0),
				240: (240.0555295, 0.0),
				241: (241.057653, 0.0),
				242: (242.0588358, 0.0),
				243: (243.0613891, 0.0),
				244: (244.0627526, 0.0),
				245: (245.0654912, 0.0),
				246: (246.0672237, 0.0),
				247: (247.070354, 0.0),
				248: (248.072349, 0.0),
				249: (249.075953, 0.0),
				250: (250.078357, 0.0),
				251: (251.082285, 0.0),
				252: (252.08487, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element. Belongs to actinoid "
				"series. Nine known isotopes, Cm-247 has a half-life of 1.64*10^7 "
				"years. First identified by Glenn T. Seaborg and associates in 1944, "
				"first produced by L.B. Werner and I. Perlman in 1947 by bombarding "
				"americium-241 with Neutrons. Named for Marie Curie."
				)
		)

Bk = Element(
		97,
		"Bk",
		"Berkelium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=247.0703,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1258.0,
		density=13.25,
		eleconfig="[Rn] 5f9 7s2",
		oxistates="4, 3*",
		ionenergy=(6.1979, ),
		isotopes={
				235: (235.05658, 0.0),
				236: (236.05733, 0.0),
				237: (237.057, 0.0),
				238: (238.05828, 0.0),
				239: (239.05828, 0.0),
				240: (240.05976, 0.0),
				241: (241.06023, 0.0),
				242: (242.06198, 0.0),
				243: (243.063008, 0.0),
				244: (244.065181, 0.0),
				245: (245.0663616, 0.0),
				246: (246.06867, 0.0),
				247: (247.070307, 0.0),
				248: (248.07309, 0.0),
				249: (249.0749867, 0.0),
				250: (250.078317, 0.0),
				251: (251.08076, 0.0),
				252: (252.08431, 0.0),
				253: (253.08688, 0.0),
				254: (254.0906, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element. Belongs to actinoid "
				"series. Eight known isotopes, the most common Bk-247, has a "
				"half-life of 1.4*10^3 years. First produced by Glenn T. Seaborg and "
				"associates in 1949 by bombarding americium-241 with alpha "
				"particles."
				)
		)

Cf = Element(
		98,
		"Cf",
		"Californium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=251.0796,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1172.0,
		density=15.1,
		eleconfig="[Rn] 5f10 7s2",
		oxistates="4, 3*",
		ionenergy=(6.2817, ),
		isotopes={
				237: (237.06207, 0.0),
				238: (238.06141, 0.0),
				239: (239.06242, 0.0),
				240: (240.0623, 0.0),
				241: (241.06373, 0.0),
				242: (242.0637, 0.0),
				243: (243.06543, 0.0),
				244: (244.066001, 0.0),
				245: (245.068049, 0.0),
				246: (246.0688053, 0.0),
				247: (247.071001, 0.0),
				248: (248.072185, 0.0),
				249: (249.0748535, 0.0),
				250: (250.0764061, 0.0),
				251: (251.079587, 0.0),
				252: (252.081626, 0.0),
				253: (253.085133, 0.0),
				254: (254.087323, 0.0),
				255: (255.09105, 0.0),
				256: (256.09344, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element. Belongs to actinoid "
				"series. Cf-251 has a half life of about 700 years. Nine isotopes "
				"are known. Cf-252 is an intense Neutron source, which makes it an "
				"intense Neutron source and gives it a use in Neutron activation "
				"analysis and a possible use as a radiation source in medicine. "
				"First produced by Glenn T. Seaborg and associates in 1950."
				)
		)

Es = Element(
		99,
		"Es",
		"Einsteinium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=252.083,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1130.0,
		density=0.0,
		eleconfig="[Rn] 5f11 7s2",
		oxistates="3*",
		ionenergy=(6.42, ),
		isotopes={
				240: (240.06892, 0.0),
				241: (241.06854, 0.0),
				242: (242.06975, 0.0),
				243: (243.06955, 0.0),
				244: (244.07088, 0.0),
				245: (245.07132, 0.0),
				246: (246.0729, 0.0),
				247: (247.07366, 0.0),
				248: (248.07547, 0.0),
				249: (249.07641, 0.0),
				250: (250.07861, 0.0),
				251: (251.079992, 0.0),
				252: (252.08298, 0.0),
				253: (253.0848247, 0.0),
				254: (254.088022, 0.0),
				255: (255.090273, 0.0),
				256: (256.0936, 0.0),
				257: (257.09598, 0.0),
				258: (258.09952, 0.0),
				},
		description=(
				"Appearance is unknown, however it is most probably metallic and "
				"silver or gray in color. Radioactive metallic transuranic element "
				"belonging to the actinoids. Es-254 has the longest half-life of the "
				"eleven known isotopes at 270 days. First identified by Albert "
				"Ghiorso and associates in the debris of the 1952 hydrogen bomb "
				"explosion. In 1961 the first microgram quantities of Es-232 were "
				"separated. While einsteinium never exists naturally, if a "
				"sufficient amount was assembled, it would pose a radiation hazard."
				)
		)

Fm = Element(
		100,
		"Fm",
		"Fermium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=257.0951,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1800.0,
		density=0.0,
		eleconfig="[Rn] 5f12 7s2",
		oxistates="3*",
		ionenergy=(6.5, ),
		isotopes={
				242: (242.07343, 0.0),
				243: (243.07435, 0.0),
				244: (244.07408, 0.0),
				245: (245.07539, 0.0),
				246: (246.0753, 0.0),
				247: (247.07685, 0.0),
				248: (248.077195, 0.0),
				249: (249.07903, 0.0),
				250: (250.079521, 0.0),
				251: (251.081575, 0.0),
				252: (252.082467, 0.0),
				253: (253.085185, 0.0),
				254: (254.0868542, 0.0),
				255: (255.089962, 0.0),
				256: (256.091773, 0.0),
				257: (257.095105, 0.0),
				258: (258.09708, 0.0),
				259: (259.1006, 0.0),
				260: (260.10268, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element, belongs to the "
				"actinoids. Ten known isotopes, most stable is Fm-257 with a "
				"half-life of 10 days. First identified by Albert Ghiorso and "
				"associates in the debris of the first hydrogen-bomb explosion in "
				"1952."
				)
		)

Md = Element(
		101,
		"Md",
		"Mendelevium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=258.0984,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1100.0,
		density=0.0,
		eleconfig="[Rn] 5f13 7s2",
		oxistates="3*",
		ionenergy=(6.58, ),
		isotopes={
				245: (245.08083, 0.0),
				246: (246.08189, 0.0),
				247: (247.08164, 0.0),
				248: (248.08282, 0.0),
				249: (249.08301, 0.0),
				250: (250.08442, 0.0),
				251: (251.08484, 0.0),
				252: (252.08656, 0.0),
				253: (253.08728, 0.0),
				254: (254.08966, 0.0),
				255: (255.091083, 0.0),
				256: (256.09406, 0.0),
				257: (257.095541, 0.0),
				258: (258.098431, 0.0),
				259: (259.10051, 0.0),
				260: (260.10365, 0.0),
				261: (261.10572, 0.0),
				262: (262.10887, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element. Belongs to the actinoid "
				"series. Only known isotope, Md-256 has a half-life of 1.3 hours. "
				"First identified by Glenn T. Seaborg, Albert Ghiorso and associates "
				"in 1955. Alternative name Unnilunium has been proposed. Named after "
				"the 'inventor' of the periodic table, Dmitri Mendeleev."
				)
		)

No = Element(
		102,
		"No",
		"Nobelium",
		group=3,
		period=7,
		block='f',
		series=10,
		mass=259.101,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1100.0,
		density=0.0,
		eleconfig="[Rn] 5f14 7s2",
		oxistates="3, 2*",
		ionenergy=(6.65, ),
		isotopes={
				248: (248.0866, 0.0),
				249: (249.08783, 0.0),
				250: (250.08751, 0.0),
				251: (251.08901, 0.0),
				252: (252.088977, 0.0),
				253: (253.09068, 0.0),
				254: (254.090955, 0.0),
				255: (255.093241, 0.0),
				256: (256.094283, 0.0),
				257: (257.096877, 0.0),
				258: (258.09821, 0.0),
				259: (259.10103, 0.0),
				260: (260.10264, 0.0),
				261: (261.10575, 0.0),
				262: (262.1073, 0.0),
				263: (263.11055, 0.0),
				264: (264.11235, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element, belongs to the "
				"actinoids. Seven known isotopes exist, the most stable being No-254 "
				"with a half-life of 255 seconds. First identified with certainty by "
				"Albert Ghiorso and Glenn T. Seaborg in 1966. Unnilbium has been "
				"proposed as an alternative name."
				)
		)

Lr = Element(
		103,
		"Lr",
		"Lawrencium",
		group=3,
		period=7,
		block='d',
		series=10,
		mass=262.1096,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=1900.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d 7s2",
		oxistates="3*",
		ionenergy=(4.9, ),
		isotopes={
				251: (251.09436, 0.0),
				252: (252.09537, 0.0),
				253: (253.09521, 0.0),
				254: (254.09645, 0.0),
				255: (255.09668, 0.0),
				256: (256.09863, 0.0),
				257: (257.09956, 0.0),
				258: (258.10181, 0.0),
				259: (259.1029, 0.0),
				260: (260.1055, 0.0),
				261: (261.10688, 0.0),
				262: (262.10963, 0.0),
				263: (263.11129, 0.0),
				264: (264.11404, 0.0),
				265: (265.11584, 0.0),
				266: (266.11931, 0.0),
				},
		description=(
				"Appearance unknown, however it is most likely silvery-white or "
				"grey and metallic. Lawrencium is a synthetic rare-earth metal. "
				"There are eight known radioisotopes, the most stable being Lr-262 "
				"with a half-life of 3.6 hours. Due to the short half-life of "
				"lawrencium, and its radioactivity, there are no known uses for it. "
				"Identified by Albert Ghiorso in 1961 at Berkeley. It was produced "
				"by bombarding californium with boron ions. The name is temporary "
				"IUPAC nomenclature, the origin of the name comes from Ernest O. "
				"Lawrence, the inventor of the cyclotron. If sufficient amounts of "
				"lawrencium were produced, it would pose a radiation hazard."
				)
		)
