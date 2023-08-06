#!/usr/bin/env python3
#
#  chalcogens.py
r"""
Group 16: Chalcogens in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: O

	:class:`~chemistry_tools.elements.classes.Element` representing Oxygen

.. data:: S

	:class:`~chemistry_tools.elements.classes.Element` representing Sulfur

.. data:: Se

	:class:`~chemistry_tools.elements.classes.Element` representing Selenium

.. data:: Te

	:class:`~chemistry_tools.elements.classes.Element` representing Tellurium

.. data:: Po

	:class:`~chemistry_tools.elements.classes.Element` representing Polonium

.. data:: Lv

	:class:`~chemistry_tools.elements.classes.Element` representing Livermorium

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

__all__ = ('O', 'S', "Se", "Te", "Po", "Lv")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

O = Element(
		8,
		'O',
		"Oxygen",
		group=16,
		period=2,
		block='p',
		series=1,
		mass=15.999405,
		eleneg=3.44,
		eleaffin=1.461112,
		covrad=0.73,
		atmrad=0.65,
		vdwrad=1.52,
		tboil=90.188,
		tmelt=54.8,
		density=1.33,
		eleconfig="[He] 2s2 2p4",
		oxistates="-2*, -1",
		ionenergy=(
				13.6181,
				35.116,
				54.934,
				77.412,
				113.896,
				138.116,
				739.315,
				871.387,
				),
		isotopes={
				12: (12.034405, 0.0),
				13: (13.024812, 0.0),
				14: (14.00859625, 0.0),
				15: (15.0030656, 0.0),
				16: (15.99491461956, 0.99757),
				17: (16.9991317, 0.00038),
				18: (17.999161, 0.00205),
				19: (19.00358, 0.0),
				20: (20.0040767, 0.0),
				21: (21.008656, 0.0),
				22: (22.00997, 0.0),
				23: (23.01569, 0.0),
				24: (24.02047, 0.0),
				25: (25.02946, 0.0),
				26: (26.03834, 0.0),
				27: (27.04826, 0.0),
				28: (28.05781, 0.0),
				},
		description=(
				"A colourless, odourless gaseous element belonging to group 16 of "
				"the periodic table. It is the most abundant element present in the "
				"Earth's crust. It also makes up 20.8% of the Earth's atmosphere. "
				"For industrial purposes, it is separated from liquid air by "
				"fractional distillation. It is used in high temperature welding, "
				"and in breathing. It commonly comes in the form of Oxygen, but is "
				"found as Ozone in the upper atmosphere. It was discovered by "
				"Priestley in 1774."
				)
		)

S = Element(
		16,
		'S',
		"Sulfur",
		group=16,
		period=3,
		block='p',
		series=1,
		mass=32.0648,
		eleneg=2.58,
		eleaffin=2.0771029,
		covrad=1.02,
		atmrad=1.09,
		vdwrad=1.8,
		tboil=717.82,
		tmelt=392.2,
		density=2.06,
		eleconfig="[Ne] 3s2 3p4",
		oxistates="6*, 4, 2, -2",
		ionenergy=(
				10.36,
				23.33,
				34.83,
				47.3,
				72.68,
				88.049,
				280.93,
				328.23,
				379.1,
				447.09,
				504.78,
				564.65,
				651.63,
				707.14,
				3223.836,
				3494.099,
				),
		isotopes={
				26: (26.02788, 0.0),
				27: (27.01883, 0.0),
				28: (28.00437, 0.0),
				29: (28.99661, 0.0),
				30: (29.984903, 0.0),
				31: (30.9795547, 0.0),
				32: (31.972071, 0.9499),
				33: (32.97145876, 0.0075),
				34: (33.9678669, 0.0425),
				35: (34.96903216, 0.0),
				36: (35.96708076, 0.0001),
				37: (36.97112557, 0.0),
				38: (37.971163, 0.0),
				39: (38.97513, 0.0),
				40: (39.97545, 0.0),
				41: (40.97958, 0.0),
				42: (41.98102, 0.0),
				43: (42.98715, 0.0),
				44: (43.99021, 0.0),
				45: (44.99651, 0.0),
				46: (46.00075, 0.0),
				47: (47.00859, 0.0),
				48: (48.01417, 0.0),
				49: (49.02362, 0.0),
				},
		description=(
				"Yellow, nonmetallic element belonging to group 16 of the periodic "
				"table. It is an essential element in living organisms, needed in "
				"the amino acids cysteine and methionine, and hence in many "
				"proteins. Absorbed by plants from the soil as sulphate ion."
				)
		)

Se = Element(
		34,
		"Se",
		"Selenium",
		group=16,
		period=4,
		block='p',
		series=1,
		mass=78.971,
		eleneg=2.55,
		eleaffin=2.02067,
		covrad=1.16,
		atmrad=1.22,
		vdwrad=1.9,
		tboil=958.0,
		tmelt=494.0,
		density=4.82,
		eleconfig="[Ar] 3d10 4s2 4p4",
		oxistates="6, 4*, -2",
		ionenergy=(
				9.7524,
				21.9,
				30.82,
				42.944,
				68.3,
				81.7,
				155.4,
				),
		isotopes={
				65: (64.96466, 0.0),
				66: (65.95521, 0.0),
				67: (66.95009, 0.0),
				68: (67.9418, 0.0),
				69: (68.93956, 0.0),
				70: (69.93339, 0.0),
				71: (70.93224, 0.0),
				72: (71.927112, 0.0),
				73: (72.926765, 0.0),
				74: (73.9224764, 0.0089),
				75: (74.9225234, 0.0),
				76: (75.9192136, 0.0937),
				77: (76.919914, 0.0763),
				78: (77.9173091, 0.2377),
				79: (78.9184991, 0.0),
				80: (79.9165213, 0.4961),
				81: (80.9179925, 0.0),
				82: (81.9166994, 0.0873),
				83: (82.919118, 0.0),
				84: (83.918462, 0.0),
				85: (84.92225, 0.0),
				86: (85.924272, 0.0),
				87: (86.92852, 0.0),
				88: (87.93142, 0.0),
				89: (88.93645, 0.0),
				90: (89.93996, 0.0),
				91: (90.94596, 0.0),
				92: (91.94992, 0.0),
				93: (92.95629, 0.0),
				94: (93.96049, 0.0),
				},
		description=(
				"Metalloid element, belongs to group 16 of the periodic table. "
				"Multiple allotropic forms exist. Chemically resembles sulphur. "
				"Discovered in 1817 by Jons J. Berzelius."
				)
		)

Te = Element(
		52,
		"Te",
		"Tellurium",
		group=16,
		period=5,
		block='p',
		series=5,
		mass=127.6,
		eleneg=2.1,
		eleaffin=1.970875,
		covrad=1.36,
		atmrad=1.42,
		vdwrad=2.06,
		tboil=1261.0,
		tmelt=722.72,
		density=6.25,
		eleconfig="[Kr] 4d10 5s2 5p4",
		oxistates="6, 4*, -2",
		ionenergy=(
				9.0096,
				18.6,
				27.96,
				37.41,
				58.75,
				70.7,
				137.0,
				),
		isotopes={
				105: (104.94364, 0.0),
				106: (105.9375, 0.0),
				107: (106.93501, 0.0),
				108: (107.92944, 0.0),
				109: (108.92742, 0.0),
				110: (109.92241, 0.0),
				111: (110.92111, 0.0),
				112: (111.91701, 0.0),
				113: (112.91589, 0.0),
				114: (113.91209, 0.0),
				115: (114.9119, 0.0),
				116: (115.90846, 0.0),
				117: (116.908645, 0.0),
				118: (117.905828, 0.0),
				119: (118.906404, 0.0),
				120: (119.90402, 0.0009),
				121: (120.904936, 0.0),
				122: (121.9030439, 0.0255),
				123: (122.90427, 0.0089),
				124: (123.9028179, 0.0474),
				125: (124.9044307, 0.0707),
				126: (125.9033117, 0.1884),
				127: (126.9052263, 0.0),
				128: (127.9044631, 0.3174),
				129: (128.9065982, 0.0),
				130: (129.9062244, 0.3408),
				131: (130.9085239, 0.0),
				132: (131.908553, 0.0),
				133: (132.910955, 0.0),
				134: (133.911369, 0.0),
				135: (134.91645, 0.0),
				136: (135.9201, 0.0),
				137: (136.92532, 0.0),
				138: (137.92922, 0.0),
				139: (138.93473, 0.0),
				140: (139.93885, 0.0),
				141: (140.94465, 0.0),
				142: (141.94908, 0.0),
				},
		description=(
				"Silvery metalloid element of group 16. Eight natural isotopes, "
				"nine radioactive isotopes. Used in semiconductors and to a degree "
				"in some steels. Chemistry is similar to Sulphur. Discovered in 1782 "
				"by Franz Miller."
				)
		)

Po = Element(
		84,
		"Po",
		"Polonium",
		group=16,
		period=6,
		block='p',
		series=5,
		mass=208.9824,
		eleneg=2.0,
		eleaffin=1.9,
		covrad=1.46,
		atmrad=1.53,
		vdwrad=0.0,
		tboil=0.0,
		tmelt=527.0,
		density=9.2,
		eleconfig="[Xe] 4f14 5d10 6s2 6p4",
		oxistates="6, 4*, 2",
		ionenergy=(8.414, ),
		isotopes={
				188: (187.999422, 0.0),
				189: (188.998481, 0.0),
				190: (189.995101, 0.0),
				191: (190.994574, 0.0),
				192: (191.991335, 0.0),
				193: (192.99103, 0.0),
				194: (193.988186, 0.0),
				195: (194.98811, 0.0),
				196: (195.985535, 0.0),
				197: (196.98566, 0.0),
				198: (197.983389, 0.0),
				199: (198.983666, 0.0),
				200: (199.981799, 0.0),
				201: (200.98226, 0.0),
				202: (201.980758, 0.0),
				203: (202.98142, 0.0),
				204: (203.980318, 0.0),
				205: (204.981203, 0.0),
				206: (205.980481, 0.0),
				207: (206.981593, 0.0),
				208: (207.9812457, 0.0),
				209: (208.9824304, 0.0),
				210: (209.9828737, 0.0),
				211: (210.9866532, 0.0),
				212: (211.988868, 0.0),
				213: (212.992857, 0.0),
				214: (213.9952014, 0.0),
				215: (214.99942, 0.0),
				216: (216.001915, 0.0),
				217: (217.006335, 0.0),
				218: (218.008973, 0.0),
				219: (219.01374, 0.0),
				220: (220.0166, 0.0),
				},
		description=(
				"Rare radioactive metallic element, belongs to group 16 of the "
				"periodic table. Over 30 known isotopes exist, the most of all "
				"elements. Po-209 has a half-life of 103 years. Possible uses in "
				"heating spacecraft. Discovered by Marie Curie in 1898 in a sample "
				"of pitchblende."
				)
		)

Lv = Element(
		116,
		"Lv",
		"Livermorium",
		group=16,
		period=7,
		block='p',
		series=8,
		isotopes={
				289: (289.19886, 0.0),
				290: (290.19859, 0.0),
				291: (291.20001, 0.0),
				292: (292.19979, 0.0),
				}
		)
