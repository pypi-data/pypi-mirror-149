#!/usr/bin/env python3
#
#  pnictogens.py
r"""
Group 15: Pnictogens in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: N

	:class:`~chemistry_tools.elements.classes.Element` representing Nitrogen

.. data:: P

	:class:`~chemistry_tools.elements.classes.Element` representing Phosphorus

.. data:: As

	:class:`~chemistry_tools.elements.classes.Element` representing Arsenic

.. data:: Sb

	:class:`~chemistry_tools.elements.classes.Element` representing Antimony

.. data:: Bi

	:class:`~chemistry_tools.elements.classes.Element` representing Bismuth

.. data:: Mc

	:class:`~chemistry_tools.elements.classes.Element` representing Moscovium

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

__all__ = ('N', 'P', "As", "Sb", "Bi", "Mc")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

N = Element(
		7,
		'N',
		"Nitrogen",
		group=15,
		period=2,
		block='p',
		series=1,
		mass=14.006703,
		eleneg=3.04,
		eleaffin=-0.07,
		covrad=0.75,
		atmrad=0.75,
		vdwrad=1.55,
		tboil=77.344,
		tmelt=63.15,
		density=1.17,
		eleconfig="[He] 2s2 2p3",
		oxistates="5, 4, 3, 2, -3*",
		ionenergy=(
				14.5341,
				39.601,
				47.488,
				77.472,
				97.888,
				522.057,
				667.029,
				),
		isotopes={
				10: (10.04165, 0.0),
				11: (11.02609, 0.0),
				12: (12.0186132, 0.0),
				13: (13.00573861, 0.0),
				14: (14.0030740048, 0.99636),
				15: (15.0001088982, 0.00364),
				16: (16.0061017, 0.0),
				17: (17.00845, 0.0),
				18: (18.014079, 0.0),
				19: (19.017029, 0.0),
				20: (20.02337, 0.0),
				21: (21.02711, 0.0),
				22: (22.03439, 0.0),
				23: (23.04122, 0.0),
				24: (24.05104, 0.0),
				25: (25.06066, 0.0),
				},
		description=(
				"Colourless, gaseous element which belongs to group 15 of the "
				"periodic table. Constitutes ~78% of the atmosphere and is an "
				"essential part of the ecosystem. Nitrogen for industrial purposes "
				"is acquired by the fractional distillation of liquid air. "
				"Chemically inactive, reactive generally only at high temperatures "
				"or in electrical discharges. It was discovered in 1772 by D. "
				"Rutherford."
				)
		)

P = Element(
		15,
		'P',
		"Phosphorus",
		group=15,
		period=3,
		block='p',
		series=1,
		mass=30.973761998,
		eleneg=2.19,
		eleaffin=0.7465,
		covrad=1.06,
		atmrad=1.23,
		vdwrad=1.8,
		tboil=553.0,
		tmelt=317.3,
		density=1.82,
		eleconfig="[Ne] 3s2 3p3",
		oxistates="5*, 3, -3",
		ionenergy=(
				10.4867,
				19.725,
				30.18,
				51.37,
				65.023,
				220.43,
				263.22,
				309.41,
				371.73,
				424.5,
				479.57,
				560.41,
				611.85,
				2816.943,
				3069.762,
				),
		isotopes={
				24: (24.03435, 0.0),
				25: (25.02026, 0.0),
				26: (26.01178, 0.0),
				27: (26.99923, 0.0),
				28: (27.992315, 0.0),
				29: (28.9818006, 0.0),
				30: (29.9783138, 0.0),
				31: (30.97376163, 1.0),
				32: (31.97390727, 0.0),
				33: (32.9717255, 0.0),
				34: (33.973636, 0.0),
				35: (34.9733141, 0.0),
				36: (35.97826, 0.0),
				37: (36.97961, 0.0),
				38: (37.98416, 0.0),
				39: (38.98618, 0.0),
				40: (39.9913, 0.0),
				41: (40.99434, 0.0),
				42: (42.00101, 0.0),
				43: (43.00619, 0.0),
				44: (44.01299, 0.0),
				45: (45.01922, 0.0),
				46: (46.02738, 0.0),
				},
		description=(
				"Non-metallic element belonging to group 15 of the periodic table. "
				"Has a multiple allotropic forms. Essential element for living "
				"organisms. It was discovered by Brandt in 1669."
				)
		)

As = Element(
		33,
		"As",
		"Arsenic",
		group=15,
		period=4,
		block='p',
		series=5,
		mass=74.921595,
		eleneg=2.18,
		eleaffin=0.814,
		covrad=1.2,
		atmrad=1.33,
		vdwrad=1.85,
		tboil=876.0,
		tmelt=1090.0,
		density=5.72,
		eleconfig="[Ar] 3d10 4s2 4p3",
		oxistates="5, 3*, -3",
		ionenergy=(
				9.7886,
				18.633,
				28.351,
				50.13,
				62.63,
				127.6,
				),
		isotopes={
				60: (59.99313, 0.0),
				61: (60.98062, 0.0),
				62: (61.9732, 0.0),
				63: (62.96369, 0.0),
				64: (63.95757, 0.0),
				65: (64.94956, 0.0),
				66: (65.94471, 0.0),
				67: (66.93919, 0.0),
				68: (67.93677, 0.0),
				69: (68.93227, 0.0),
				70: (69.93092, 0.0),
				71: (70.927112, 0.0),
				72: (71.926752, 0.0),
				73: (72.923825, 0.0),
				74: (73.9239287, 0.0),
				75: (74.9215965, 1.0),
				76: (75.922394, 0.0),
				77: (76.9206473, 0.0),
				78: (77.921827, 0.0),
				79: (78.920948, 0.0),
				80: (79.922534, 0.0),
				81: (80.922132, 0.0),
				82: (81.9245, 0.0),
				83: (82.92498, 0.0),
				84: (83.92906, 0.0),
				85: (84.93202, 0.0),
				86: (85.9365, 0.0),
				87: (86.9399, 0.0),
				88: (87.94494, 0.0),
				89: (88.94939, 0.0),
				90: (89.9555, 0.0),
				91: (90.96043, 0.0),
				92: (91.9668, 0.0),
				},
		description=(
				"Metalloid element of group 15. There are three allotropes, yellow, "
				"black, and grey. Reacts with halogens, concentrated oxidizing acids "
				"and hot alkalis. Albertus Magnus is believed to have been the first "
				"to isolate the element in 1250."
				)
		)

Sb = Element(
		51,
		"Sb",
		"Antimony",
		group=15,
		period=5,
		block='p',
		series=5,
		mass=121.76,
		eleneg=2.05,
		eleaffin=1.047401,
		covrad=1.4,
		atmrad=1.53,
		vdwrad=0.0,
		tboil=1860.0,
		tmelt=903.91,
		density=6.69,
		eleconfig="[Kr] 4d10 5s2 5p3",
		oxistates="5, 3*, -3",
		ionenergy=(
				8.6084,
				16.53,
				25.3,
				44.2,
				56.0,
				108.0,
				),
		isotopes={
				103: (102.93969, 0.0),
				104: (103.93647, 0.0),
				105: (104.93149, 0.0),
				106: (105.92879, 0.0),
				107: (106.92415, 0.0),
				108: (107.92216, 0.0),
				109: (108.918132, 0.0),
				110: (109.91675, 0.0),
				111: (110.91316, 0.0),
				112: (111.912398, 0.0),
				113: (112.909372, 0.0),
				114: (113.90927, 0.0),
				115: (114.906598, 0.0),
				116: (115.906794, 0.0),
				117: (116.904836, 0.0),
				118: (117.905529, 0.0),
				119: (118.903942, 0.0),
				120: (119.905072, 0.0),
				121: (120.9038157, 0.5721),
				122: (121.9051737, 0.0),
				123: (122.904214, 0.4279),
				124: (123.9059357, 0.0),
				125: (124.9052538, 0.0),
				126: (125.90725, 0.0),
				127: (126.906924, 0.0),
				128: (127.909169, 0.0),
				129: (128.909148, 0.0),
				130: (129.911656, 0.0),
				131: (130.911982, 0.0),
				132: (131.914467, 0.0),
				133: (132.915252, 0.0),
				134: (133.92038, 0.0),
				135: (134.92517, 0.0),
				136: (135.93035, 0.0),
				137: (136.93531, 0.0),
				138: (137.94079, 0.0),
				139: (138.94598, 0.0),
				},
		description=(
				"Element of group 15. Multiple allotropic forms. The stable form of "
				"antimony is a blue-white metal. Yellow and black antimony are "
				"unstable non-metals. Used in flame-proofing, paints, ceramics, "
				"enamels, and rubber. Attacked by oxidizing acids and halogens. "
				"First reported by Tholden in 1450."
				)
		)

Bi = Element(
		83,
		"Bi",
		"Bismuth",
		group=15,
		period=6,
		block='p',
		series=7,
		mass=208.9804,
		eleneg=2.02,
		eleaffin=0.942363,
		covrad=1.46,
		atmrad=1.63,
		vdwrad=0.0,
		tboil=1837.0,
		tmelt=544.59,
		density=9.8,
		eleconfig="[Xe] 4f14 5d10 6s2 6p3",
		oxistates="5, 3*",
		ionenergy=(
				7.2855,
				16.69,
				25.56,
				45.3,
				56.0,
				88.3,
				),
		isotopes={
				184: (184.00112, 0.0),
				185: (184.99763, 0.0),
				186: (185.9966, 0.0),
				187: (186.993158, 0.0),
				188: (187.99227, 0.0),
				189: (188.9892, 0.0),
				190: (189.9883, 0.0),
				191: (190.985786, 0.0),
				192: (191.98546, 0.0),
				193: (192.98296, 0.0),
				194: (193.98283, 0.0),
				195: (194.980651, 0.0),
				196: (195.980667, 0.0),
				197: (196.978864, 0.0),
				198: (197.97921, 0.0),
				199: (198.977672, 0.0),
				200: (199.978132, 0.0),
				201: (200.977009, 0.0),
				202: (201.977742, 0.0),
				203: (202.976876, 0.0),
				204: (203.977813, 0.0),
				205: (204.977389, 0.0),
				206: (205.978499, 0.0),
				207: (206.9784707, 0.0),
				208: (207.9797422, 0.0),
				209: (208.9803987, 1.0),
				210: (209.9841204, 0.0),
				211: (210.987269, 0.0),
				212: (211.9912857, 0.0),
				213: (212.994385, 0.0),
				214: (213.998712, 0.0),
				215: (215.00177, 0.0),
				216: (216.006306, 0.0),
				217: (217.00947, 0.0),
				218: (218.01432, 0.0),
				},
		description=(
				"White crystalline metal with a pink tinge, belongs to group 15. "
				"Most diamagnetic of all metals and has the lowest thermal "
				"conductivity of all the elements except mercury. Lead-free bismuth "
				"compounds are used in cosmetics and medical procedures. Burns in "
				"the air and produces a blue flame. In 1753, C.G. Junine first "
				"demonstrated that it was different from lead."
				)
		)

Mc = Element(
		115,
		"Mc",
		"Moscovium",
		group=15,
		period=7,
		block='p',
		series=8,
		isotopes={
				287: (287.19119, 0.0),
				288: (288.19249, 0.0),
				289: (289.19272, 0.0),
				290: (290.19414, 0.0),
				291: (291.19438, 0.0),
				}
		)
