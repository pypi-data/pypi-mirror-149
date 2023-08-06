#!/usr/bin/env python3
#
#  halogens.py
r"""
Group 17: Halogens in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: F

	:class:`~chemistry_tools.elements.classes.Element` representing Fluorine

.. data:: Cl

	:class:`~chemistry_tools.elements.classes.Element` representing Chlorine

.. data:: Br

	:class:`~chemistry_tools.elements.classes.Element` representing Bromine

.. data:: I

	:class:`~chemistry_tools.elements.classes.Element` representing Iodine

.. data:: At

	:class:`~chemistry_tools.elements.classes.Element` representing Astatine

.. data:: Ts

	:class:`~chemistry_tools.elements.classes.Element` representing Tennessine

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

__all__ = ('F', "Cl", "Br", 'I', "At", "Ts")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

F = Element(
		9,
		'F',
		"Fluorine",
		group=17,
		period=2,
		block='p',
		series=6,
		mass=18.998403163,
		eleneg=3.98,
		eleaffin=3.4011887,
		covrad=0.72,
		atmrad=0.57,
		vdwrad=1.47,
		tboil=85.0,
		tmelt=53.55,
		density=1.58,
		eleconfig="[He] 2s2 2p5",
		oxistates="-1*",
		ionenergy=(
				17.4228,
				34.97,
				62.707,
				87.138,
				114.24,
				157.161,
				185.182,
				953.886,
				1103.089,
				),
		isotopes={
				14: (14.03506, 0.0),
				15: (15.01801, 0.0),
				16: (16.011466, 0.0),
				17: (17.00209524, 0.0),
				18: (18.000938, 0.0),
				19: (18.99840322, 1.0),
				20: (19.99998132, 0.0),
				21: (20.999949, 0.0),
				22: (22.002999, 0.0),
				23: (23.00357, 0.0),
				24: (24.00812, 0.0),
				25: (25.0121, 0.0),
				26: (26.01962, 0.0),
				27: (27.02676, 0.0),
				28: (28.03567, 0.0),
				29: (29.04326, 0.0),
				30: (30.0525, 0.0),
				31: (31.06043, 0.0),
				},
		description=(
				"A poisonous pale yellow gaseous element belonging to group 17 of "
				"the periodic table (The halogens). It is the most chemically "
				"reactive and electronegative element. It is highly dangerous, "
				"causing severe chemical burns on contact with flesh. Fluorine was "
				"identified by Scheele in 1771 and first isolated by Moissan in "
				"1886."
				)
		)

Cl = Element(
		17,
		"Cl",
		"Chlorine",
		group=17,
		period=3,
		block='p',
		series=6,
		mass=35.4529,
		eleneg=3.16,
		eleaffin=3.612724,
		covrad=0.99,
		atmrad=0.97,
		vdwrad=1.75,
		tboil=239.18,
		tmelt=172.17,
		density=2.95,
		eleconfig="[Ne] 3s2 3p5",
		oxistates="7, 5, 3, 1, -1*",
		ionenergy=(
				12.9676,
				23.81,
				39.61,
				53.46,
				67.8,
				98.03,
				114.193,
				348.28,
				400.05,
				455.62,
				529.97,
				591.97,
				656.69,
				749.75,
				809.39,
				3658.425,
				3946.193,
				),
		isotopes={
				28: (28.02851, 0.0),
				29: (29.01411, 0.0),
				30: (30.00477, 0.0),
				31: (30.99241, 0.0),
				32: (31.98569, 0.0),
				33: (32.9774519, 0.0),
				34: (33.97376282, 0.0),
				35: (34.96885268, 0.7576),
				36: (35.96830698, 0.0),
				37: (36.96590259, 0.2424),
				38: (37.96801043, 0.0),
				39: (38.9680082, 0.0),
				40: (39.97042, 0.0),
				41: (40.97068, 0.0),
				42: (41.97325, 0.0),
				43: (42.97405, 0.0),
				44: (43.97828, 0.0),
				45: (44.98029, 0.0),
				46: (45.98421, 0.0),
				47: (46.98871, 0.0),
				48: (47.99495, 0.0),
				49: (49.00032, 0.0),
				50: (50.00784, 0.0),
				51: (51.01449, 0.0),
				},
		description=(
				"Halogen element. Poisonous greenish-yellow gas. Occurs widely in "
				"nature as sodium chloride in seawater. Reacts directly with many "
				"elements and compounds, strong oxidizing agent. Discovered by Karl "
				"Scheele in 1774. Humphrey David confirmed it as an element in 1810."
				)
		)

Br = Element(
		35,
		"Br",
		"Bromine",
		group=17,
		period=4,
		block='p',
		series=6,
		mass=79.9035,
		eleneg=2.96,
		eleaffin=3.363588,
		covrad=1.14,
		atmrad=1.12,
		vdwrad=1.85,
		tboil=331.85,
		tmelt=265.95,
		density=3.14,
		eleconfig="[Ar] 3d10 4s2 4p5",
		oxistates="7, 5, 3, 1, -1*",
		ionenergy=(
				11.8138,
				21.8,
				36.0,
				47.3,
				59.7,
				88.6,
				103.0,
				192.8,
				),
		isotopes={
				67: (66.96479, 0.0),
				68: (67.95852, 0.0),
				69: (68.95011, 0.0),
				70: (69.94479, 0.0),
				71: (70.93874, 0.0),
				72: (71.93664, 0.0),
				73: (72.93169, 0.0),
				74: (73.929891, 0.0),
				75: (74.925776, 0.0),
				76: (75.924541, 0.0),
				77: (76.921379, 0.0),
				78: (77.921146, 0.0),
				79: (78.9183371, 0.5069),
				80: (79.9185293, 0.0),
				81: (80.9162906, 0.4931),
				82: (81.9168041, 0.0),
				83: (82.91518, 0.0),
				84: (83.916479, 0.0),
				85: (84.915608, 0.0),
				86: (85.918798, 0.0),
				87: (86.920711, 0.0),
				88: (87.92407, 0.0),
				89: (88.92639, 0.0),
				90: (89.93063, 0.0),
				91: (90.93397, 0.0),
				92: (91.93926, 0.0),
				93: (92.94305, 0.0),
				94: (93.94868, 0.0),
				95: (94.95287, 0.0),
				96: (95.95853, 0.0),
				97: (96.9628, 0.0),
				},
		description=(
				"Halogen element. Red volatile liquid at room temperature. Its "
				"reactivity is somewhere between chlorine and iodine. Harmful to "
				"human tissue in a liquid state, the vapour irritates eyes and "
				"throat. Discovered in 1826 by Antoine Balard."
				)
		)

I = Element(
		53,
		'I',
		"Iodine",
		group=17,
		period=5,
		block='p',
		series=6,
		mass=126.90447,
		eleneg=2.66,
		eleaffin=3.059038,
		covrad=1.33,
		atmrad=1.32,
		vdwrad=1.98,
		tboil=457.5,
		tmelt=386.7,
		density=4.94,
		eleconfig="[Kr] 4d10 5s2 5p5",
		oxistates="7, 5, 1, -1*",
		ionenergy=(10.4513, 19.131, 33.0),
		isotopes={
				108: (107.94348, 0.0),
				109: (108.93815, 0.0),
				110: (109.93524, 0.0),
				111: (110.93028, 0.0),
				112: (111.92797, 0.0),
				113: (112.92364, 0.0),
				114: (113.92185, 0.0),
				115: (114.91805, 0.0),
				116: (115.91681, 0.0),
				117: (116.91365, 0.0),
				118: (117.913074, 0.0),
				119: (118.91007, 0.0),
				120: (119.910048, 0.0),
				121: (120.907367, 0.0),
				122: (121.907589, 0.0),
				123: (122.905589, 0.0),
				124: (123.9062099, 0.0),
				125: (124.9046302, 0.0),
				126: (125.905624, 0.0),
				127: (126.904473, 1.0),
				128: (127.905809, 0.0),
				129: (128.904988, 0.0),
				130: (129.906674, 0.0),
				131: (130.9061246, 0.0),
				132: (131.907997, 0.0),
				133: (132.907797, 0.0),
				134: (133.909744, 0.0),
				135: (134.910048, 0.0),
				136: (135.91465, 0.0),
				137: (136.917871, 0.0),
				138: (137.92235, 0.0),
				139: (138.9261, 0.0),
				140: (139.931, 0.0),
				141: (140.93503, 0.0),
				142: (141.94018, 0.0),
				143: (142.94456, 0.0),
				144: (143.94999, 0.0),
				},
		description=(
				"Dark violet nonmetallic element, belongs to group 17 of the "
				"periodic table. Insoluble in water. Required as a trace element for "
				"living organisms. One stable isotope, I-127 exists, in addition to "
				"fourteen radioactive isotopes. Chemically the least reactive of the "
				"halogens, and the most electropositive metallic halogen. Discovered "
				"in 1812 by Courtois."
				)
		)

At = Element(
		85,
		"At",
		"Astatine",
		group=17,
		period=6,
		block='p',
		series=6,
		mass=209.9871,
		eleneg=2.2,
		eleaffin=2.8,
		covrad=1.45,
		atmrad=1.43,
		vdwrad=0.0,
		tboil=610.0,
		tmelt=575.0,
		density=0.0,
		eleconfig="[Xe] 4f14 5d10 6s2 6p5",
		oxistates="7, 5, 3, 1, -1*",
		ionenergy=(),
		isotopes={
				193: (192.99984, 0.0),
				194: (193.99873, 0.0),
				195: (194.996268, 0.0),
				196: (195.99579, 0.0),
				197: (196.99319, 0.0),
				198: (197.99284, 0.0),
				199: (198.99053, 0.0),
				200: (199.990351, 0.0),
				201: (200.988417, 0.0),
				202: (201.98863, 0.0),
				203: (202.986942, 0.0),
				204: (203.987251, 0.0),
				205: (204.986074, 0.0),
				206: (205.986667, 0.0),
				207: (206.985784, 0.0),
				208: (207.98659, 0.0),
				209: (208.986173, 0.0),
				210: (209.987148, 0.0),
				211: (210.9874963, 0.0),
				212: (211.990745, 0.0),
				213: (212.992937, 0.0),
				214: (213.996372, 0.0),
				215: (214.998653, 0.0),
				216: (216.002423, 0.0),
				217: (217.004719, 0.0),
				218: (218.008694, 0.0),
				219: (219.011162, 0.0),
				220: (220.01541, 0.0),
				221: (221.01805, 0.0),
				222: (222.02233, 0.0),
				223: (223.02519, 0.0),
				},
		description=(
				"Radioactive halogen element. Occurs naturally from uranium and "
				"thorium decay. At least 20 known isotopes. At-210, the most stable, "
				"has a half-life of 8.3 hours. Synthesized by nuclear bombardment in "
				"1940 by D.R. Corson, K.R. MacKenzie and E. Segre at the University "
				"of California."
				)
		)

Ts = Element(
		117,
		"Ts",
		"Tennessine",
		group=17,
		period=7,
		block='p',
		series=8,
		isotopes={
				291: (291.20656, 0.0),
				292: (292.20755, 0.0),
				}
		)
