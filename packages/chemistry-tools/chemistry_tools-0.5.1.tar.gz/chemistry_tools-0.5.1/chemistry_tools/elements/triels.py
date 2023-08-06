#!/usr/bin/env python3
#
#  triels.py
r"""
Group 13: Triels (or boron group) in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: B

	:class:`~chemistry_tools.elements.classes.Element` representing Boron

.. data:: Al

	:class:`~chemistry_tools.elements.classes.Element` representing Aluminium

.. data:: Ga

	:class:`~chemistry_tools.elements.classes.Element` representing Gallium

.. data:: In

	:class:`~chemistry_tools.elements.classes.Element` representing Indium

.. data:: Tl

	:class:`~chemistry_tools.elements.classes.Element` representing Thallium

.. data:: Nh

	:class:`~chemistry_tools.elements.classes.Element` representing Nihonium

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

__all__ = ('B', "Al", "Ga", "In", "Tl", "Nh")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

B = Element(
		5,
		'B',
		"Boron",
		group=13,
		period=2,
		block='p',
		series=5,
		mass=10.811,
		eleneg=2.04,
		eleaffin=0.279723,
		covrad=0.82,
		atmrad=1.17,
		vdwrad=0.0,
		tboil=4275.0,
		tmelt=2365.0,
		density=2.46,
		eleconfig="[He] 2s2 2p",
		oxistates="3*",
		ionenergy=(8.298, 25.154, 37.93, 59.368, 340.217),
		isotopes={
				6: (6.04681, 0.0),
				7: (7.02992, 0.0),
				8: (8.0246072, 0.0),
				9: (9.0133288, 0.0),
				10: (10.012937, 0.199),
				11: (11.0093054, 0.801),
				12: (12.0143521, 0.0),
				13: (13.0177802, 0.0),
				14: (14.025404, 0.0),
				15: (15.031103, 0.0),
				16: (16.03981, 0.0),
				17: (17.04699, 0.0),
				18: (18.05617, 0.0),
				19: (19.06373, 0.0),
				},
		description=(
				"An element of group 13 of the periodic table. There are two "
				"allotropes, amorphous boron is a brown power, but metallic boron is "
				"black. The metallic form is hard (9.3 on Mohs' scale) and a bad "
				"conductor in room temperatures. It is never found free in nature. "
				"Boron-10 is used in nuclear reactor control rods and shields. It "
				"was discovered in 1808 by Sir Humphry Davy and by J.L. Gay-Lussac "
				"and L.J. Thenard."
				)
		)

Al = Element(
		13,
		"Al",
		"Aluminium",
		group=13,
		period=3,
		block='p',
		series=7,
		mass=26.9815385,
		eleneg=1.61,
		eleaffin=0.43283,
		covrad=1.18,
		atmrad=1.82,
		vdwrad=0.0,
		tboil=2740.0,
		tmelt=933.5,
		density=2.7,
		eleconfig="[Ne] 3s2 3p",
		oxistates="3*",
		ionenergy=(
				5.9858,
				18.828,
				28.447,
				119.99,
				153.71,
				190.47,
				241.43,
				284.59,
				330.21,
				398.57,
				442.07,
				2085.983,
				2304.08,
				),
		isotopes={
				21: (21.02804, 0.0),
				22: (22.01952, 0.0),
				23: (23.007267, 0.0),
				24: (23.9999389, 0.0),
				25: (24.9904281, 0.0),
				26: (25.98689169, 0.0),
				27: (26.98153863, 1.0),
				28: (27.98191031, 0.0),
				29: (28.980445, 0.0),
				30: (29.98296, 0.0),
				31: (30.983947, 0.0),
				32: (31.98812, 0.0),
				33: (32.99084, 0.0),
				34: (33.99685, 0.0),
				35: (34.99986, 0.0),
				36: (36.00621, 0.0),
				37: (37.01068, 0.0),
				38: (38.01723, 0.0),
				39: (39.02297, 0.0),
				40: (40.03145, 0.0),
				41: (41.03833, 0.0),
				42: (42.04689, 0.0),
				},
		description=(
				"Silvery-white lustrous metallic element of group 3 of the periodic "
				"table. Highly reactive but protected by a thin transparent layer of "
				"the oxide which quickly forms in air. There are many alloys of "
				"aluminum, as well as a good number of industrial uses. Makes up "
				"8.1% of the Earth's crust, by weight. Isolated in 1825 by H.C. "
				"Oersted."
				)
		)

Ga = Element(
		31,
		"Ga",
		"Gallium",
		group=13,
		period=4,
		block='p',
		series=7,
		mass=69.723,
		eleneg=1.81,
		eleaffin=0.41,
		covrad=1.26,
		atmrad=1.81,
		vdwrad=1.87,
		tboil=2478.0,
		tmelt=302.92,
		density=5.91,
		eleconfig="[Ar] 3d10 4s2 4p",
		oxistates="3*",
		ionenergy=(5.9993, 20.51, 30.71, 64.0),
		isotopes={
				56: (55.99491, 0.0),
				57: (56.98293, 0.0),
				58: (57.97425, 0.0),
				59: (58.96337, 0.0),
				60: (59.95706, 0.0),
				61: (60.94945, 0.0),
				62: (61.944175, 0.0),
				63: (62.9392942, 0.0),
				64: (63.9368387, 0.0),
				65: (64.9327348, 0.0),
				66: (65.931589, 0.0),
				67: (66.9282017, 0.0),
				68: (67.9279801, 0.0),
				69: (68.9255736, 0.60108),
				70: (69.926022, 0.0),
				71: (70.9247013, 0.39892),
				72: (71.9263663, 0.0),
				73: (72.9251747, 0.0),
				74: (73.926946, 0.0),
				75: (74.9265002, 0.0),
				76: (75.9288276, 0.0),
				77: (76.9291543, 0.0),
				78: (77.9316082, 0.0),
				79: (78.93289, 0.0),
				80: (79.93652, 0.0),
				81: (80.93775, 0.0),
				82: (81.94299, 0.0),
				83: (82.94698, 0.0),
				84: (83.95265, 0.0),
				85: (84.957, 0.0),
				86: (85.96312, 0.0),
				},
		description=(
				"Soft silvery metallic element, belongs to group 13 of the periodic "
				"table. The two stable isotopes are Ga-69 and Ga-71. Eight "
				"radioactive isotopes are known, all having short half-lives. "
				"Gallium Arsenide is used as a semiconductor. Corrodes most other "
				"metals by diffusing into their lattice. First identified by "
				"Francois Lecoq de Boisbaudran in 1875."
				)
		)

In = Element(
		49,
		"In",
		"Indium",
		group=13,
		period=5,
		block='p',
		series=7,
		mass=114.818,
		eleneg=1.78,
		eleaffin=0.404,
		covrad=1.44,
		atmrad=2.0,
		vdwrad=1.93,
		tboil=2350.0,
		tmelt=429.78,
		density=7.31,
		eleconfig="[Kr] 4d10 5s2 5p",
		oxistates="3*",
		ionenergy=(5.7864, 18.869, 28.03, 55.45),
		isotopes={
				97: (96.94954, 0.0),
				98: (97.94214, 0.0),
				99: (98.93422, 0.0),
				100: (99.93111, 0.0),
				101: (100.92634, 0.0),
				102: (101.92409, 0.0),
				103: (102.919914, 0.0),
				104: (103.9183, 0.0),
				105: (104.914674, 0.0),
				106: (105.913465, 0.0),
				107: (106.910295, 0.0),
				108: (107.909698, 0.0),
				109: (108.907151, 0.0),
				110: (109.907165, 0.0),
				111: (110.905103, 0.0),
				112: (111.905532, 0.0),
				113: (112.904058, 0.0429),
				114: (113.904914, 0.0),
				115: (114.903878, 0.9571),
				116: (115.90526, 0.0),
				117: (116.904514, 0.0),
				118: (117.906354, 0.0),
				119: (118.905845, 0.0),
				120: (119.90796, 0.0),
				121: (120.907846, 0.0),
				122: (121.91028, 0.0),
				123: (122.910438, 0.0),
				124: (123.91318, 0.0),
				125: (124.9136, 0.0),
				126: (125.91646, 0.0),
				127: (126.91735, 0.0),
				128: (127.92017, 0.0),
				129: (128.9217, 0.0),
				130: (129.92497, 0.0),
				131: (130.92685, 0.0),
				132: (131.93299, 0.0),
				133: (132.93781, 0.0),
				134: (133.94415, 0.0),
				135: (134.94933, 0.0),
				},
		description=(
				"Soft silvery element belonging to group 13 of the periodic table. "
				"The most common natural isotope is In-115, which has a half-life of "
				"6*10^4 years. Five other radioisotopes exist. Discovered in 1863 by "
				"Reich and Richter."
				)
		)

Tl = Element(
		81,
		"Tl",
		"Thallium",
		group=13,
		period=6,
		block='p',
		series=7,
		mass=204.3834,
		eleneg=2.04,
		eleaffin=0.377,
		covrad=1.48,
		atmrad=2.08,
		vdwrad=1.96,
		tboil=1746.0,
		tmelt=577.0,
		density=11.85,
		eleconfig="[Xe] 4f14 5d10 6s2 6p",
		oxistates="3, 1*",
		ionenergy=(6.1082, 20.428, 29.83),
		isotopes={
				176: (176.00059, 0.0),
				177: (176.996427, 0.0),
				178: (177.9949, 0.0),
				179: (178.99109, 0.0),
				180: (179.98991, 0.0),
				181: (180.986257, 0.0),
				182: (181.98567, 0.0),
				183: (182.982193, 0.0),
				184: (183.98187, 0.0),
				185: (184.97879, 0.0),
				186: (185.97833, 0.0),
				187: (186.975906, 0.0),
				188: (187.97601, 0.0),
				189: (188.973588, 0.0),
				190: (189.97388, 0.0),
				191: (190.971786, 0.0),
				192: (191.97223, 0.0),
				193: (192.97067, 0.0),
				194: (193.9712, 0.0),
				195: (194.969774, 0.0),
				196: (195.970481, 0.0),
				197: (196.969575, 0.0),
				198: (197.97048, 0.0),
				199: (198.96988, 0.0),
				200: (199.970963, 0.0),
				201: (200.970819, 0.0),
				202: (201.972106, 0.0),
				203: (202.9723442, 0.2952),
				204: (203.9738635, 0.0),
				205: (204.9744275, 0.7048),
				206: (205.9761103, 0.0),
				207: (206.977419, 0.0),
				208: (207.9820187, 0.0),
				209: (208.985359, 0.0),
				210: (209.990074, 0.0),
				211: (210.99348, 0.0),
				212: (211.99823, 0.0),
				},
		description=(
				"Pure, unreacted thallium appears silvery-white and exhibits a "
				"metallic lustre. Upon reacting with air, it begins to turn "
				"bluish-grey and looks like lead. It is very malleable, and can be "
				"cut with a knife. There are two stable isotopes, and four "
				"radioisotopes, Tl-204 being the most stable with a half-life of "
				"3.78 years. Thallium sulphate was used as a rodenticide. Thallium "
				"sulphine's conductivity changes with exposure to infrared light, "
				"this gives it a use in infrared detectors. Discovered by Sir "
				"William Crookes via spectroscopy. Its name comes from the Greek "
				"word thallos, which means green twig. Thallium and its compounds "
				"are toxic and can cause cancer."
				)
		)

Nh = Element(
		113,
		"Nh",
		"Nihonium",
		group=13,
		period=7,
		block='p',
		series=8,
		isotopes={
				283: (283.17645, 0.0),
				284: (284.17808, 0.0),
				285: (285.17873, 0.0),
				286: (286.18048, 0.0),
				287: (287.18105, 0.0),
				}
		)
