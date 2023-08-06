#!/usr/bin/env python3
#
#  alkaline_earth_metals.py
r"""
Group 2: Alkaline Earth Metals in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: Be

	:class:`~chemistry_tools.elements.classes.Element` representing Beryllium

.. data:: Mg

	:class:`~chemistry_tools.elements.classes.Element` representing Magnesium

.. data:: Ca

	:class:`~chemistry_tools.elements.classes.Element` representing Calcium

.. data:: Sr

	:class:`~chemistry_tools.elements.classes.Element` representing Strontium

.. data:: Ba

	:class:`~chemistry_tools.elements.classes.Element` representing Barium

.. data:: Ra

	:class:`~chemistry_tools.elements.classes.Element` representing Radium

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

__all__ = ("Be", "Mg", "Ca", "Sr", "Ba", "Ra")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

Be = Element(
		4,
		"Be",
		"Beryllium",
		group=2,
		period=2,
		block='s',
		series=4,
		mass=9.0121831,
		eleneg=1.57,
		eleaffin=0.0,
		covrad=0.9,
		atmrad=1.4,
		vdwrad=0.0,
		tboil=3243.0,
		tmelt=1560.0,
		density=1.85,
		eleconfig="[He] 2s2",
		oxistates="2*",
		ionenergy=(9.3227, 18.211, 153.893, 217.713),
		isotopes={
				5: (5.04079, 0.0),
				6: (6.019726, 0.0),
				7: (7.01692983, 0.0),
				8: (8.0053051, 0.0),
				9: (9.0121822, 1.0),
				10: (10.0135338, 0.0),
				11: (11.021658, 0.0),
				12: (12.026921, 0.0),
				13: (13.03569, 0.0),
				14: (14.04289, 0.0),
				15: (15.05346, 0.0),
				16: (16.06192, 0.0),
				},
		description=(
				"Grey metallic element of group 2 of the periodic table. Is toxic "
				"and can cause severe lung diseases and dermatitis. Shows high "
				"covalent character. It was isolated independently by F. Wohler and "
				"A.A. Bussy in 1828."
				)
		)

Mg = Element(
		12,
		"Mg",
		"Magnesium",
		group=2,
		period=3,
		block='s',
		series=4,
		mass=24.3051,
		eleneg=1.31,
		eleaffin=0.0,
		covrad=1.36,
		atmrad=1.72,
		vdwrad=1.73,
		tboil=1380.0,
		tmelt=922.0,
		density=1.74,
		eleconfig="[Ne] 3s2",
		oxistates="2*",
		ionenergy=(
				7.6462,
				15.035,
				80.143,
				109.24,
				141.26,
				186.5,
				224.94,
				265.9,
				327.95,
				367.53,
				1761.802,
				1962.613,
				),
		isotopes={
				19: (19.03547, 0.0),
				20: (20.018863, 0.0),
				21: (21.011713, 0.0),
				22: (21.9995738, 0.0),
				23: (22.9941237, 0.0),
				24: (23.9850417, 0.7899),
				25: (24.98583692, 0.1),
				26: (25.982592929, 0.1101),
				27: (26.98434059, 0.0),
				28: (27.9838768, 0.0),
				29: (28.9886, 0.0),
				30: (29.990434, 0.0),
				31: (30.996546, 0.0),
				32: (31.998975, 0.0),
				33: (33.005254, 0.0),
				34: (34.00946, 0.0),
				35: (35.01734, 0.0),
				36: (36.023, 0.0),
				37: (37.0314, 0.0),
				38: (38.03757, 0.0),
				39: (39.04677, 0.0),
				40: (40.05393, 0.0),
				},
		description=(
				"Silvery metallic element belonging to group 2 of the periodic "
				"table (alkaline-earth metals). It is essential for living "
				"organisms, and is used in a number of light alloys. Chemically very "
				"reactive, it forms a protective oxide coating when exposed to air "
				"and burns with an intense white flame. It also reacts with sulphur, "
				"nitrogen and the halogens. First isolated by Bussy in 1828."
				)
		)

Ca = Element(
		20,
		"Ca",
		"Calcium",
		group=2,
		period=4,
		block='s',
		series=4,
		mass=40.078,
		eleneg=1.0,
		eleaffin=0.02455,
		covrad=1.74,
		atmrad=2.23,
		vdwrad=0.0,
		tboil=1757.0,
		tmelt=1112.0,
		density=1.54,
		eleconfig="[Ar] 4s2",
		oxistates="2*",
		ionenergy=(
				6.1132,
				11.71,
				50.908,
				67.1,
				84.41,
				108.78,
				127.7,
				147.24,
				188.54,
				211.27,
				591.25,
				656.39,
				726.03,
				816.61,
				895.12,
				974.0,
				1087.0,
				1157.0,
				5129.045,
				5469.738,
				),
		isotopes={
				34: (34.01412, 0.0),
				35: (35.00494, 0.0),
				36: (35.99309, 0.0),
				37: (36.98587, 0.0),
				38: (37.976318, 0.0),
				39: (38.9707197, 0.0),
				40: (39.96259098, 0.96941),
				41: (40.96227806, 0.0),
				42: (41.95861801, 0.00647),
				43: (42.9587666, 0.00135),
				44: (43.9554818, 0.02086),
				45: (44.9561866, 0.0),
				46: (45.9536926, 4e-05),
				47: (46.954546, 0.0),
				48: (47.952534, 0.00187),
				49: (48.955674, 0.0),
				50: (49.957519, 0.0),
				51: (50.9615, 0.0),
				52: (51.9651, 0.0),
				53: (52.97005, 0.0),
				54: (53.97435, 0.0),
				55: (54.98055, 0.0),
				56: (55.98557, 0.0),
				57: (56.99236, 0.0),
				},
		description=(
				"Soft grey metallic element belonging to group 2 of the periodic "
				"table. Used a reducing agent in the extraction of thorium, "
				"zirconium and uranium. Essential element for living organisms."
				)
		)

Sr = Element(
		38,
		"Sr",
		"Strontium",
		group=2,
		period=5,
		block='s',
		series=4,
		mass=87.62,
		eleneg=0.95,
		eleaffin=0.05206,
		covrad=1.91,
		atmrad=2.45,
		vdwrad=0.0,
		tboil=1655.0,
		tmelt=1042.0,
		density=2.63,
		eleconfig="[Kr] 5s2",
		oxistates="2*",
		ionenergy=(
				5.6949,
				11.03,
				43.6,
				57.0,
				71.6,
				90.8,
				106.0,
				122.3,
				162.0,
				177.0,
				324.1,
				),
		isotopes={
				73: (72.96597, 0.0),
				74: (73.95631, 0.0),
				75: (74.94995, 0.0),
				76: (75.94177, 0.0),
				77: (76.937945, 0.0),
				78: (77.93218, 0.0),
				79: (78.929708, 0.0),
				80: (79.924521, 0.0),
				81: (80.923212, 0.0),
				82: (81.918402, 0.0),
				83: (82.917557, 0.0),
				84: (83.913425, 0.0056),
				85: (84.912933, 0.0),
				86: (85.9092602, 0.0986),
				87: (86.9088771, 0.07),
				88: (87.9056121, 0.8258),
				89: (88.9074507, 0.0),
				90: (89.907738, 0.0),
				91: (90.910203, 0.0),
				92: (91.911038, 0.0),
				93: (92.914026, 0.0),
				94: (93.915361, 0.0),
				95: (94.919359, 0.0),
				96: (95.921697, 0.0),
				97: (96.926153, 0.0),
				98: (97.928453, 0.0),
				99: (98.93324, 0.0),
				100: (99.93535, 0.0),
				101: (100.94052, 0.0),
				102: (101.94302, 0.0),
				103: (102.94895, 0.0),
				104: (103.95233, 0.0),
				105: (104.95858, 0.0),
				},
		description=(
				"Soft yellowish metallic element, belongs to group 2 of the "
				"periodic table. Highly reactive chemically. Sr-90 is present in "
				"radioactive fallout and has a half-life of 28 years. Discovered in "
				"1798 by Klaproth and Hope, isolated in 1808 by Humphry Davy."
				)
		)

Ba = Element(
		56,
		"Ba",
		"Barium",
		group=2,
		period=6,
		block='s',
		series=4,
		mass=137.327,
		eleneg=0.89,
		eleaffin=0.14462,
		covrad=1.98,
		atmrad=2.78,
		vdwrad=0.0,
		tboil=2078.0,
		tmelt=1002.0,
		density=3.65,
		eleconfig="[Xe] 6s2",
		oxistates="2*",
		ionenergy=(5.2117, 100.004),
		isotopes={
				114: (113.95068, 0.0),
				115: (114.94737, 0.0),
				116: (115.94138, 0.0),
				117: (116.9385, 0.0),
				118: (117.93304, 0.0),
				119: (118.93066, 0.0),
				120: (119.92604, 0.0),
				121: (120.92405, 0.0),
				122: (121.9199, 0.0),
				123: (122.918781, 0.0),
				124: (123.915094, 0.0),
				125: (124.914473, 0.0),
				126: (125.91125, 0.0),
				127: (126.911094, 0.0),
				128: (127.908318, 0.0),
				129: (128.908679, 0.0),
				130: (129.9063208, 0.00106),
				131: (130.906941, 0.0),
				132: (131.9050613, 0.00101),
				133: (132.9060075, 0.0),
				134: (133.9045084, 0.02417),
				135: (134.9056886, 0.06592),
				136: (135.9045759, 0.07854),
				137: (136.9058274, 0.11232),
				138: (137.9052472, 0.71698),
				139: (138.9088413, 0.0),
				140: (139.910605, 0.0),
				141: (140.914411, 0.0),
				142: (141.916453, 0.0),
				143: (142.920627, 0.0),
				144: (143.922953, 0.0),
				145: (144.92763, 0.0),
				146: (145.93022, 0.0),
				147: (146.93495, 0.0),
				148: (147.93772, 0.0),
				149: (148.94258, 0.0),
				150: (149.94568, 0.0),
				151: (150.95081, 0.0),
				152: (151.95427, 0.0),
				153: (152.95961, 0.0),
				},
		description=(
				"Silvery-white reactive element, belonging to group 2 of the "
				"periodic table. Soluble barium compounds are extremely poisonous. "
				"Identified in 1774 by Karl Scheele and extracted in 1808 by Humphry "
				"Davy."
				),
		)

Ra = Element(
		88,
		"Ra",
		"Radium",
		group=2,
		period=7,
		block='s',
		series=4,
		mass=226.0254,
		eleneg=0.9,
		eleaffin=0.0,
		covrad=0.0,
		atmrad=0.0,
		vdwrad=0.0,
		tboil=1413.0,
		tmelt=973.0,
		density=5.5,
		eleconfig="[Rn] 7s2",
		oxistates="2*",
		ionenergy=(5.2784, 10.147),
		isotopes={
				202: (202.00989, 0.0),
				203: (203.00927, 0.0),
				204: (204.0065, 0.0),
				205: (205.00627, 0.0),
				206: (206.003827, 0.0),
				207: (207.0038, 0.0),
				208: (208.00184, 0.0),
				209: (209.00199, 0.0),
				210: (210.000495, 0.0),
				211: (211.000898, 0.0),
				212: (211.999794, 0.0),
				213: (213.000384, 0.0),
				214: (214.000108, 0.0),
				215: (215.00272, 0.0),
				216: (216.003533, 0.0),
				217: (217.00632, 0.0),
				218: (218.00714, 0.0),
				219: (219.010085, 0.0),
				220: (220.011028, 0.0),
				221: (221.013917, 0.0),
				222: (222.015375, 0.0),
				223: (223.0185022, 0.0),
				224: (224.0202118, 0.0),
				225: (225.023612, 0.0),
				226: (226.0254098, 0.0),
				227: (227.0291778, 0.0),
				228: (228.0310703, 0.0),
				229: (229.034958, 0.0),
				230: (230.037056, 0.0),
				231: (231.04122, 0.0),
				232: (232.04364, 0.0),
				233: (233.04806, 0.0),
				234: (234.0507, 0.0),
				},
		description=(
				"Radioactive metallic transuranic element, belongs to group 2 of "
				"the periodic table. Most stable isotope, Ra-226 has a half-life of "
				"1602 years, which decays into radon. Isolated from pitchblende in "
				"1898 Marie and Pierre Curie."
				)
		)
