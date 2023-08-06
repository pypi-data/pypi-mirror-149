#!/usr/bin/env python3
#
#  transition_metals.py
r"""
Transition Metals block in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: Sc

	:class:`~chemistry_tools.elements.classes.Element` representing Scandium

.. data:: Ti

	:class:`~chemistry_tools.elements.classes.Element` representing Titanium

.. data:: V

	:class:`~chemistry_tools.elements.classes.Element` representing Vanadium

.. data:: Cr

	:class:`~chemistry_tools.elements.classes.Element` representing Chromium

.. data:: Mn

	:class:`~chemistry_tools.elements.classes.Element` representing Manganese

.. data:: Fe

	:class:`~chemistry_tools.elements.classes.Element` representing Iron

.. data:: Co

	:class:`~chemistry_tools.elements.classes.Element` representing Cobalt

.. data:: Ni

	:class:`~chemistry_tools.elements.classes.Element` representing Nickel

.. data:: Cu

	:class:`~chemistry_tools.elements.classes.Element` representing Copper

.. data:: Zn

	:class:`~chemistry_tools.elements.classes.Element` representing Zinc

.. data:: Y

	:class:`~chemistry_tools.elements.classes.Element` representing Yttrium

.. data:: Zr

	:class:`~chemistry_tools.elements.classes.Element` representing Zirconium

.. data:: Nb

	:class:`~chemistry_tools.elements.classes.Element` representing Niobium

.. data:: Mo

	:class:`~chemistry_tools.elements.classes.Element` representing Molybdenum

.. data:: Tc

	:class:`~chemistry_tools.elements.classes.Element` representing Technetium

.. data:: Ru

	:class:`~chemistry_tools.elements.classes.Element` representing Ruthenium

.. data:: Rh

	:class:`~chemistry_tools.elements.classes.Element` representing Rhodium

.. data:: Pd

	:class:`~chemistry_tools.elements.classes.Element` representing Palladium

.. data:: Ag

	:class:`~chemistry_tools.elements.classes.Element` representing Silver

.. data:: Cd

	:class:`~chemistry_tools.elements.classes.Element` representing Cadmium

.. data:: Hf

	:class:`~chemistry_tools.elements.classes.Element` representing Hafnium

.. data:: Ta

	:class:`~chemistry_tools.elements.classes.Element` representing Tantalum

.. data:: W

	:class:`~chemistry_tools.elements.classes.Element` representing Tungsten

.. data:: Re

	:class:`~chemistry_tools.elements.classes.Element` representing Rhenium

.. data:: Os

	:class:`~chemistry_tools.elements.classes.Element` representing Osmium

.. data:: Ir

	:class:`~chemistry_tools.elements.classes.Element` representing Iridium

.. data:: Pt

	:class:`~chemistry_tools.elements.classes.Element` representing Platinum

.. data:: Au

	:class:`~chemistry_tools.elements.classes.Element` representing Gold

.. data:: Hg

	:class:`~chemistry_tools.elements.classes.Element` representing Mercury

.. data:: Rf

	:class:`~chemistry_tools.elements.classes.Element` representing Rutherfordium

.. data:: Db

	:class:`~chemistry_tools.elements.classes.Element` representing Dubnium

.. data:: Sg

	:class:`~chemistry_tools.elements.classes.Element` representing Seaborgium

.. data:: Bh

	:class:`~chemistry_tools.elements.classes.Element` representing Bohrium

.. data:: Hs

	:class:`~chemistry_tools.elements.classes.Element` representing Hassium

.. data:: Mt

	:class:`~chemistry_tools.elements.classes.Element` representing Meitnerium

.. data:: Ds

	:class:`~chemistry_tools.elements.classes.Element` representing Darmstadtium

.. data:: Rg

	:class:`~chemistry_tools.elements.classes.Element` representing Roentgenium

.. data:: Cn

	:class:`~chemistry_tools.elements.classes.Element` representing Roentgenium

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
from .classes import Element

__all__ = (
		"Sc",
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

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

Sc = Element(
		21,
		"Sc",
		"Scandium",
		group=3,
		period=4,
		block='d',
		series=8,
		mass=44.955908,
		eleneg=1.36,
		eleaffin=0.188,
		covrad=1.44,
		atmrad=2.09,
		vdwrad=0.0,
		tboil=3109.0,
		tmelt=1814.0,
		density=2.99,
		eleconfig="[Ar] 3d 4s2",
		oxistates="3*",
		ionenergy=(
				6.5615,
				12.8,
				24.76,
				73.47,
				91.66,
				110.1,
				138.0,
				158.7,
				180.02,
				225.32,
				249.8,
				685.89,
				755.47,
				829.79,
				926.0,
				),
		isotopes={
				36: (36.01492, 0.0),
				37: (37.00305, 0.0),
				38: (37.9947, 0.0),
				39: (38.98479, 0.0),
				40: (39.977967, 0.0),
				41: (40.96925113, 0.0),
				42: (41.96551643, 0.0),
				43: (42.9611507, 0.0),
				44: (43.9594028, 0.0),
				45: (44.9559119, 1.0),
				46: (45.9551719, 0.0),
				47: (46.9524075, 0.0),
				48: (47.952231, 0.0),
				49: (48.950024, 0.0),
				50: (49.952188, 0.0),
				51: (50.953603, 0.0),
				52: (51.95668, 0.0),
				53: (52.95961, 0.0),
				54: (53.96326, 0.0),
				55: (54.96824, 0.0),
				56: (55.97287, 0.0),
				57: (56.97779, 0.0),
				58: (57.98371, 0.0),
				59: (58.98922, 0.0),
				60: (59.99571, 0.0),
				},
		description=(
				"Rare soft silvery metallic element belonging to group 3 of the "
				"periodic table. There are ten isotopes, nine of which are "
				"radioactive and have short half-lives. Predicted in 1869 by "
				"Mendeleev, isolated by Nilson in 1879."
				)
		)

Ti = Element(
		22,
		"Ti",
		"Titanium",
		group=4,
		period=4,
		block='d',
		series=8,
		mass=47.867,
		eleneg=1.54,
		eleaffin=0.084,
		covrad=1.32,
		atmrad=2.0,
		vdwrad=0.0,
		tboil=3560.0,
		tmelt=1935.0,
		density=4.51,
		eleconfig="[Ar] 3d2 4s2",
		oxistates="4*, 3",
		ionenergy=(
				6.8281,
				13.58,
				27.491,
				43.266,
				99.22,
				119.36,
				140.8,
				168.5,
				193.5,
				215.91,
				265.23,
				291.497,
				787.33,
				861.33,
				),
		isotopes={
				38: (38.00977, 0.0),
				39: (39.00161, 0.0),
				40: (39.9905, 0.0),
				41: (40.98315, 0.0),
				42: (41.973031, 0.0),
				43: (42.968522, 0.0),
				44: (43.9596901, 0.0),
				45: (44.9581256, 0.0),
				46: (45.9526316, 0.0825),
				47: (46.9517631, 0.0744),
				48: (47.9479463, 0.7372),
				49: (48.94787, 0.0541),
				50: (49.9447912, 0.0518),
				51: (50.946615, 0.0),
				52: (51.946897, 0.0),
				53: (52.94973, 0.0),
				54: (53.95105, 0.0),
				55: (54.95527, 0.0),
				56: (55.9582, 0.0),
				57: (56.96399, 0.0),
				58: (57.96697, 0.0),
				59: (58.97293, 0.0),
				60: (59.97676, 0.0),
				61: (60.9832, 0.0),
				62: (61.98749, 0.0),
				63: (62.99442, 0.0),
				},
		description=(
				"White metallic transition element. Occurs in numerous minerals. "
				"Used in strong, light corrosion-resistant alloys. Forms a passive "
				"oxide coating when exposed to air. First discovered by Gregor in "
				"1789."
				)
		)

V = Element(
		23,
		'V',
		"Vanadium",
		group=5,
		period=4,
		block='d',
		series=8,
		mass=50.9415,
		eleneg=1.63,
		eleaffin=0.525,
		covrad=1.22,
		atmrad=1.92,
		vdwrad=0.0,
		tboil=3650.0,
		tmelt=2163.0,
		density=6.09,
		eleconfig="[Ar] 3d3 4s2",
		oxistates="5*, 4, 3, 2, 0",
		ionenergy=(
				6.7462,
				14.65,
				29.31,
				46.707,
				65.23,
				128.12,
				150.17,
				173.7,
				205.8,
				230.5,
				255.04,
				308.25,
				336.267,
				895.58,
				974.02,
				),
		isotopes={
				40: (40.01109, 0.0),
				41: (40.99978, 0.0),
				42: (41.99123, 0.0),
				43: (42.98065, 0.0),
				44: (43.97411, 0.0),
				45: (44.965776, 0.0),
				46: (45.9602005, 0.0),
				47: (46.9549089, 0.0),
				48: (47.9522537, 0.0),
				49: (48.9485161, 0.0),
				50: (49.9471585, 0.0025),
				51: (50.9439595, 0.9975),
				52: (51.9447755, 0.0),
				53: (52.944338, 0.0),
				54: (53.94644, 0.0),
				55: (54.94723, 0.0),
				56: (55.95053, 0.0),
				57: (56.95256, 0.0),
				58: (57.95683, 0.0),
				59: (58.96021, 0.0),
				60: (59.96503, 0.0),
				61: (60.96848, 0.0),
				62: (61.97378, 0.0),
				63: (62.97755, 0.0),
				64: (63.98347, 0.0),
				65: (64.98792, 0.0),
				},
		description=(
				"Soft and ductile, bright white metal. Good resistance to corrosion "
				"by alkalis, sulphuric and hydrochloric acid. It oxidizes readily "
				"about 933K. There are two naturally occurring isotopes of vanadium, "
				"and 5 radioisotopes, V-49 having the longest half-life at 337 days. "
				"Vanadium has nuclear applications, the foil is used in cladding "
				"titanium to steel, and vanadium-gallium tape is used to produce a "
				"superconductive magnet. Originally discovered by Andres Manuel del "
				"Rio of Mexico City in 1801. His discovery went unheeded, however, "
				"and in 1820, Nils Gabriel Sefstron of Sweden rediscovered it. "
				"Metallic vanadium was isolated by Henry Enfield Roscoe in 1867. The "
				"name vanadium comes from Vanadis, a goddess of Scandinavian "
				"mythology. Silvery-white metallic transition element. Vanadium is "
				"essential to Ascidians. Rats and chickens are also known to require "
				"it. Metal powder is a fire hazard, and vanadium compounds should be "
				"considered highly toxic. May cause lung cancer if inhaled."
				)
		)

Cr = Element(
		24,
		"Cr",
		"Chromium",
		group=6,
		period=4,
		block='d',
		series=8,
		mass=51.9961,
		eleneg=1.66,
		eleaffin=0.67584,
		covrad=1.18,
		atmrad=1.85,
		vdwrad=0.0,
		tboil=2945.0,
		tmelt=2130.0,
		density=7.14,
		eleconfig="[Ar] 3d5 4s",
		oxistates="6, 3*, 2, 0",
		ionenergy=(
				6.7665,
				16.5,
				30.96,
				49.1,
				69.3,
				90.56,
				161.1,
				184.7,
				209.3,
				244.4,
				270.8,
				298.0,
				355.0,
				384.3,
				1010.64,
				),
		isotopes={
				42: (42.00643, 0.0),
				43: (42.99771, 0.0),
				44: (43.98555, 0.0),
				45: (44.97964, 0.0),
				46: (45.968359, 0.0),
				47: (46.9629, 0.0),
				48: (47.954032, 0.0),
				49: (48.9513357, 0.0),
				50: (49.9460442, 0.04345),
				51: (50.9447674, 0.0),
				52: (51.9405075, 0.83789),
				53: (52.9406494, 0.09501),
				54: (53.9388804, 0.02365),
				55: (54.9408397, 0.0),
				56: (55.9406531, 0.0),
				57: (56.943613, 0.0),
				58: (57.94435, 0.0),
				59: (58.94859, 0.0),
				60: (59.95008, 0.0),
				61: (60.95472, 0.0),
				62: (61.95661, 0.0),
				63: (62.96186, 0.0),
				64: (63.96441, 0.0),
				65: (64.97016, 0.0),
				66: (65.97338, 0.0),
				67: (66.97955, 0.0),
				},
		description=(
				"Hard silvery transition element. Used in decorative "
				"electroplating. Discovered in 1797 by Vauquelin."
				)
		)

Mn = Element(
		25,
		"Mn",
		"Manganese",
		group=7,
		period=4,
		block='d',
		series=8,
		mass=54.938044,
		eleneg=1.55,
		eleaffin=0.0,
		covrad=1.17,
		atmrad=1.79,
		vdwrad=0.0,
		tboil=2235.0,
		tmelt=1518.0,
		density=7.44,
		eleconfig="[Ar] 3d5 4s2",
		oxistates="7, 6, 4, 3, 2*, 0, -1",
		ionenergy=(
				7.434,
				15.64,
				33.667,
				51.2,
				72.4,
				95.0,
				119.27,
				196.46,
				221.8,
				248.3,
				286.0,
				314.4,
				343.6,
				404.0,
				435.3,
				1136.2,
				),
		isotopes={
				44: (44.00687, 0.0),
				45: (44.99451, 0.0),
				46: (45.98672, 0.0),
				47: (46.9761, 0.0),
				48: (47.96852, 0.0),
				49: (48.959618, 0.0),
				50: (49.9542382, 0.0),
				51: (50.9482108, 0.0),
				52: (51.9455655, 0.0),
				53: (52.9412901, 0.0),
				54: (53.9403589, 0.0),
				55: (54.9380451, 1.0),
				56: (55.9389049, 0.0),
				57: (56.9382854, 0.0),
				58: (57.93998, 0.0),
				59: (58.94044, 0.0),
				60: (59.94291, 0.0),
				61: (60.94465, 0.0),
				62: (61.94843, 0.0),
				63: (62.95024, 0.0),
				64: (63.95425, 0.0),
				65: (64.95634, 0.0),
				66: (65.96108, 0.0),
				67: (66.96414, 0.0),
				68: (67.9693, 0.0),
				69: (68.97284, 0.0),
				},
		description=(
				"Grey brittle metallic transition element. Rather electropositive, "
				"combines with some non-metals when heated. Discovered in 1774 by "
				"Scheele."
				)
		)

Fe = Element(
		26,
		"Fe",
		"Iron",
		group=8,
		period=4,
		block='d',
		series=8,
		mass=55.845,
		eleneg=1.83,
		eleaffin=0.151,
		covrad=1.17,
		atmrad=1.72,
		vdwrad=0.0,
		tboil=3023.0,
		tmelt=1808.0,
		density=7.874,
		eleconfig="[Ar] 3d6 4s2",
		oxistates="6, 3*, 2, 0, -2",
		ionenergy=(
				7.9024,
				16.18,
				30.651,
				54.8,
				75.0,
				99.0,
				125.0,
				151.06,
				235.04,
				262.1,
				290.4,
				330.8,
				361.0,
				392.2,
				457.0,
				485.5,
				1266.1,
				),
		isotopes={
				45: (45.01458, 0.0),
				46: (46.00081, 0.0),
				47: (46.99289, 0.0),
				48: (47.9805, 0.0),
				49: (48.97361, 0.0),
				50: (49.96299, 0.0),
				51: (50.95682, 0.0),
				52: (51.948114, 0.0),
				53: (52.9453079, 0.0),
				54: (53.9396105, 0.05845),
				55: (54.9382934, 0.0),
				56: (55.9349375, 0.91754),
				57: (56.935394, 0.02119),
				58: (57.9332756, 0.00282),
				59: (58.9348755, 0.0),
				60: (59.934072, 0.0),
				61: (60.936745, 0.0),
				62: (61.936767, 0.0),
				63: (62.94037, 0.0),
				64: (63.9412, 0.0),
				65: (64.94538, 0.0),
				66: (65.94678, 0.0),
				67: (66.95095, 0.0),
				68: (67.9537, 0.0),
				69: (68.95878, 0.0),
				70: (69.96146, 0.0),
				71: (70.96672, 0.0),
				72: (71.96962, 0.0),
				},
		description=(
				"Silvery malleable and ductile metallic transition element. Has "
				"nine isotopes and is the fourth most abundant element in the "
				"Earth's crust. Required by living organisms as a trace element "
				"(used in hemoglobin in humans.) Quite reactive, oxidizes in moist "
				"air, displaces hydrogen from dilute acids and combines with "
				"nonmetallic elements."
				)
		)

Co = Element(
		27,
		"Co",
		"Cobalt",
		group=9,
		period=4,
		block='d',
		series=8,
		mass=58.933194,
		eleneg=1.88,
		eleaffin=0.6633,
		covrad=1.16,
		atmrad=1.67,
		vdwrad=0.0,
		tboil=3143.0,
		tmelt=1768.0,
		density=8.89,
		eleconfig="[Ar] 3d7 4s2",
		oxistates="3, 2*, 0, -1",
		ionenergy=(
				7.881,
				17.06,
				33.5,
				51.3,
				79.5,
				102.0,
				129.0,
				157.0,
				186.13,
				276.0,
				305.0,
				336.0,
				376.0,
				411.0,
				444.0,
				512.0,
				546.8,
				1403.0,
				),
		isotopes={
				47: (47.01149, 0.0),
				48: (48.00176, 0.0),
				49: (48.98972, 0.0),
				50: (49.98154, 0.0),
				51: (50.97072, 0.0),
				52: (51.96359, 0.0),
				53: (52.954219, 0.0),
				54: (53.9484596, 0.0),
				55: (54.941999, 0.0),
				56: (55.9398393, 0.0),
				57: (56.9362914, 0.0),
				58: (57.9357528, 0.0),
				59: (58.933195, 1.0),
				60: (59.9338171, 0.0),
				61: (60.9324758, 0.0),
				62: (61.934051, 0.0),
				63: (62.933612, 0.0),
				64: (63.93581, 0.0),
				65: (64.936478, 0.0),
				66: (65.93976, 0.0),
				67: (66.94089, 0.0),
				68: (67.94487, 0.0),
				69: (68.94632, 0.0),
				70: (69.951, 0.0),
				71: (70.9529, 0.0),
				72: (71.95781, 0.0),
				73: (72.96024, 0.0),
				74: (73.96538, 0.0),
				75: (74.96833, 0.0),
				},
		description=(
				"Light grey transition element. Some meteorites contain small "
				"amounts of metallic cobalt. Generally alloyed for use. Mammals "
				"require small amounts of cobalt salts. Cobalt-60, an artificially "
				"produced radioactive isotope of Cobalt is an important radioactive "
				"tracer and cancer-treatment agent. Discovered by G. Brandt in 1737."
				)
		)

Ni = Element(
		28,
		"Ni",
		"Nickel",
		group=10,
		period=4,
		block='d',
		series=8,
		mass=58.6934,
		eleneg=1.91,
		eleaffin=1.15716,
		covrad=1.15,
		atmrad=1.62,
		vdwrad=1.63,
		tboil=3005.0,
		tmelt=1726.0,
		density=8.91,
		eleconfig="[Ar] 3d8 4s2",
		oxistates="3, 2*, 0",
		ionenergy=(
				7.6398,
				18.168,
				35.17,
				54.9,
				75.5,
				108.0,
				133.0,
				162.0,
				193.0,
				224.5,
				321.2,
				352.0,
				384.0,
				430.0,
				464.0,
				499.0,
				571.0,
				607.2,
				1547.0,
				),
		isotopes={
				48: (48.01975, 0.0),
				49: (49.00966, 0.0),
				50: (49.99593, 0.0),
				51: (50.98772, 0.0),
				52: (51.97568, 0.0),
				53: (52.96847, 0.0),
				54: (53.95791, 0.0),
				55: (54.95133, 0.0),
				56: (55.942132, 0.0),
				57: (56.9397935, 0.0),
				58: (57.9353429, 0.680769),
				59: (58.9343467, 0.0),
				60: (59.9307864, 0.262231),
				61: (60.931056, 0.011399),
				62: (61.9283451, 0.036345),
				63: (62.9296694, 0.0),
				64: (63.927966, 0.009256),
				65: (64.9300843, 0.0),
				66: (65.9291393, 0.0),
				67: (66.931569, 0.0),
				68: (67.931869, 0.0),
				69: (68.93561, 0.0),
				70: (69.9365, 0.0),
				71: (70.94074, 0.0),
				72: (71.94209, 0.0),
				73: (72.94647, 0.0),
				74: (73.94807, 0.0),
				75: (74.95287, 0.0),
				76: (75.95533, 0.0),
				77: (76.96055, 0.0),
				78: (77.96318, 0.0),
				},
		description=(
				"Malleable ductile silvery metallic transition element. Discovered "
				"by A.F. Cronstedt in 1751."
				)
		)

Cu = Element(
		29,
		"Cu",
		"Copper",
		group=11,
		period=4,
		block='d',
		series=8,
		mass=63.546,
		eleneg=1.9,
		eleaffin=1.23578,
		covrad=1.17,
		atmrad=1.57,
		vdwrad=1.4,
		tboil=2840.0,
		tmelt=1356.6,
		density=8.92,
		eleconfig="[Ar] 3d10 4s",
		oxistates="2*, 1",
		ionenergy=(
				7.7264,
				20.292,
				26.83,
				55.2,
				79.9,
				103.0,
				139.0,
				166.0,
				199.0,
				232.0,
				266.0,
				368.8,
				401.0,
				435.0,
				484.0,
				520.0,
				557.0,
				633.0,
				671.0,
				1698.0,
				),
		isotopes={
				52: (51.99718, 0.0),
				53: (52.98555, 0.0),
				54: (53.97671, 0.0),
				55: (54.96605, 0.0),
				56: (55.95856, 0.0),
				57: (56.949211, 0.0),
				58: (57.9445385, 0.0),
				59: (58.939498, 0.0),
				60: (59.937365, 0.0),
				61: (60.9334578, 0.0),
				62: (61.932584, 0.0),
				63: (62.9295975, 0.6915),
				64: (63.9297642, 0.0),
				65: (64.9277895, 0.3085),
				66: (65.9288688, 0.0),
				67: (66.9277303, 0.0),
				68: (67.9296109, 0.0),
				69: (68.9294293, 0.0),
				70: (69.9323923, 0.0),
				71: (70.9326768, 0.0),
				72: (71.9358203, 0.0),
				73: (72.936675, 0.0),
				74: (73.939875, 0.0),
				75: (74.9419, 0.0),
				76: (75.945275, 0.0),
				77: (76.94785, 0.0),
				78: (77.95196, 0.0),
				79: (78.95456, 0.0),
				80: (79.96087, 0.0),
				},
		description=(
				"Red-brown transition element. Known by the Romans as 'cuprum.' "
				"Extracted and used for thousands of years. Malleable, ductile and "
				"an excellent conductor of heat and electricity. When in moist "
				"conditions, a greenish layer forms on the outside."
				)
		)

Zn = Element(
		30,
		"Zn",
		"Zinc",
		group=12,
		period=4,
		block='d',
		series=8,
		mass=65.38,
		eleneg=1.65,
		eleaffin=0.0,
		covrad=1.25,
		atmrad=1.53,
		vdwrad=1.39,
		tboil=1180.0,
		tmelt=692.73,
		density=7.14,
		eleconfig="[Ar] 3d10 4s2",
		oxistates="2*",
		ionenergy=(
				9.3942,
				17.964,
				39.722,
				59.4,
				82.6,
				108.0,
				134.0,
				174.0,
				203.0,
				238.0,
				274.0,
				310.8,
				419.7,
				454.0,
				490.0,
				542.0,
				579.0,
				619.0,
				698.8,
				738.0,
				1856.0,
				),
		isotopes={
				54: (53.99295, 0.0),
				55: (54.98398, 0.0),
				56: (55.97238, 0.0),
				57: (56.96479, 0.0),
				58: (57.95459, 0.0),
				59: (58.94926, 0.0),
				60: (59.941827, 0.0),
				61: (60.939511, 0.0),
				62: (61.93433, 0.0),
				63: (62.9332116, 0.0),
				64: (63.9291422, 0.48268),
				65: (64.929241, 0.0),
				66: (65.9260334, 0.27975),
				67: (66.9271273, 0.04102),
				68: (67.9248442, 0.19024),
				69: (68.9265503, 0.0),
				70: (69.9253193, 0.00631),
				71: (70.927722, 0.0),
				72: (71.926858, 0.0),
				73: (72.92978, 0.0),
				74: (73.92946, 0.0),
				75: (74.93294, 0.0),
				76: (75.93329, 0.0),
				77: (76.93696, 0.0),
				78: (77.93844, 0.0),
				79: (78.94265, 0.0),
				80: (79.94434, 0.0),
				81: (80.95048, 0.0),
				82: (81.95442, 0.0),
				83: (82.96103, 0.0),
				},
		description=(
				"Blue-white metallic element. Occurs in multiple compounds "
				"naturally. Five stable isotopes are six radioactive isotopes have "
				"been found. Chemically a reactive metal, combines with oxygen and "
				"other non-metals, reacts with dilute acids to release hydrogen."
				)
		)

Y = Element(
		39,
		'Y',
		"Yttrium",
		group=3,
		period=5,
		block='d',
		series=8,
		mass=88.90584,
		eleneg=1.22,
		eleaffin=0.307,
		covrad=1.62,
		atmrad=2.27,
		vdwrad=0.0,
		tboil=3611.0,
		tmelt=1795.0,
		density=4.47,
		eleconfig="[Kr] 4d 5s2",
		oxistates="3*",
		ionenergy=(
				6.2173,
				12.24,
				20.52,
				61.8,
				77.0,
				93.0,
				116.0,
				129.0,
				146.52,
				191.0,
				206.0,
				374.0,
				),
		isotopes={
				76: (75.95845, 0.0),
				77: (76.94965, 0.0),
				78: (77.94361, 0.0),
				79: (78.93735, 0.0),
				80: (79.93428, 0.0),
				81: (80.92913, 0.0),
				82: (81.92679, 0.0),
				83: (82.92235, 0.0),
				84: (83.92039, 0.0),
				85: (84.916433, 0.0),
				86: (85.914886, 0.0),
				87: (86.9108757, 0.0),
				88: (87.9095011, 0.0),
				89: (88.9058483, 1.0),
				90: (89.9071519, 0.0),
				91: (90.907305, 0.0),
				92: (91.908949, 0.0),
				93: (92.909583, 0.0),
				94: (93.911595, 0.0),
				95: (94.912821, 0.0),
				96: (95.915891, 0.0),
				97: (96.918134, 0.0),
				98: (97.922203, 0.0),
				99: (98.924636, 0.0),
				100: (99.92776, 0.0),
				101: (100.93031, 0.0),
				102: (101.93356, 0.0),
				103: (102.93673, 0.0),
				104: (103.94105, 0.0),
				105: (104.94487, 0.0),
				106: (105.94979, 0.0),
				107: (106.95414, 0.0),
				108: (107.95948, 0.0),
				},
		description=(
				"Silvery-grey metallic element of group 3 on the periodic table. "
				"Found in uranium ores. The only natural isotope is Y-89, there are "
				"14 other artificial isotopes. Chemically resembles the lanthanoids. "
				"Stable in the air below 400 degrees, celsius. Discovered in 1828 by "
				"Friedrich Wohler."
				)
		)

Zr = Element(
		40,
		"Zr",
		"Zirconium",
		group=4,
		period=5,
		block='d',
		series=8,
		mass=91.224,
		eleneg=1.33,
		eleaffin=0.426,
		covrad=1.45,
		atmrad=2.16,
		vdwrad=0.0,
		tboil=4682.0,
		tmelt=2128.0,
		density=6.51,
		eleconfig="[Kr] 4d2 5s2",
		oxistates="4*",
		ionenergy=(6.6339, 13.13, 22.99, 34.34, 81.5),
		isotopes={
				78: (77.95523, 0.0),
				79: (78.94916, 0.0),
				80: (79.9404, 0.0),
				81: (80.93721, 0.0),
				82: (81.93109, 0.0),
				83: (82.92865, 0.0),
				84: (83.92325, 0.0),
				85: (84.92147, 0.0),
				86: (85.91647, 0.0),
				87: (86.914816, 0.0),
				88: (87.910227, 0.0),
				89: (88.90889, 0.0),
				90: (89.9047044, 0.5145),
				91: (90.9056458, 0.1122),
				92: (91.9050408, 0.1715),
				93: (92.906476, 0.0),
				94: (93.9063152, 0.1738),
				95: (94.9080426, 0.0),
				96: (95.9082734, 0.028),
				97: (96.9109531, 0.0),
				98: (97.912735, 0.0),
				99: (98.916512, 0.0),
				100: (99.91776, 0.0),
				101: (100.92114, 0.0),
				102: (101.92298, 0.0),
				103: (102.9266, 0.0),
				104: (103.92878, 0.0),
				105: (104.93305, 0.0),
				106: (105.93591, 0.0),
				107: (106.94075, 0.0),
				108: (107.94396, 0.0),
				109: (108.94924, 0.0),
				110: (109.95287, 0.0),
				},
		description=(
				"Grey-white metallic transition element. Five natural isotopes and "
				"six radioactive isotopes are known. Used in nuclear reactors for a "
				"Neutron absorber. Discovered in 1789 by Martin Klaproth, isolated "
				"in 1824 by Berzelius."
				)
		)

Nb = Element(
		41,
		"Nb",
		"Niobium",
		group=5,
		period=5,
		block='d',
		series=8,
		mass=92.90637,
		eleneg=1.6,
		eleaffin=0.893,
		covrad=1.34,
		atmrad=2.08,
		vdwrad=0.0,
		tboil=5015.0,
		tmelt=2742.0,
		density=8.58,
		eleconfig="[Kr] 4d4 5s",
		oxistates="5*, 3",
		ionenergy=(
				6.7589,
				14.32,
				25.04,
				38.3,
				50.55,
				102.6,
				125.0,
				),
		isotopes={
				81: (80.94903, 0.0),
				82: (81.94313, 0.0),
				83: (82.93671, 0.0),
				84: (83.93357, 0.0),
				85: (84.92791, 0.0),
				86: (85.92504, 0.0),
				87: (86.92036, 0.0),
				88: (87.91833, 0.0),
				89: (88.913418, 0.0),
				90: (89.911265, 0.0),
				91: (90.906996, 0.0),
				92: (91.907194, 0.0),
				93: (92.9063781, 1.0),
				94: (93.9072839, 0.0),
				95: (94.9068358, 0.0),
				96: (95.908101, 0.0),
				97: (96.9080986, 0.0),
				98: (97.910328, 0.0),
				99: (98.911618, 0.0),
				100: (99.914182, 0.0),
				101: (100.915252, 0.0),
				102: (101.91804, 0.0),
				103: (102.91914, 0.0),
				104: (103.92246, 0.0),
				105: (104.92394, 0.0),
				106: (105.92797, 0.0),
				107: (106.93031, 0.0),
				108: (107.93484, 0.0),
				109: (108.93763, 0.0),
				110: (109.94244, 0.0),
				111: (110.94565, 0.0),
				112: (111.95083, 0.0),
				113: (112.9547, 0.0),
				},
		description=(
				"Soft, ductile grey-blue metallic transition element. Used in "
				"special steels and in welded joints to increase strength. Combines "
				"with halogens and oxidizes in air at 200 degrees celsius. "
				"Discovered by Charles Hatchett in 1801 and isolated by Blomstrand "
				"in 1864. Called Columbium originally."
				)
		)

Mo = Element(
		42,
		"Mo",
		"Molybdenum",
		group=6,
		period=5,
		block='d',
		series=8,
		mass=95.95,
		eleneg=2.16,
		eleaffin=0.7472,
		covrad=1.3,
		atmrad=2.01,
		vdwrad=0.0,
		tboil=4912.0,
		tmelt=2896.0,
		density=10.28,
		eleconfig="[Kr] 4d5 5s",
		oxistates="6*, 5, 4, 3, 2, 0",
		ionenergy=(
				7.0924,
				16.15,
				27.16,
				46.4,
				61.2,
				68.0,
				126.8,
				153.0,
				),
		isotopes={
				83: (82.94874, 0.0),
				84: (83.94009, 0.0),
				85: (84.93655, 0.0),
				86: (85.9307, 0.0),
				87: (86.92733, 0.0),
				88: (87.921953, 0.0),
				89: (88.91948, 0.0),
				90: (89.913937, 0.0),
				91: (90.91175, 0.0),
				92: (91.906811, 0.1477),
				93: (92.906813, 0.0),
				94: (93.9050883, 0.0923),
				95: (94.9058421, 0.159),
				96: (95.9046795, 0.1668),
				97: (96.9060215, 0.0956),
				98: (97.9054082, 0.2419),
				99: (98.9077119, 0.0),
				100: (99.907477, 0.0967),
				101: (100.910347, 0.0),
				102: (101.910297, 0.0),
				103: (102.91321, 0.0),
				104: (103.91376, 0.0),
				105: (104.91697, 0.0),
				106: (105.918137, 0.0),
				107: (106.92169, 0.0),
				108: (107.92345, 0.0),
				109: (108.92781, 0.0),
				110: (109.92973, 0.0),
				111: (110.93441, 0.0),
				112: (111.93684, 0.0),
				113: (112.94188, 0.0),
				114: (113.94492, 0.0),
				115: (114.95029, 0.0),
				},
		description=(
				"Silvery-white, hard metallic transition element. It is chemically "
				"unreactive and is not affected by most acids. It oxidizes at high "
				"temperatures. There are seven natural isotopes, and four "
				"radioisotopes, Mo-93 being the most stable with a half-life of 3500 "
				"years. Molybdenum is used in almost all high-strength steels, it "
				"has nuclear applications, and is a catalyst in petroleum refining. "
				"Discovered in 1778 by Carl Welhelm Scheele of Sweden. Impure metal "
				"was prepared in 1782 by Peter Jacob Hjelm. The name comes from the "
				"Greek word molybdos which means lead. Trace amounts of molybdenum "
				"are required for all known forms of life. All molybdenum compounds "
				"should be considered highly toxic, and will also cause severe birth "
				"defects."
				)
		)

Tc = Element(
		43,
		"Tc",
		"Technetium",
		group=7,
		period=5,
		block='d',
		series=8,
		mass=97.9072,
		eleneg=1.9,
		eleaffin=0.55,
		covrad=1.27,
		atmrad=1.95,
		vdwrad=0.0,
		tboil=4538.0,
		tmelt=2477.0,
		density=11.49,
		eleconfig="[Kr] 4d5 5s2",
		oxistates="7*",
		ionenergy=(7.28, 15.26, 29.54),
		isotopes={
				85: (84.94883, 0.0),
				86: (85.94288, 0.0),
				87: (86.93653, 0.0),
				88: (87.93268, 0.0),
				89: (88.92717, 0.0),
				90: (89.92356, 0.0),
				91: (90.91843, 0.0),
				92: (91.91526, 0.0),
				93: (92.910249, 0.0),
				94: (93.909657, 0.0),
				95: (94.907657, 0.0),
				96: (95.907871, 0.0),
				97: (96.906365, 0.0),
				98: (97.907216, 0.0),
				99: (98.9062547, 0.0),
				100: (99.9076578, 0.0),
				101: (100.907315, 0.0),
				102: (101.909215, 0.0),
				103: (102.909181, 0.0),
				104: (103.91145, 0.0),
				105: (104.91166, 0.0),
				106: (105.914358, 0.0),
				107: (106.91508, 0.0),
				108: (107.91846, 0.0),
				109: (108.91998, 0.0),
				110: (109.92382, 0.0),
				111: (110.92569, 0.0),
				112: (111.92915, 0.0),
				113: (112.93159, 0.0),
				114: (113.93588, 0.0),
				115: (114.93869, 0.0),
				116: (115.94337, 0.0),
				117: (116.94648, 0.0),
				118: (117.95148, 0.0),
				},
		description=(
				"Radioactive metallic transition element. Can be detected in some "
				"stars and the fission products of uranium. First made by Perrier "
				"and Segre by bombarding molybdenum with deutrons, giving them "
				"Tc-97. Tc-99 is the most stable isotope with a half-life of "
				"2.6*10^6 years. Sixteen isotopes are known. Organic technetium "
				"compounds are used in bone imaging. Chemical properties are "
				"intermediate between rhenium and manganese."
				)
		)

Ru = Element(
		44,
		"Ru",
		"Ruthenium",
		group=8,
		period=5,
		block='d',
		series=8,
		mass=101.07,
		eleneg=2.2,
		eleaffin=1.04638,
		covrad=1.25,
		atmrad=1.89,
		vdwrad=0.0,
		tboil=4425.0,
		tmelt=2610.0,
		density=12.45,
		eleconfig="[Kr] 4d7 5s",
		oxistates="8, 6, 4*, 3*, 2, 0, -2",
		ionenergy=(7.3605, 16.76, 28.47),
		isotopes={
				87: (86.94918, 0.0),
				88: (87.94026, 0.0),
				89: (88.93611, 0.0),
				90: (89.92989, 0.0),
				91: (90.92629, 0.0),
				92: (91.92012, 0.0),
				93: (92.91705, 0.0),
				94: (93.91136, 0.0),
				95: (94.910413, 0.0),
				96: (95.907598, 0.0554),
				97: (96.907555, 0.0),
				98: (97.905287, 0.0187),
				99: (98.9059393, 0.1276),
				100: (99.9042195, 0.126),
				101: (100.9055821, 0.1706),
				102: (101.9043493, 0.3155),
				103: (102.9063238, 0.0),
				104: (103.905433, 0.1862),
				105: (104.907753, 0.0),
				106: (105.907329, 0.0),
				107: (106.90991, 0.0),
				108: (107.91017, 0.0),
				109: (108.9132, 0.0),
				110: (109.91414, 0.0),
				111: (110.9177, 0.0),
				112: (111.91897, 0.0),
				113: (112.92249, 0.0),
				114: (113.92428, 0.0),
				115: (114.92869, 0.0),
				116: (115.93081, 0.0),
				117: (116.93558, 0.0),
				118: (117.93782, 0.0),
				119: (118.94284, 0.0),
				120: (119.94531, 0.0),
				},
		description=(
				"Hard white metallic transition element. Found with platinum, used "
				"as a catalyst in some platinum alloys. Dissolves in fused alkalis, "
				"and is not attacked by acids. Reacts with halogens and oxygen at "
				"high temperatures. Isolated in 1844 by K.K. Klaus."
				)
		)

Rh = Element(
		45,
		"Rh",
		"Rhodium",
		group=9,
		period=5,
		block='d',
		series=8,
		mass=102.9055,
		eleneg=2.28,
		eleaffin=1.14289,
		covrad=1.25,
		atmrad=1.83,
		vdwrad=0.0,
		tboil=3970.0,
		tmelt=2236.0,
		density=12.41,
		eleconfig="[Kr] 4d8 5s",
		oxistates="5, 4, 3*, 1*, 2, 0",
		ionenergy=(7.4589, 18.08, 31.06),
		isotopes={
				89: (88.94884, 0.0),
				90: (89.94287, 0.0),
				91: (90.93655, 0.0),
				92: (91.93198, 0.0),
				93: (92.92574, 0.0),
				94: (93.9217, 0.0),
				95: (94.9159, 0.0),
				96: (95.914461, 0.0),
				97: (96.91134, 0.0),
				98: (97.910708, 0.0),
				99: (98.908132, 0.0),
				100: (99.908122, 0.0),
				101: (100.906164, 0.0),
				102: (101.906843, 0.0),
				103: (102.905504, 1.0),
				104: (103.906656, 0.0),
				105: (104.905694, 0.0),
				106: (105.907287, 0.0),
				107: (106.906748, 0.0),
				108: (107.90873, 0.0),
				109: (108.908737, 0.0),
				110: (109.91114, 0.0),
				111: (110.91159, 0.0),
				112: (111.91439, 0.0),
				113: (112.91553, 0.0),
				114: (113.91881, 0.0),
				115: (114.92033, 0.0),
				116: (115.92406, 0.0),
				117: (116.92598, 0.0),
				118: (117.93007, 0.0),
				119: (118.93211, 0.0),
				120: (119.93641, 0.0),
				121: (120.93872, 0.0),
				122: (121.94321, 0.0),
				},
		description=(
				"Silvery white metallic transition element. Found with platinum and "
				"used in some platinum alloys. Not attacked by acids, dissolves only "
				"in aqua regia. Discovered in 1803 by W.H. Wollaston."
				)
		)

Pd = Element(
		46,
		"Pd",
		"Palladium",
		group=10,
		period=5,
		block='d',
		series=8,
		mass=106.42,
		eleneg=2.2,
		eleaffin=0.56214,
		covrad=1.28,
		atmrad=1.79,
		vdwrad=1.63,
		tboil=3240.0,
		tmelt=1825.0,
		density=12.02,
		eleconfig="[Kr] 4d10",
		oxistates="4, 2*, 0",
		ionenergy=(8.3369, 19.43, 32.93),
		isotopes={
				91: (90.94911, 0.0),
				92: (91.94042, 0.0),
				93: (92.93591, 0.0),
				94: (93.92877, 0.0),
				95: (94.92469, 0.0),
				96: (95.91816, 0.0),
				97: (96.91648, 0.0),
				98: (97.912721, 0.0),
				99: (98.911768, 0.0),
				100: (99.908506, 0.0),
				101: (100.908289, 0.0),
				102: (101.905609, 0.0102),
				103: (102.906087, 0.0),
				104: (103.904036, 0.1114),
				105: (104.905085, 0.2233),
				106: (105.903486, 0.2733),
				107: (106.905133, 0.0),
				108: (107.903892, 0.2646),
				109: (108.90595, 0.0),
				110: (109.905153, 0.1172),
				111: (110.907671, 0.0),
				112: (111.907314, 0.0),
				113: (112.91015, 0.0),
				114: (113.910363, 0.0),
				115: (114.91368, 0.0),
				116: (115.91416, 0.0),
				117: (116.91784, 0.0),
				118: (117.91898, 0.0),
				119: (118.92311, 0.0),
				120: (119.92469, 0.0),
				121: (120.92887, 0.0),
				122: (121.93055, 0.0),
				123: (122.93493, 0.0),
				124: (123.93688, 0.0),
				},
		description=(
				"Soft white ductile transition element. Found with some copper and "
				"nickel ores. Does not react with oxygen at normal temperatures. "
				"Dissolves slowly in hydrochloric acid. Discovered in 1803 by W.H. "
				"Wollaston"
				),
		)

Ag = Element(
		47,
		"Ag",
		"Silver",
		group=11,
		period=5,
		block='d',
		series=8,
		mass=107.8682,
		eleneg=1.93,
		eleaffin=1.30447,
		covrad=1.34,
		atmrad=1.75,
		vdwrad=1.72,
		tboil=2436.0,
		tmelt=1235.1,
		density=10.49,
		eleconfig="[Kr] 4d10 5s",
		oxistates="2, 1*",
		ionenergy=(7.5762, 21.49, 34.83),
		isotopes={
				93: (92.94978, 0.0),
				94: (93.94278, 0.0),
				95: (94.93548, 0.0),
				96: (95.93068, 0.0),
				97: (96.92397, 0.0),
				98: (97.92157, 0.0),
				99: (98.9176, 0.0),
				100: (99.9161, 0.0),
				101: (100.9128, 0.0),
				102: (101.91169, 0.0),
				103: (102.908973, 0.0),
				104: (103.908629, 0.0),
				105: (104.906529, 0.0),
				106: (105.906669, 0.0),
				107: (106.905097, 0.51839),
				108: (107.905956, 0.0),
				109: (108.904752, 0.48161),
				110: (109.906107, 0.0),
				111: (110.905291, 0.0),
				112: (111.907005, 0.0),
				113: (112.906567, 0.0),
				114: (113.908804, 0.0),
				115: (114.90876, 0.0),
				116: (115.91136, 0.0),
				117: (116.91168, 0.0),
				118: (117.91458, 0.0),
				119: (118.91567, 0.0),
				120: (119.91879, 0.0),
				121: (120.91985, 0.0),
				122: (121.92353, 0.0),
				123: (122.9249, 0.0),
				124: (123.92864, 0.0),
				125: (124.93043, 0.0),
				126: (125.9345, 0.0),
				127: (126.93677, 0.0),
				128: (127.94117, 0.0),
				129: (128.94369, 0.0),
				130: (129.95045, 0.0),
				},
		description=(
				"White lustrous soft metallic transition element. Found in both its "
				"elemental form and in minerals. Used in jewellery, tableware and so "
				"on. Less reactive than silver, chemically."
				)
		)

Cd = Element(
		48,
		"Cd",
		"Cadmium",
		group=12,
		period=5,
		block='d',
		series=8,
		mass=112.414,
		eleneg=1.69,
		eleaffin=0.0,
		covrad=1.48,
		atmrad=1.71,
		vdwrad=1.58,
		tboil=1040.0,
		tmelt=594.26,
		density=8.64,
		eleconfig="[Kr] 4d10 5s2",
		oxistates="2*",
		ionenergy=(8.9938, 16.908, 37.48),
		isotopes={
				95: (94.94987, 0.0),
				96: (95.93977, 0.0),
				97: (96.93494, 0.0),
				98: (97.9274, 0.0),
				99: (98.92501, 0.0),
				100: (99.92029, 0.0),
				101: (100.91868, 0.0),
				102: (101.91446, 0.0),
				103: (102.913419, 0.0),
				104: (103.909849, 0.0),
				105: (104.909468, 0.0),
				106: (105.906459, 0.0125),
				107: (106.906618, 0.0),
				108: (107.904184, 0.0089),
				109: (108.904982, 0.0),
				110: (109.9030021, 0.1249),
				111: (110.9041781, 0.128),
				112: (111.9027578, 0.2413),
				113: (112.9044017, 0.1222),
				114: (113.9033585, 0.2873),
				115: (114.905431, 0.0),
				116: (115.904756, 0.0749),
				117: (116.907219, 0.0),
				118: (117.906915, 0.0),
				119: (118.90992, 0.0),
				120: (119.90985, 0.0),
				121: (120.91298, 0.0),
				122: (121.91333, 0.0),
				123: (122.917, 0.0),
				124: (123.91765, 0.0),
				125: (124.92125, 0.0),
				126: (125.92235, 0.0),
				127: (126.92644, 0.0),
				128: (127.92776, 0.0),
				129: (128.93215, 0.0),
				130: (129.9339, 0.0),
				131: (130.94067, 0.0),
				132: (131.94555, 0.0),
				},
		description=(
				"Soft bluish metal belonging to group 12 of the periodic table. "
				"Extremely toxic even in low concentrations. Chemically similar to "
				"zinc, but lends itself to more complex compounds. Discovered in "
				"1817 by F. Stromeyer."
				)
		)

Hf = Element(
		72,
		"Hf",
		"Hafnium",
		group=4,
		period=6,
		block='d',
		series=8,
		mass=178.49,
		eleneg=1.3,
		eleaffin=0.0,
		covrad=1.44,
		atmrad=2.16,
		vdwrad=0.0,
		tboil=4875.0,
		tmelt=2504.0,
		density=13.31,
		eleconfig="[Xe] 4f14 5d2 6s2",
		oxistates="4*",
		ionenergy=(6.8251, 14.9, 23.3, 33.3),
		isotopes={
				153: (152.97069, 0.0),
				154: (153.96486, 0.0),
				155: (154.96339, 0.0),
				156: (155.95936, 0.0),
				157: (156.9584, 0.0),
				158: (157.954799, 0.0),
				159: (158.953995, 0.0),
				160: (159.950684, 0.0),
				161: (160.950275, 0.0),
				162: (161.94721, 0.0),
				163: (162.94709, 0.0),
				164: (163.944367, 0.0),
				165: (164.94457, 0.0),
				166: (165.94218, 0.0),
				167: (166.9426, 0.0),
				168: (167.94057, 0.0),
				169: (168.94126, 0.0),
				170: (169.93961, 0.0),
				171: (170.94049, 0.0),
				172: (171.939448, 0.0),
				173: (172.94051, 0.0),
				174: (173.940046, 0.0016),
				175: (174.941509, 0.0),
				176: (175.9414086, 0.0526),
				177: (176.9432207, 0.186),
				178: (177.9436988, 0.2728),
				179: (178.9458161, 0.1362),
				180: (179.94655, 0.3508),
				181: (180.9491012, 0.0),
				182: (181.950554, 0.0),
				183: (182.95353, 0.0),
				184: (183.95545, 0.0),
				185: (184.95882, 0.0),
				186: (185.96089, 0.0),
				187: (186.96459, 0.0),
				188: (187.96685, 0.0),
				},
		description=(
				"Silvery lustrous metallic transition element. Used in tungsten "
				"alloys in filaments and electrodes, also acts as a neutron "
				"absorber. First reported by Urbain in 1911, existence was finally "
				"established in 1923 by D. Coster, G.C. de Hevesy in 1923."
				)
		)

Ta = Element(
		73,
		"Ta",
		"Tantalum",
		group=5,
		period=6,
		block='d',
		series=8,
		mass=180.94788,
		eleneg=1.5,
		eleaffin=0.322,
		covrad=1.34,
		atmrad=2.09,
		vdwrad=0.0,
		tboil=5730.0,
		tmelt=3293.0,
		density=16.68,
		eleconfig="[Xe] 4f14 5d3 6s2",
		oxistates="5*",
		ionenergy=(7.5496, ),
		isotopes={
				155: (154.97459, 0.0),
				156: (155.9723, 0.0),
				157: (156.96819, 0.0),
				158: (157.9667, 0.0),
				159: (158.963018, 0.0),
				160: (159.96149, 0.0),
				161: (160.95842, 0.0),
				162: (161.95729, 0.0),
				163: (162.95433, 0.0),
				164: (163.95353, 0.0),
				165: (164.950773, 0.0),
				166: (165.95051, 0.0),
				167: (166.94809, 0.0),
				168: (167.94805, 0.0),
				169: (168.94601, 0.0),
				170: (169.94618, 0.0),
				171: (170.94448, 0.0),
				172: (171.9449, 0.0),
				173: (172.94375, 0.0),
				174: (173.94445, 0.0),
				175: (174.94374, 0.0),
				176: (175.94486, 0.0),
				177: (176.944472, 0.0),
				178: (177.945778, 0.0),
				179: (178.9459295, 0.0),
				180: (179.9474648, 0.00012),
				181: (180.9479958, 0.99988),
				182: (181.9501518, 0.0),
				183: (182.9513726, 0.0),
				184: (183.954008, 0.0),
				185: (184.955559, 0.0),
				186: (185.95855, 0.0),
				187: (186.96053, 0.0),
				188: (187.9637, 0.0),
				189: (188.96583, 0.0),
				190: (189.96923, 0.0),
				},
		description=(
				"Heavy blue-grey metallic transition element. Ta-181 is a stable "
				"isotope, and Ta-180 is a radioactive isotope, with a half-life in "
				"excess of 10^7 years. Used in surgery as it is unreactive. Forms a "
				"passive oxide layer in air. Identified in 1802 by Ekeberg and "
				"isolated in 1820 by Jons J. Berzelius."
				)
		)

W = Element(
		74,
		'W',
		"Tungsten",
		group=6,
		period=6,
		block='d',
		series=8,
		mass=183.84,
		eleneg=2.36,
		eleaffin=0.815,
		covrad=1.3,
		atmrad=2.02,
		vdwrad=0.0,
		tboil=5825.0,
		tmelt=3695.0,
		density=19.26,
		eleconfig="[Xe] 4f14 5d4 6s2",
		oxistates="6*, 5, 4, 3, 2, 0",
		ionenergy=(7.864, ),
		isotopes={
				158: (157.97456, 0.0),
				159: (158.97292, 0.0),
				160: (159.96848, 0.0),
				161: (160.96736, 0.0),
				162: (161.963497, 0.0),
				163: (162.96252, 0.0),
				164: (163.958954, 0.0),
				165: (164.95828, 0.0),
				166: (165.955027, 0.0),
				167: (166.954816, 0.0),
				168: (167.951808, 0.0),
				169: (168.951779, 0.0),
				170: (169.949228, 0.0),
				171: (170.94945, 0.0),
				172: (171.94729, 0.0),
				173: (172.94769, 0.0),
				174: (173.94608, 0.0),
				175: (174.94672, 0.0),
				176: (175.94563, 0.0),
				177: (176.94664, 0.0),
				178: (177.945876, 0.0),
				179: (178.94707, 0.0),
				180: (179.946704, 0.0012),
				181: (180.948197, 0.0),
				182: (181.9482042, 0.265),
				183: (182.950223, 0.1431),
				184: (183.9509312, 0.3064),
				185: (184.9534193, 0.0),
				186: (185.9543641, 0.2843),
				187: (186.9571605, 0.0),
				188: (187.958489, 0.0),
				189: (188.96191, 0.0),
				190: (189.96318, 0.0),
				191: (190.9666, 0.0),
				192: (191.96817, 0.0),
				},
		description=(
				"White or grey metallic transition element,formerly called Wolfram. "
				"Forms a protective oxide in air and can be oxidized at high "
				"temperature. First isolated by Jose and Fausto de Elhuyer in 1783."
				)
		)

Re = Element(
		75,
		"Re",
		"Rhenium",
		group=7,
		period=6,
		block='d',
		series=8,
		mass=186.207,
		eleneg=1.9,
		eleaffin=0.15,
		covrad=1.28,
		atmrad=1.97,
		vdwrad=0.0,
		tboil=5870.0,
		tmelt=3455.0,
		density=21.03,
		eleconfig="[Xe] 4f14 5d5 6s2",
		oxistates="7, 6, 4, 2, -1",
		ionenergy=(7.8335, ),
		isotopes={
				160: (159.98212, 0.0),
				161: (160.97759, 0.0),
				162: (161.976, 0.0),
				163: (162.972081, 0.0),
				164: (163.97032, 0.0),
				165: (164.967089, 0.0),
				166: (165.96581, 0.0),
				167: (166.9626, 0.0),
				168: (167.96157, 0.0),
				169: (168.95879, 0.0),
				170: (169.95822, 0.0),
				171: (170.95572, 0.0),
				172: (171.95542, 0.0),
				173: (172.95324, 0.0),
				174: (173.95312, 0.0),
				175: (174.95138, 0.0),
				176: (175.95162, 0.0),
				177: (176.95033, 0.0),
				178: (177.95099, 0.0),
				179: (178.949988, 0.0),
				180: (179.950789, 0.0),
				181: (180.950068, 0.0),
				182: (181.95121, 0.0),
				183: (182.95082, 0.0),
				184: (183.952521, 0.0),
				185: (184.952955, 0.374),
				186: (185.9549861, 0.0),
				187: (186.9557531, 0.626),
				188: (187.9581144, 0.0),
				189: (188.959229, 0.0),
				190: (189.96182, 0.0),
				191: (190.963125, 0.0),
				192: (191.96596, 0.0),
				193: (192.96747, 0.0),
				194: (193.97042, 0.0),
				},
		description=(
				"Silvery-white metallic transition element. Obtained as a "
				"by-product of molybdenum refinement. Rhenium-molybdenum alloys are "
				"superconducting."
				)
		)

Os = Element(
		76,
		"Os",
		"Osmium",
		group=8,
		period=6,
		block='d',
		series=8,
		mass=190.23,
		eleneg=2.2,
		eleaffin=1.0778,
		covrad=1.26,
		atmrad=1.92,
		vdwrad=0.0,
		tboil=5300.0,
		tmelt=3300.0,
		density=22.61,
		eleconfig="[Xe] 4f14 5d6 6s2",
		oxistates="8, 6, 4*, 3, 2, 0, -2",
		ionenergy=(8.4382, ),
		isotopes={
				162: (161.98443, 0.0),
				163: (162.98269, 0.0),
				164: (163.97804, 0.0),
				165: (164.97676, 0.0),
				166: (165.972691, 0.0),
				167: (166.97155, 0.0),
				168: (167.967804, 0.0),
				169: (168.967019, 0.0),
				170: (169.963577, 0.0),
				171: (170.963185, 0.0),
				172: (171.960023, 0.0),
				173: (172.959808, 0.0),
				174: (173.957062, 0.0),
				175: (174.956946, 0.0),
				176: (175.95481, 0.0),
				177: (176.954965, 0.0),
				178: (177.953251, 0.0),
				179: (178.953816, 0.0),
				180: (179.952379, 0.0),
				181: (180.95324, 0.0),
				182: (181.95211, 0.0),
				183: (182.95313, 0.0),
				184: (183.9524891, 0.0002),
				185: (184.9540423, 0.0),
				186: (185.9538382, 0.0159),
				187: (186.9557505, 0.0196),
				188: (187.9558382, 0.1324),
				189: (188.9581475, 0.1615),
				190: (189.958447, 0.2626),
				191: (190.9609297, 0.0),
				192: (191.9614807, 0.4078),
				193: (192.9641516, 0.0),
				194: (193.9651821, 0.0),
				195: (194.96813, 0.0),
				196: (195.96964, 0.0),
				},
		description=(
				"Hard blue-white metallic transition element. Found with platinum "
				"and used in some alloys with platinum and iridium."
				)
		)

Ir = Element(
		77,
		"Ir",
		"Iridium",
		group=9,
		period=6,
		block='d',
		series=8,
		mass=192.217,
		eleneg=2.2,
		eleaffin=1.56436,
		covrad=1.27,
		atmrad=1.87,
		vdwrad=0.0,
		tboil=4700.0,
		tmelt=2720.0,
		density=22.65,
		eleconfig="[Xe] 4f14 5d7 6s2",
		oxistates="6, 4*, 3, 2, 1*, 0, -1",
		ionenergy=(8.967, ),
		isotopes={
				164: (163.9922, 0.0),
				165: (164.98752, 0.0),
				166: (165.98582, 0.0),
				167: (166.981665, 0.0),
				168: (167.97988, 0.0),
				169: (168.976295, 0.0),
				170: (169.97497, 0.0),
				171: (170.97163, 0.0),
				172: (171.97046, 0.0),
				173: (172.967502, 0.0),
				174: (173.966861, 0.0),
				175: (174.964113, 0.0),
				176: (175.963649, 0.0),
				177: (176.961302, 0.0),
				178: (177.961082, 0.0),
				179: (178.959122, 0.0),
				180: (179.959229, 0.0),
				181: (180.957625, 0.0),
				182: (181.958076, 0.0),
				183: (182.956846, 0.0),
				184: (183.95748, 0.0),
				185: (184.9567, 0.0),
				186: (185.957946, 0.0),
				187: (186.957363, 0.0),
				188: (187.958853, 0.0),
				189: (188.958719, 0.0),
				190: (189.960546, 0.0),
				191: (190.960594, 0.373),
				192: (191.962605, 0.0),
				193: (192.9629264, 0.627),
				194: (193.9650784, 0.0),
				195: (194.9659796, 0.0),
				196: (195.9684, 0.0),
				197: (196.969653, 0.0),
				198: (197.97228, 0.0),
				199: (198.9738, 0.0),
				},
		description=(
				"Very hard and brittle, silvery metallic transition element. It has "
				"a yellowish cast to it. Salts of iridium are highly colored. It is "
				"the most corrosion resistant metal known, not attacked by any acid, "
				"but is attacked by molten salts. There are two natural isotopes of "
				"iridium, and 4 radioisotopes, the most stable being Ir-192 with a "
				"half-life of 73.83 days. Ir-192 decays into Platinum, while the "
				"other radioisotopes decay into Osmium. Iridium is used in high "
				"temperature apparatus, electrical contacts, and as a hardening "
				"agent for platinumpy. Discovered in 1803 by Smithson Tennant in "
				"England. The name comes from the Greek word iris, which means "
				"rainbow. Iridium metal is generally non-toxic due to its relative "
				"unreactivity, but iridium compounds should be considered highly "
				"toxic."
				)
		)

Pt = Element(
		78,
		"Pt",
		"Platinum",
		group=10,
		period=6,
		block='d',
		series=8,
		mass=195.084,
		eleneg=2.28,
		eleaffin=2.1251,
		covrad=1.3,
		atmrad=1.83,
		vdwrad=1.75,
		tboil=4100.0,
		tmelt=2042.1,
		density=21.45,
		eleconfig="[Xe] 4f14 5d9 6s",
		oxistates="4*, 2*, 0",
		ionenergy=(8.9588, 18.563),
		isotopes={
				166: (165.99486, 0.0),
				167: (166.99298, 0.0),
				168: (167.98815, 0.0),
				169: (168.98672, 0.0),
				170: (169.982495, 0.0),
				171: (170.98124, 0.0),
				172: (171.977347, 0.0),
				173: (172.97644, 0.0),
				174: (173.972819, 0.0),
				175: (174.972421, 0.0),
				176: (175.968945, 0.0),
				177: (176.968469, 0.0),
				178: (177.965649, 0.0),
				179: (178.965363, 0.0),
				180: (179.963031, 0.0),
				181: (180.963097, 0.0),
				182: (181.961171, 0.0),
				183: (182.961597, 0.0),
				184: (183.959922, 0.0),
				185: (184.96062, 0.0),
				186: (185.959351, 0.0),
				187: (186.96059, 0.0),
				188: (187.959395, 0.0),
				189: (188.960834, 0.0),
				190: (189.959932, 0.00014),
				191: (190.961677, 0.0),
				192: (191.961038, 0.00782),
				193: (192.9629874, 0.0),
				194: (193.9626803, 0.32967),
				195: (194.9647911, 0.33832),
				196: (195.9649515, 0.25242),
				197: (196.9673402, 0.0),
				198: (197.967893, 0.07163),
				199: (198.970593, 0.0),
				200: (199.971441, 0.0),
				201: (200.97451, 0.0),
				202: (201.97574, 0.0),
				},
		description=(
				"Attractive greyish-white metal. When pure, it is malleable and "
				"ductile. Does not oxidize in air, insoluble in hydrochloric and "
				"nitric acid. Corroded by halogens, cyandies, sulphur and alkalis. "
				"Hydrogen and Oxygen react explosively in the presence of "
				"platinumpy. There are six stable isotopes and three radioisotopes, "
				"the most stable being Pt-193 with a half-life of 60 years. Platinum "
				"is used in jewelry, laboratory equipment, electrical contacts, "
				"dentistry, and anti-pollution devices in cars. PtCl2(NH3)2 is used "
				"to treat some forms of cancer. Platinum-Cobalt alloys have magnetic "
				"properties. It is also used in the definition of the Standard "
				"Hydrogen Electrode. Discovered by Antonio de Ulloa in South America "
				"in 1735. The name comes from the Spanish word platina which means "
				"silver. Platinum metal is generally not a health concern due to its "
				"unreactivity, however platinum compounds should be considered "
				"highly toxic."
				)
		)

Au = Element(
		79,
		"Au",
		"Gold",
		group=11,
		period=6,
		block='d',
		series=8,
		mass=196.966569,
		eleneg=2.54,
		eleaffin=2.30861,
		covrad=1.34,
		atmrad=1.79,
		vdwrad=1.66,
		tboil=3130.0,
		tmelt=1337.58,
		density=19.32,
		eleconfig="[Xe] 4f14 5d10 6s",
		oxistates="3*, 1",
		ionenergy=(9.2255, 20.5),
		isotopes={
				169: (168.99808, 0.0),
				170: (169.99612, 0.0),
				171: (170.991879, 0.0),
				172: (171.99004, 0.0),
				173: (172.986237, 0.0),
				174: (173.98476, 0.0),
				175: (174.98127, 0.0),
				176: (175.9801, 0.0),
				177: (176.976865, 0.0),
				178: (177.97603, 0.0),
				179: (178.973213, 0.0),
				180: (179.972521, 0.0),
				181: (180.970079, 0.0),
				182: (181.969618, 0.0),
				183: (182.967593, 0.0),
				184: (183.967452, 0.0),
				185: (184.965789, 0.0),
				186: (185.965953, 0.0),
				187: (186.964568, 0.0),
				188: (187.965324, 0.0),
				189: (188.963948, 0.0),
				190: (189.9647, 0.0),
				191: (190.9637, 0.0),
				192: (191.964813, 0.0),
				193: (192.96415, 0.0),
				194: (193.965365, 0.0),
				195: (194.9650346, 0.0),
				196: (195.96657, 0.0),
				197: (196.9665687, 1.0),
				198: (197.9682423, 0.0),
				199: (198.9687652, 0.0),
				200: (199.97073, 0.0),
				201: (200.971657, 0.0),
				202: (201.97381, 0.0),
				203: (202.975155, 0.0),
				204: (203.97772, 0.0),
				205: (204.97987, 0.0),
				},
		description=(
				"Gold is gold colored. It is the most malleable and ductile metal "
				"known. There is only one stable isotope of gold, and five "
				"radioisotopes of gold, Au-195 being the most stable with a "
				"half-life of 186 days. Gold is used as a monetary standard, in "
				"jewelry, dentistry, electronics. Au-198 is used in treating cancer "
				"and some other medical conditions. Gold has been known to exist as "
				"far back as 2600 BC. Gold comes from the Anglo-Saxon word gold. Its "
				"symbol, Au, comes from the Latin word aurum, which means gold. Gold "
				"is not particularly toxic, however it is known to cause damage to "
				"the liver and kidneys in some."
				)
		)

Hg = Element(
		80,
		"Hg",
		"Mercury",
		group=12,
		period=6,
		block='d',
		series=8,
		mass=200.592,
		eleneg=2.0,
		eleaffin=0.0,
		covrad=1.49,
		atmrad=1.76,
		vdwrad=0.0,
		tboil=629.88,
		tmelt=234.31,
		density=13.55,
		eleconfig="[Xe] 4f14 5d10 6s2",
		oxistates="2*, 1",
		ionenergy=(10.4375, 18.756, 34.2),
		isotopes={
				171: (171.00376, 0.0),
				172: (171.99883, 0.0),
				173: (172.99724, 0.0),
				174: (173.992864, 0.0),
				175: (174.99142, 0.0),
				176: (175.987355, 0.0),
				177: (176.98628, 0.0),
				178: (177.982483, 0.0),
				179: (178.981834, 0.0),
				180: (179.978266, 0.0),
				181: (180.977819, 0.0),
				182: (181.97469, 0.0),
				183: (182.97445, 0.0),
				184: (183.971713, 0.0),
				185: (184.971899, 0.0),
				186: (185.969362, 0.0),
				187: (186.969814, 0.0),
				188: (187.967577, 0.0),
				189: (188.96819, 0.0),
				190: (189.966322, 0.0),
				191: (190.967157, 0.0),
				192: (191.965634, 0.0),
				193: (192.966665, 0.0),
				194: (193.965439, 0.0),
				195: (194.96672, 0.0),
				196: (195.965833, 0.0015),
				197: (196.967213, 0.0),
				198: (197.966769, 0.0997),
				199: (198.9682799, 0.1687),
				200: (199.968326, 0.231),
				201: (200.9703023, 0.1318),
				202: (201.970643, 0.2986),
				203: (202.9728725, 0.0),
				204: (203.9734939, 0.0687),
				205: (204.976073, 0.0),
				206: (205.977514, 0.0),
				207: (206.98259, 0.0),
				208: (207.98594, 0.0),
				209: (208.99104, 0.0),
				210: (209.99451, 0.0),
				},
		description=(
				"Heavy silvery liquid metallic element, belongs to the zinc group. "
				"Used in thermometers, barometers and other scientific apparatus. "
				"Less reactive than zinc and cadmium, does not displace hydrogen "
				"from acids. Forms a number of complexes and organomercury "
				"compounds."
				)
		)

Rf = Element(
		104,
		"Rf",
		"Rutherfordium",
		group=4,
		period=7,
		block='d',
		series=8,
		mass=267.1218,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=0.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d2 7s2",
		oxistates='*',
		ionenergy=(6.0, ),
		isotopes={
				253: (253.10069, 0.0),
				254: (254.10018, 0.0),
				255: (255.10134, 0.0),
				256: (256.101166, 0.0),
				257: (257.10299, 0.0),
				258: (258.10349, 0.0),
				259: (259.10564, 0.0),
				260: (260.10644, 0.0),
				261: (261.10877, 0.0),
				262: (262.10993, 0.0),
				263: (263.11255, 0.0),
				264: (264.11399, 0.0),
				265: (265.1167, 0.0),
				266: (266.11796, 0.0),
				267: (267.12153, 0.0),
				268: (268.12364, 0.0),
				},
		description=(
				"Radioactive transactinide element. Expected to have similar "
				"chemical properties to those displayed by hafnium. Rf-260 was "
				"discovered by the Joint Nuclear Research Institute at Dubna "
				"(U.S.S.R.) in 1964. Researchers at Berkeley discovered Unq-257 and "
				"Unq-258 in 1964."
				)
		)

Db = Element(
		105,
		"Db",
		"Dubnium",
		group=5,
		period=7,
		block='d',
		series=8,
		mass=268.1257,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=0.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d3 7s2",
		oxistates='*',
		ionenergy=(),
		isotopes={
				255: (255.1074, 0.0),
				256: (256.10813, 0.0),
				257: (257.10772, 0.0),
				258: (258.10923, 0.0),
				259: (259.10961, 0.0),
				260: (260.1113, 0.0),
				261: (261.11206, 0.0),
				262: (262.11408, 0.0),
				263: (263.11499, 0.0),
				264: (264.1174, 0.0),
				265: (265.1186, 0.0),
				266: (266.12103, 0.0),
				267: (267.12238, 0.0),
				268: (268.12545, 0.0),
				269: (269.12746, 0.0),
				270: (270.13071, 0.0),
				},
		description=(
				"Also known as Hahnium, Ha. Radioactive transactinide element. "
				"Half-life of 1.6s. Discovered in 1970 by Berkeley researchers. So "
				"far, seven isotopes have been discovered."
				)
		)

Sg = Element(
		106,
		"Sg",
		"Seaborgium",
		group=6,
		period=7,
		block='d',
		series=8,
		mass=271.1339,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=0.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d4 7s2",
		oxistates='*',
		ionenergy=(),
		isotopes={
				258: (258.11317, 0.0),
				259: (259.1145, 0.0),
				260: (260.11442, 0.0),
				261: (261.11612, 0.0),
				262: (262.1164, 0.0),
				263: (263.11832, 0.0),
				264: (264.11893, 0.0),
				265: (265.12111, 0.0),
				266: (266.12207, 0.0),
				267: (267.12443, 0.0),
				268: (268.12561, 0.0),
				269: (269.12876, 0.0),
				270: (270.13033, 0.0),
				271: (271.13347, 0.0),
				272: (272.13516, 0.0),
				273: (273.13822, 0.0),
				},
		description=(
				"Half-life of 0.9 +/- 0.2 s. Discovered by the Joint Institute for "
				"Nuclear Research at Dubna (U.S.S.R.) in June of 1974. Its existence "
				"was confirmed by the Lawrence Berkeley Laboratory and Livermore "
				"National Laboratory in September of 1974."
				)
		)

Bh = Element(
		107,
		"Bh",
		"Bohrium",
		group=7,
		period=7,
		block='d',
		series=8,
		mass=272.1383,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=0.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d5 7s2",
		oxistates='*',
		ionenergy=(),
		isotopes={
				260: (260.12197, 0.0),
				261: (261.12166, 0.0),
				262: (262.12289, 0.0),
				263: (263.12304, 0.0),
				264: (264.1246, 0.0),
				265: (265.12515, 0.0),
				266: (266.12694, 0.0),
				267: (267.12765, 0.0),
				268: (268.12976, 0.0),
				269: (269.13069, 0.0),
				270: (270.13362, 0.0),
				271: (271.13518, 0.0),
				272: (272.13803, 0.0),
				273: (273.13962, 0.0),
				274: (274.14244, 0.0),
				275: (275.14425, 0.0),
				},
		description=(
				"Radioactive transition metal. Half-life of approximately 1/500 s. "
				"Discovered by the Joint Institute for Nuclear Research at Dubna "
				"(U.S.S.R.) in 1976. Confirmed by West German physicists at the "
				"Heavy Ion Research Laboratory at Darmstadt."
				)
		)

Hs = Element(
		108,
		"Hs",
		"Hassium",
		group=8,
		period=7,
		block='d',
		series=8,
		mass=270.1343,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=0.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d6 7s2",
		oxistates='*',
		ionenergy=(),
		isotopes={
				263: (263.12856, 0.0),
				264: (264.12839, 0.0),
				265: (265.13009, 0.0),
				266: (266.1301, 0.0),
				267: (267.13179, 0.0),
				268: (268.13216, 0.0),
				269: (269.13406, 0.0),
				270: (270.13465, 0.0),
				271: (271.13766, 0.0),
				272: (272.13905, 0.0),
				273: (273.14199, 0.0),
				274: (274.14313, 0.0),
				275: (275.14595, 0.0),
				276: (276.14721, 0.0),
				277: (277.14984, 0.0),
				},
		description=(
				"Radioactive transition metal first synthesized in 1984 by a German "
				"research team led by Peter Armbruster and Gottfried Muenzenberg at "
				"the Institute for Heavy Ion Research at Darmstadt."
				)
		)

Mt = Element(
		109,
		"Mt",
		"Meitnerium",
		group=9,
		period=7,
		block='d',
		series=8,
		mass=276.1516,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=0.0,
		density=0.0,
		eleconfig="[Rn] 5f14 6d7 7s2",
		oxistates='*',
		ionenergy=(),
		isotopes={
				265: (265.13615, 0.0),
				266: (266.1373, 0.0),
				267: (267.13731, 0.0),
				268: (268.13873, 0.0),
				269: (269.13906, 0.0),
				270: (270.14066, 0.0),
				271: (271.14114, 0.0),
				272: (272.14374, 0.0),
				273: (273.14491, 0.0),
				274: (274.14749, 0.0),
				275: (275.14865, 0.0),
				276: (276.15116, 0.0),
				277: (277.15242, 0.0),
				278: (278.15481, 0.0),
				279: (279.15619, 0.0),
				},
		description=(
				"Half-life of approximately 5 ms. The creation of this element "
				"demonstrated that fusion techniques could indeed be used to make "
				"new, heavy nuclei. Made and identified by physicists of the Heavy "
				"Ion Research Laboratory, Darmstadt, West Germany in 1982. Named in "
				"honor of Lise Meitner, the Austrian physicist."
				)
		)

Ds = Element(
		110,
		"Ds",
		"Darmstadtium",
		group=10,
		period=7,
		block='d',
		series=8,
		isotopes={
				267: (267.14434, 0.0),
				268: (268.1438, 0.0),
				269: (269.14512, 0.0),
				270: (270.14472, 0.0),
				271: (271.14606, 0.0),
				272: (272.14632, 0.0),
				273: (273.14886, 0.0),
				274: (274.14949, 0.0),
				275: (275.15218, 0.0),
				276: (276.15303, 0.0),
				277: (277.15565, 0.0),
				278: (278.15647, 0.0),
				279: (279.15886, 0.0),
				280: (280.1598, 0.0),
				281: (281.16206, 0.0),
				}
		)

Rg = Element(
		111,
		"Rg",
		"Roentgenium",
		group=11,
		period=7,
		block='d',
		series=8,
		isotopes={
				272: (272.15362, 0.0),
				273: (273.15368, 0.0),
				274: (274.15571, 0.0),
				275: (275.15614, 0.0),
				276: (276.15849, 0.0),
				277: (277.15952, 0.0),
				278: (278.1616, 0.0),
				279: (279.16247, 0.0),
				280: (280.16447, 0.0),
				281: (281.16537, 0.0),
				282: (282.16749, 0.0),
				283: (283.16842, 0.0),
				}
		)

Cn = Element(
		112,
		"Cn",
		"Roentgenium",
		group=12,
		period=7,
		block='d',
		series=8,
		isotopes={
				277: (277.16394, 0.0),
				278: (278.16431, 0.0),
				279: (279.16655, 0.0),
				280: (280.16704, 0.0),
				281: (281.16929, 0.0),
				282: (282.16977, 0.0),
				283: (283.17179, 0.0),
				284: (284.17238, 0.0),
				285: (285.17411, 0.0),
				}
		)
