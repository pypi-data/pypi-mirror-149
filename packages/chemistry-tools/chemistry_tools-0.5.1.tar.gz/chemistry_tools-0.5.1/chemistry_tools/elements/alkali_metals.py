#!/usr/bin/env python3
#
#  alkali_metals.py
r"""
Group 1: Alkali Metals in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: Li

	:class:`~chemistry_tools.elements.classes.Element` representing Lithium

.. data:: Na

	:class:`~chemistry_tools.elements.classes.Element` representing Sodium

.. data:: K

	:class:`~chemistry_tools.elements.classes.Element` representing Potassium

.. data:: Rb

	:class:`~chemistry_tools.elements.classes.Element` representing Rubidium

.. data:: Cs

	:class:`~chemistry_tools.elements.classes.Element` representing Caesium

.. data:: Fr

	:class:`~chemistry_tools.elements.classes.Element` representing Francium

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

__all__ = ("Li", "Na", 'K', "Rb", "Cs", "Fr")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

Li = Element(
		3,
		"Li",
		"Lithium",
		group=1,
		period=2,
		block='s',
		series=3,
		mass=6.94,
		eleneg=0.98,
		eleaffin=0.618049,
		covrad=1.23,
		atmrad=2.05,
		vdwrad=1.82,
		tboil=1615.0,
		tmelt=453.7,
		density=0.53,
		eleconfig="[He] 2s",
		oxistates="1*",
		ionenergy=(5.3917, 75.638, 122.451),
		isotopes={
				3: (3.03078, 0.0),
				4: (4.02719, 0.0),
				5: (5.01254, 0.0),
				6: (6.015122795, 0.0759),
				7: (7.01600455, 0.9241),
				8: (8.02248736, 0.0),
				9: (9.0267895, 0.0),
				10: (10.035481, 0.0),
				11: (11.043798, 0.0),
				12: (12.05378, 0.0),
				},
		description=(
				"Socket silvery metal. First member of group 1 of the periodic "
				"table. Lithium salts are used in psychomedicine."
				)
		)

Na = Element(
		11,
		"Na",
		"Sodium",
		group=1,
		period=3,
		block='s',
		series=3,
		mass=22.98976928,
		eleneg=0.93,
		eleaffin=0.547926,
		covrad=1.54,
		atmrad=2.23,
		vdwrad=2.27,
		tboil=1156.0,
		tmelt=371.0,
		density=0.97,
		eleconfig="[Ne] 3s",
		oxistates="1*",
		ionenergy=(
				5.1391,
				47.286,
				71.64,
				98.91,
				138.39,
				172.15,
				208.47,
				264.18,
				299.87,
				1465.091,
				1648.659,
				),
		isotopes={
				18: (18.02597, 0.0),
				19: (19.013877, 0.0),
				20: (20.007351, 0.0),
				21: (20.9976552, 0.0),
				22: (21.9944364, 0.0),
				23: (22.9897692809, 1.0),
				24: (23.99096278, 0.0),
				25: (24.989954, 0.0),
				26: (25.992633, 0.0),
				27: (26.994077, 0.0),
				28: (27.998938, 0.0),
				29: (29.002861, 0.0),
				30: (30.008976, 0.0),
				31: (31.01359, 0.0),
				32: (32.02047, 0.0),
				33: (33.02672, 0.0),
				34: (34.03517, 0.0),
				35: (35.04249, 0.0),
				36: (36.05148, 0.0),
				37: (37.05934, 0.0),
				},
		description=(
				"Soft silvery reactive element belonging to group 1 of the periodic "
				"table (alkali metals). It is highly reactive, oxidizing in air and "
				"reacting violently with water, forcing it to be kept under oil. It "
				"was first isolated by Humphrey Davy in 1807."
				)
		)

K = Element(
		19,
		'K',
		"Potassium",
		group=1,
		period=4,
		block='s',
		series=3,
		mass=39.0983,
		eleneg=0.82,
		eleaffin=0.501459,
		covrad=2.03,
		atmrad=2.77,
		vdwrad=2.75,
		tboil=1033.0,
		tmelt=336.8,
		density=0.86,
		eleconfig="[Ar] 4s",
		oxistates="1*",
		ionenergy=(
				4.3407,
				31.625,
				45.72,
				60.91,
				82.66,
				100.0,
				117.56,
				154.86,
				175.814,
				503.44,
				564.13,
				629.09,
				714.02,
				787.13,
				861.77,
				968.0,
				1034.0,
				4610.955,
				4933.931,
				),
		isotopes={
				32: (32.02192, 0.0),
				33: (33.00726, 0.0),
				34: (33.99841, 0.0),
				35: (34.98801, 0.0),
				36: (35.981292, 0.0),
				37: (36.97337589, 0.0),
				38: (37.9690812, 0.0),
				39: (38.96370668, 0.932581),
				40: (39.96399848, 0.000117),
				41: (40.96182576, 0.067302),
				42: (41.96240281, 0.0),
				43: (42.960716, 0.0),
				44: (43.96156, 0.0),
				45: (44.960699, 0.0),
				46: (45.961977, 0.0),
				47: (46.961678, 0.0),
				48: (47.965514, 0.0),
				49: (48.96745, 0.0),
				50: (49.97278, 0.0),
				51: (50.97638, 0.0),
				52: (51.98261, 0.0),
				53: (52.98712, 0.0),
				54: (53.9942, 0.0),
				55: (54.99971, 0.0),
				},
		description=(
				"Soft silvery metallic element belonging to group 1 of the periodic "
				"table (alkali metals). Occurs naturally in seawater and a many "
				"minerals. Highly reactive, chemically, it resembles sodium in its "
				"behavior and compounds. Discovered by Sir Humphry Davy in 1807."
				)
		)

Rb = Element(
		37,
		"Rb",
		"Rubidium",
		group=1,
		period=5,
		block='s',
		series=3,
		mass=85.4678,
		eleneg=0.82,
		eleaffin=0.485916,
		covrad=2.16,
		atmrad=2.98,
		vdwrad=0.0,
		tboil=961.0,
		tmelt=312.63,
		density=1.53,
		eleconfig="[Kr] 5s",
		oxistates="1*",
		ionenergy=(
				4.1771,
				27.28,
				40.0,
				52.6,
				71.0,
				84.4,
				99.2,
				136.0,
				150.0,
				277.1,
				),
		isotopes={
				71: (70.96532, 0.0),
				72: (71.95908, 0.0),
				73: (72.95056, 0.0),
				74: (73.944265, 0.0),
				75: (74.93857, 0.0),
				76: (75.9350722, 0.0),
				77: (76.930408, 0.0),
				78: (77.928141, 0.0),
				79: (78.923989, 0.0),
				80: (79.922519, 0.0),
				81: (80.918996, 0.0),
				82: (81.9182086, 0.0),
				83: (82.91511, 0.0),
				84: (83.914385, 0.0),
				85: (84.911789738, 0.7217),
				86: (85.91116742, 0.0),
				87: (86.909180527, 0.2783),
				88: (87.91131559, 0.0),
				89: (88.912278, 0.0),
				90: (89.914802, 0.0),
				91: (90.916537, 0.0),
				92: (91.919729, 0.0),
				93: (92.922042, 0.0),
				94: (93.926405, 0.0),
				95: (94.929303, 0.0),
				96: (95.93427, 0.0),
				97: (96.93735, 0.0),
				98: (97.94179, 0.0),
				99: (98.94538, 0.0),
				100: (99.94987, 0.0),
				101: (100.9532, 0.0),
				102: (101.95887, 0.0),
				},
		description=(
				"Soft silvery metallic element, belongs to group 1 of the periodic "
				"table. Rb-97, the naturally occurring isotope, is radioactive. It "
				"is highly reactive, with properties similar to other elements in "
				"group 1, like igniting spontaneously in air. Discovered "
				"spectroscopically in 1861 by W. Bunsen and G.R. Kirchoff."
				)
		)

Cs = Element(
		55,
		"Cs",
		"Caesium",
		group=1,
		period=6,
		block='s',
		series=3,
		mass=132.90545196,
		eleneg=0.79,
		eleaffin=0.471626,
		covrad=2.35,
		atmrad=3.34,
		vdwrad=0.0,
		tboil=944.0,
		tmelt=301.54,
		density=1.9,
		eleconfig="[Xe] 6s",
		oxistates="1*",
		ionenergy=(3.8939, 25.1),
		isotopes={
				112: (111.9503, 0.0),
				113: (112.94449, 0.0),
				114: (113.94145, 0.0),
				115: (114.93591, 0.0),
				116: (115.93337, 0.0),
				117: (116.92867, 0.0),
				118: (117.926559, 0.0),
				119: (118.922377, 0.0),
				120: (119.920677, 0.0),
				121: (120.917229, 0.0),
				122: (121.91611, 0.0),
				123: (122.912996, 0.0),
				124: (123.912258, 0.0),
				125: (124.909728, 0.0),
				126: (125.909452, 0.0),
				127: (126.907418, 0.0),
				128: (127.907749, 0.0),
				129: (128.906064, 0.0),
				130: (129.906709, 0.0),
				131: (130.905464, 0.0),
				132: (131.9064343, 0.0),
				133: (132.905451933, 1.0),
				134: (133.906718475, 0.0),
				135: (134.905977, 0.0),
				136: (135.9073116, 0.0),
				137: (136.9070895, 0.0),
				138: (137.911017, 0.0),
				139: (138.913364, 0.0),
				140: (139.917282, 0.0),
				141: (140.920046, 0.0),
				142: (141.924299, 0.0),
				143: (142.927352, 0.0),
				144: (143.932077, 0.0),
				145: (144.935526, 0.0),
				146: (145.94029, 0.0),
				147: (146.94416, 0.0),
				148: (147.94922, 0.0),
				149: (148.95293, 0.0),
				150: (149.95817, 0.0),
				151: (150.96219, 0.0),
				},
		description=(
				"Soft silvery-white metallic element belonging to group 1 of the "
				"periodic table. One of the three metals which are liquid at room "
				"temperature. Cs-133 is the natural, and only stable, isotope. "
				"Fifteen other radioisotopes exist. Caesium reacts explosively with "
				"cold water, and ice at temperatures above 157K. Caesium hydroxide "
				"is the strongest base known. Caesium is the most electropositive, "
				"most alkaline and has the least ionization potential of all the "
				"elements. Known uses include the basis of atomic clocks, catalyst "
				"for the hydrogenation of some organic compounds, and in "
				"photoelectric cells. Caesium was discovered by Gustav Kirchoff and "
				"Robert Bunsen in Germany in 1860 spectroscopically. Its "
				"identification was based upon the bright blue lines in its "
				"spectrum. The name comes from the latin word caesius, which means "
				"sky blue. Caesium should be considered highly toxic. Some of the "
				"radioisotopes are even more toxic."
				)
		)

Fr = Element(
		87,
		"Fr",
		"Francium",
		group=1,
		period=7,
		block='s',
		series=3,
		mass=223.0197,
		eleneg=0.7,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=950.0,
		tmelt=300.0,
		density=0.0,
		eleconfig="[Rn] 7s",
		oxistates="1*",
		ionenergy=(4.0727, ),
		isotopes={
				199: (199.00726, 0.0),
				200: (200.00657, 0.0),
				201: (201.00386, 0.0),
				202: (202.00337, 0.0),
				203: (203.000925, 0.0),
				204: (204.000653, 0.0),
				205: (204.998594, 0.0),
				206: (205.99867, 0.0),
				207: (206.99695, 0.0),
				208: (207.99714, 0.0),
				209: (208.995954, 0.0),
				210: (209.996408, 0.0),
				211: (210.995537, 0.0),
				212: (211.996202, 0.0),
				213: (212.996189, 0.0),
				214: (213.998971, 0.0),
				215: (215.000341, 0.0),
				216: (216.003198, 0.0),
				217: (217.004632, 0.0),
				218: (218.007578, 0.0),
				219: (219.009252, 0.0),
				220: (220.012327, 0.0),
				221: (221.014255, 0.0),
				222: (222.017552, 0.0),
				223: (223.0197359, 0.0),
				224: (224.02325, 0.0),
				225: (225.02557, 0.0),
				226: (226.02939, 0.0),
				227: (227.03184, 0.0),
				228: (228.03573, 0.0),
				229: (229.03845, 0.0),
				230: (230.04251, 0.0),
				231: (231.04544, 0.0),
				232: (232.04977, 0.0),
				},
		description=(
				"Radioactive element, belongs to group 1 of the periodic table. "
				"Found in uranium and thorium ores. The 22 known isotopes are all "
				"radioactive, with the most stable being Fr-223. Its existence was "
				"confirmed in 1939 by Marguerite Perey."
				)
		)
