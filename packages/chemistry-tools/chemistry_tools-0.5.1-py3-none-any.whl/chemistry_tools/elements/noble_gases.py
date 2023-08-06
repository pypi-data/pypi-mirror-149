#!/usr/bin/env python3
#
#  noble_gases.py
r"""
Group 18: Noble Gases in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: He

	:class:`~chemistry_tools.elements.classes.Element` representing Helium

.. data:: Ne

	:class:`~chemistry_tools.elements.classes.Element` representing Neon

.. data:: Ar

	:class:`~chemistry_tools.elements.classes.Element` representing Argon

.. data:: Kr

	:class:`~chemistry_tools.elements.classes.Element` representing Krypton

.. data:: Xe

	:class:`~chemistry_tools.elements.classes.Element` representing Xenon

.. data:: Rn

	:class:`~chemistry_tools.elements.classes.Element` representing Radon

.. data:: Og

	:class:`~chemistry_tools.elements.classes.Element` representing Oganesson

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

__all__ = ("He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

He = Element(
		2,
		"He",
		"Helium",
		group=18,
		period=1,
		block='s',
		series=2,
		mass=4.002602,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.93,
		atmrad=0.49,
		vdwrad=1.4,
		tboil=4.216,
		tmelt=0.95,
		density=0.1785,
		eleconfig="1s2",
		oxistates='*',
		ionenergy=(24.5874, 54.416),
		isotopes={
				3: (3.0160293191, 1.34e-06),
				4: (4.00260325415, 0.99999866),
				5: (5.01222, 0.0),
				6: (6.0188891, 0.0),
				7: (7.028021, 0.0),
				8: (8.033922, 0.0),
				9: (9.04395, 0.0),
				10: (10.0524, 0.0),
				},
		description=(
				"Colourless, odourless gaseous nonmetallic element. Belongs to "
				"group 18 of the periodic table. Lowest boiling point of all "
				"elements and can only be solidified under pressure. Chemically "
				"inert, no known compounds. Discovered in the solar spectrum in 1868 "
				"by Lockyer."
				)
		)

Ne = Element(
		10,
		"Ne",
		"Neon",
		group=18,
		period=2,
		block='p',
		series=2,
		mass=20.1797,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.71,
		atmrad=0.51,
		vdwrad=1.54,
		tboil=27.1,
		tmelt=24.55,
		density=0.8999,
		eleconfig="[He] 2s2 2p6",
		oxistates='*',
		ionenergy=(
				21.5645,
				40.962,
				63.45,
				97.11,
				126.21,
				157.93,
				207.27,
				239.09,
				1195.797,
				1362.164,
				),
		isotopes={
				16: (16.025761, 0.0),
				17: (17.017672, 0.0),
				18: (18.0057082, 0.0),
				19: (19.0018802, 0.0),
				20: (19.9924401754, 0.9048),
				21: (20.99384668, 0.0027),
				22: (21.991385114, 0.0925),
				23: (22.9944669, 0.0),
				24: (23.9936108, 0.0),
				25: (24.997737, 0.0),
				26: (26.000461, 0.0),
				27: (27.00759, 0.0),
				28: (28.01207, 0.0),
				29: (29.01939, 0.0),
				30: (30.0248, 0.0),
				31: (31.03311, 0.0),
				32: (32.04002, 0.0),
				33: (33.04938, 0.0),
				34: (34.05703, 0.0),
				},
		description=(
				"Colourless gaseous element of group 18 on the periodic table "
				"(noble gases). Neon occurs in the atmosphere, and comprises 0.0018% "
				"of the volume of the atmosphere. It has a distinct reddish glow "
				"when used in discharge tubes and neon based lamps. It forms almost "
				"no chemical compounds. Neon was discovered in 1898 by Sir William "
				"Ramsey and M.W. Travers."
				)
		)

Ar = Element(
		18,
		"Ar",
		"Argon",
		group=18,
		period=3,
		block='p',
		series=2,
		mass=39.948,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.98,
		atmrad=0.88,
		vdwrad=1.88,
		tboil=87.45,
		tmelt=83.95,
		density=1.66,
		eleconfig="[Ne] 3s2 3p6",
		oxistates='*',
		ionenergy=(
				15.7596,
				27.629,
				40.74,
				59.81,
				75.02,
				91.007,
				124.319,
				143.456,
				422.44,
				478.68,
				538.95,
				618.24,
				686.09,
				755.73,
				854.75,
				918.0,
				4120.778,
				4426.114,
				),
		isotopes={
				30: (30.02156, 0.0),
				31: (31.01212, 0.0),
				32: (31.997638, 0.0),
				33: (32.9899257, 0.0),
				34: (33.9802712, 0.0),
				35: (34.9752576, 0.0),
				36: (35.967545106, 0.003365),
				37: (36.96677632, 0.0),
				38: (37.9627324, 0.000632),
				39: (38.964313, 0.0),
				40: (39.9623831225, 0.996003),
				41: (40.9645006, 0.0),
				42: (41.963046, 0.0),
				43: (42.965636, 0.0),
				44: (43.964924, 0.0),
				45: (44.96804, 0.0),
				46: (45.96809, 0.0),
				47: (46.97219, 0.0),
				48: (47.97454, 0.0),
				49: (48.98052, 0.0),
				50: (49.98443, 0.0),
				51: (50.99163, 0.0),
				52: (51.99678, 0.0),
				53: (53.00494, 0.0),
				},
		description=(
				"Monatomic noble gas. Makes up 0.93% of the air. Colourless, "
				"odorless. Is inert and has no true compounds. Lord Rayleigh and Sir "
				"william Ramsey identified argon in 1894."
				)
		)

Kr = Element(
		36,
		"Kr",
		"Krypton",
		group=18,
		period=4,
		block='p',
		series=2,
		mass=83.798,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=1.12,
		atmrad=1.03,
		vdwrad=2.02,
		tboil=120.85,
		tmelt=116.0,
		density=4.48,
		eleconfig="[Ar] 3d10 4s2 4p6",
		oxistates="2*",
		ionenergy=(
				13.9996,
				24.359,
				36.95,
				52.5,
				64.7,
				78.5,
				110.0,
				126.0,
				230.39,
				),
		isotopes={
				69: (68.96518, 0.0),
				70: (69.95526, 0.0),
				71: (70.94963, 0.0),
				72: (71.942092, 0.0),
				73: (72.939289, 0.0),
				74: (73.9330844, 0.0),
				75: (74.930946, 0.0),
				76: (75.92591, 0.0),
				77: (76.92467, 0.0),
				78: (77.9203648, 0.00355),
				79: (78.920082, 0.0),
				80: (79.916379, 0.02286),
				81: (80.916592, 0.0),
				82: (81.9134836, 0.11593),
				83: (82.914136, 0.115),
				84: (83.911507, 0.56987),
				85: (84.9125273, 0.0),
				86: (85.91061073, 0.17279),
				87: (86.91335486, 0.0),
				88: (87.914447, 0.0),
				89: (88.91763, 0.0),
				90: (89.919517, 0.0),
				91: (90.92345, 0.0),
				92: (91.926156, 0.0),
				93: (92.93127, 0.0),
				94: (93.93436, 0.0),
				95: (94.93984, 0.0),
				96: (95.94307, 0.0),
				97: (96.94856, 0.0),
				98: (97.95191, 0.0),
				99: (98.9576, 0.0),
				100: (99.96114, 0.0),
				},
		description=(
				"Colorless gaseous element, belongs to the noble gases. Occurs in "
				"the air, 0.0001% by volume. It can be extracted from liquid air by "
				"fractional distillation. Generally not isolated, but used with "
				"other inert gases in fluorescent lamps. Five natural isotopes, and "
				"five radioactive isotopes. Kr-85, the most stable radioactive "
				"isotope, has a half-life of 10.76 years and is produced in fission "
				"reactors. Practically inert, though known to form compounds with "
				"Fluorine."
				)
		)

Xe = Element(
		54,
		"Xe",
		"Xenon",
		group=18,
		period=5,
		block='p',
		series=2,
		mass=131.293,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=1.31,
		atmrad=1.24,
		vdwrad=2.16,
		tboil=165.1,
		tmelt=161.39,
		density=4.49,
		eleconfig="[Kr] 4d10 5s2 5p6",
		oxistates="2, 4, 6",
		ionenergy=(12.1298, 21.21, 32.1),
		isotopes={
				110: (109.94428, 0.0),
				111: (110.9416, 0.0),
				112: (111.93562, 0.0),
				113: (112.93334, 0.0),
				114: (113.92798, 0.0),
				115: (114.926294, 0.0),
				116: (115.921581, 0.0),
				117: (116.920359, 0.0),
				118: (117.916179, 0.0),
				119: (118.915411, 0.0),
				120: (119.911784, 0.0),
				121: (120.911462, 0.0),
				122: (121.908368, 0.0),
				123: (122.908482, 0.0),
				124: (123.905893, 0.000952),
				125: (124.9063955, 0.0),
				126: (125.904274, 0.00089),
				127: (126.905184, 0.0),
				128: (127.9035313, 0.019102),
				129: (128.9047794, 0.264006),
				130: (129.903508, 0.04071),
				131: (130.9050824, 0.212324),
				132: (131.9041535, 0.269086),
				133: (132.9059107, 0.0),
				134: (133.9053945, 0.104357),
				135: (134.907227, 0.0),
				136: (135.907219, 0.088573),
				137: (136.911562, 0.0),
				138: (137.91395, 0.0),
				139: (138.918793, 0.0),
				140: (139.92164, 0.0),
				141: (140.92665, 0.0),
				142: (141.92971, 0.0),
				143: (142.93511, 0.0),
				144: (143.93851, 0.0),
				145: (144.94407, 0.0),
				146: (145.94775, 0.0),
				147: (146.95356, 0.0),
				},
		description=(
				"Colourless, odourless gas belonging to group 18 on the periodic "
				"table (the noble gases.) Nine natural isotopes and seven "
				"radioactive isotopes are known. Xenon was part of the first "
				"noble-gas compound synthesized. Several others involving Xenon have "
				"been found since then. Xenon was discovered by Ramsey and Travers "
				"in 1898."
				)
		)

Rn = Element(
		86,
		"Rn",
		"Radon",
		group=18,
		period=6,
		block='p',
		series=2,
		mass=222.0176,
		eleneg=0.0,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=1.34,
		vdwrad=0.0,
		tboil=211.4,
		tmelt=202.0,
		density=9.23,
		eleconfig="[Xe] 4f14 5d10 6s2 6p6",
		oxistates="2*",
		ionenergy=(10.7485, ),
		isotopes={
				195: (195.00544, 0.0),
				196: (196.002115, 0.0),
				197: (197.00158, 0.0),
				198: (197.998679, 0.0),
				199: (198.99837, 0.0),
				200: (199.995699, 0.0),
				201: (200.99563, 0.0),
				202: (201.993263, 0.0),
				203: (202.993387, 0.0),
				204: (203.991429, 0.0),
				205: (204.99172, 0.0),
				206: (205.990214, 0.0),
				207: (206.990734, 0.0),
				208: (207.989642, 0.0),
				209: (208.990415, 0.0),
				210: (209.989696, 0.0),
				211: (210.990601, 0.0),
				212: (211.990704, 0.0),
				213: (212.993883, 0.0),
				214: (213.995363, 0.0),
				215: (214.998745, 0.0),
				216: (216.000274, 0.0),
				217: (217.003928, 0.0),
				218: (218.0056013, 0.0),
				219: (219.0094802, 0.0),
				220: (220.011394, 0.0),
				221: (221.015537, 0.0),
				222: (222.0175777, 0.0),
				223: (223.02179, 0.0),
				224: (224.02409, 0.0),
				225: (225.02844, 0.0),
				226: (226.03089, 0.0),
				227: (227.03541, 0.0),
				228: (228.03799, 0.0),
				},
		description=(
				"Colorless radioactive gaseous element, belongs to the noble gases. "
				"Of the twenty known isotopes, the most stable is Rn-222 with a "
				"half-life of 3.8 days. Formed by the radioactive decay of "
				"Radium-226. Radon itself decays into Polonium. Used in "
				"radiotherapy. As a noble gas, it is effectively inert, though radon "
				"fluoride has been synthesized. First isolated in 1908 by Ramsey and "
				"Gray."
				),
		)

Og = Element(
		118,
		"Og",
		"Oganesson",
		group=18,
		period=7,
		block='p',
		series=8,
		isotopes={
				293: (293.21467, 0.0),
				},
		)
