#!/usr/bin/env python3
#
#  tetrels.py
r"""
Group 14: Tetrels, carbon group, crystallogens or adamantogens in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: C

	:class:`~chemistry_tools.elements.classes.Element` representing Carbon

.. data:: Si

	:class:`~chemistry_tools.elements.classes.Element` representing Silicon

.. data:: Ge

	:class:`~chemistry_tools.elements.classes.Element` representing Germanium

.. data:: Sn

	:class:`~chemistry_tools.elements.classes.Element` representing Tin

.. data:: Pb

	:class:`~chemistry_tools.elements.classes.Element` representing Lead

.. data:: Fl

	:class:`~chemistry_tools.elements.classes.Element` representing Flerovium

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

__all__ = ('C', "Si", "Ge", "Sn", "Pb", "Fl")

# this package
from .classes import Element

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

C = Element(
		6,
		'C',
		"Carbon",
		group=14,
		period=2,
		block='p',
		series=1,
		mass=12.01074,
		eleneg=2.55,
		eleaffin=1.262118,
		covrad=0.77,
		atmrad=0.91,
		vdwrad=1.7,
		tboil=5100.0,
		tmelt=3825.0,
		density=3.51,
		eleconfig="[He] 2s2 2p2",
		oxistates="4*, 2, -4*",
		ionenergy=(
				11.2603,
				24.383,
				47.877,
				64.492,
				392.077,
				489.981,
				),
		isotopes={
				8: (8.037675, 0.0),
				9: (9.0310367, 0.0),
				10: (10.0168532, 0.0),
				11: (11.0114336, 0.0),
				12: (12.0, 0.9893),
				13: (13.0033548378, 0.0107),
				14: (14.003241989, 0.0),
				15: (15.0105993, 0.0),
				16: (16.014701, 0.0),
				17: (17.022586, 0.0),
				18: (18.02676, 0.0),
				19: (19.03481, 0.0),
				20: (20.04032, 0.0),
				21: (21.04934, 0.0),
				22: (22.0572, 0.0),
				},
		description=(
				"Carbon is a member of group 14 of the periodic table. It has three "
				"allotropic forms of it, diamonds, graphite and fullerite. Carbon-14 "
				"is commonly used in radioactive dating. Carbon occurs in all "
				"organic life and is the basis of organic chemistry. Carbon has the "
				"interesting chemical property of being able to bond with itself, "
				"and a wide variety of other elements."
				)
		)

Si = Element(
		14,
		"Si",
		"Silicon",
		group=14,
		period=3,
		block='p',
		series=5,
		mass=28.0855,
		eleneg=1.9,
		eleaffin=1.389521,
		covrad=1.11,
		atmrad=1.46,
		vdwrad=2.1,
		tboil=2630.0,
		tmelt=1683.0,
		density=2.33,
		eleconfig="[Ne] 3s2 3p2",
		oxistates="4*, -4",
		ionenergy=(
				8.1517,
				16.345,
				33.492,
				45.141,
				166.77,
				205.05,
				246.52,
				303.17,
				351.1,
				401.43,
				476.06,
				523.5,
				2437.676,
				2673.108,
				),
		isotopes={
				22: (22.03453, 0.0),
				23: (23.02552, 0.0),
				24: (24.011546, 0.0),
				25: (25.004106, 0.0),
				26: (25.99233, 0.0),
				27: (26.98670491, 0.0),
				28: (27.9769265325, 0.92223),
				29: (28.9764947, 0.04685),
				30: (29.97377017, 0.03092),
				31: (30.97536323, 0.0),
				32: (31.97414808, 0.0),
				33: (32.978, 0.0),
				34: (33.978576, 0.0),
				35: (34.98458, 0.0),
				36: (35.9866, 0.0),
				37: (36.99294, 0.0),
				38: (37.99563, 0.0),
				39: (39.00207, 0.0),
				40: (40.00587, 0.0),
				41: (41.01456, 0.0),
				42: (42.01979, 0.0),
				43: (43.02866, 0.0),
				44: (44.03526, 0.0),
				},
		description=(
				"Metalloid element belonging to group 14 of the periodic table. It "
				"is the second most abundant element in the Earth's crust, making up "
				"25.7% of it by weight. Chemically less reactive than carbon. First "
				"identified by Lavoisier in 1787 and first isolated in 1823 by "
				"Berzelius."
				)
		)

Ge = Element(
		32,
		"Ge",
		"Germanium",
		group=14,
		period=4,
		block='p',
		series=5,
		mass=72.63,
		eleneg=2.01,
		eleaffin=1.232712,
		covrad=1.22,
		atmrad=1.52,
		vdwrad=0.0,
		tboil=3107.0,
		tmelt=1211.5,
		density=5.32,
		eleconfig="[Ar] 3d10 4s2 4p2",
		oxistates="4*",
		ionenergy=(7.8994, 15.934, 34.22, 45.71, 93.5),
		isotopes={
				58: (57.99101, 0.0),
				59: (58.98175, 0.0),
				60: (59.97019, 0.0),
				61: (60.96379, 0.0),
				62: (61.95465, 0.0),
				63: (62.94964, 0.0),
				64: (63.94165, 0.0),
				65: (64.93944, 0.0),
				66: (65.93384, 0.0),
				67: (66.932734, 0.0),
				68: (67.928094, 0.0),
				69: (68.9279645, 0.0),
				70: (69.9242474, 0.2038),
				71: (70.924951, 0.0),
				72: (71.9220758, 0.2731),
				73: (72.9234589, 0.0776),
				74: (73.9211778, 0.3672),
				75: (74.9228589, 0.0),
				76: (75.9214026, 0.0783),
				77: (76.9235486, 0.0),
				78: (77.922853, 0.0),
				79: (78.9254, 0.0),
				80: (79.92537, 0.0),
				81: (80.92882, 0.0),
				82: (81.92955, 0.0),
				83: (82.93462, 0.0),
				84: (83.93747, 0.0),
				85: (84.94303, 0.0),
				86: (85.94649, 0.0),
				87: (86.95251, 0.0),
				88: (87.95691, 0.0),
				89: (88.96383, 0.0),
				},
		description=(
				"Lustrous hard metalloid element, belongs to group 14 of the "
				"periodic table. Forms a large number of organometallic compounds. "
				"Predicted by Mendeleev in 1871, it was actually found in 1886 by "
				"Winkler."
				)
		)

Sn = Element(
		50,
		"Sn",
		"Tin",
		group=14,
		period=5,
		block='p',
		series=7,
		mass=118.71,
		eleneg=1.96,
		eleaffin=1.112066,
		covrad=1.41,
		atmrad=1.72,
		vdwrad=2.17,
		tboil=2876.0,
		tmelt=505.12,
		density=7.29,
		eleconfig="[Kr] 4d10 5s2 5p2",
		oxistates="4*, 2*",
		ionenergy=(7.3439, 14.632, 30.502, 40.734, 72.28),
		isotopes={
				99: (98.94933, 0.0),
				100: (99.93904, 0.0),
				101: (100.93606, 0.0),
				102: (101.9303, 0.0),
				103: (102.9281, 0.0),
				104: (103.92314, 0.0),
				105: (104.92135, 0.0),
				106: (105.91688, 0.0),
				107: (106.91564, 0.0),
				108: (107.911925, 0.0),
				109: (108.911283, 0.0),
				110: (109.907843, 0.0),
				111: (110.907734, 0.0),
				112: (111.904818, 0.0097),
				113: (112.905171, 0.0),
				114: (113.902779, 0.0066),
				115: (114.903342, 0.0034),
				116: (115.901741, 0.1454),
				117: (116.902952, 0.0768),
				118: (117.901603, 0.2422),
				119: (118.903308, 0.0859),
				120: (119.9021947, 0.3258),
				121: (120.9042355, 0.0),
				122: (121.903439, 0.0463),
				123: (122.9057208, 0.0),
				124: (123.9052739, 0.0579),
				125: (124.9077841, 0.0),
				126: (125.907653, 0.0),
				127: (126.91036, 0.0),
				128: (127.910537, 0.0),
				129: (128.91348, 0.0),
				130: (129.913967, 0.0),
				131: (130.917, 0.0),
				132: (131.917816, 0.0),
				133: (132.92383, 0.0),
				134: (133.92829, 0.0),
				135: (134.93473, 0.0),
				136: (135.93934, 0.0),
				137: (136.94599, 0.0),
				},
		description=(
				"Silvery malleable metallic element belonging to group 14 of the "
				"periodic table. Twenty-six isotopes are known, five of which are "
				"radioactive. Chemically reactive. Combines directly with chlorine "
				"and oxygen and displaces hydrogen from dilute acids."
				)
		)

Pb = Element(
		82,
		"Pb",
		"Lead",
		group=14,
		period=6,
		block='p',
		series=7,
		mass=207.2,
		eleneg=2.33,
		eleaffin=0.364,
		covrad=1.47,
		atmrad=1.81,
		vdwrad=2.02,
		tboil=2023.0,
		tmelt=600.65,
		density=11.34,
		eleconfig="[Xe] 4f14 5d10 6s2 6p2",
		oxistates="4, 2*",
		ionenergy=(7.4167, 15.032, 31.937, 42.32, 68.8),
		isotopes={
				178: (178.00383, 0.0),
				179: (179.00215, 0.0),
				180: (179.997918, 0.0),
				181: (180.99662, 0.0),
				182: (181.992672, 0.0),
				183: (182.99187, 0.0),
				184: (183.988142, 0.0),
				185: (184.98761, 0.0),
				186: (185.984239, 0.0),
				187: (186.983918, 0.0),
				188: (187.980874, 0.0),
				189: (188.98081, 0.0),
				190: (189.978082, 0.0),
				191: (190.97827, 0.0),
				192: (191.975785, 0.0),
				193: (192.97617, 0.0),
				194: (193.974012, 0.0),
				195: (194.974542, 0.0),
				196: (195.972774, 0.0),
				197: (196.973431, 0.0),
				198: (197.972034, 0.0),
				199: (198.972917, 0.0),
				200: (199.971827, 0.0),
				201: (200.972885, 0.0),
				202: (201.972159, 0.0),
				203: (202.973391, 0.0),
				204: (203.9730436, 0.014),
				205: (204.9744818, 0.0),
				206: (205.9744653, 0.241),
				207: (206.9758969, 0.221),
				208: (207.9766521, 0.524),
				209: (208.9810901, 0.0),
				210: (209.9841885, 0.0),
				211: (210.988737, 0.0),
				212: (211.9918975, 0.0),
				213: (212.996581, 0.0),
				214: (213.9998054, 0.0),
				215: (215.00481, 0.0),
				},
		description=(
				"Heavy dull grey ductile metallic element, belongs to group 14. "
				"Used in building construction, lead-place accumulators, bullets and "
				"shot, and is part of solder, pewter, bearing metals, type metals "
				"and fusible alloys."
				)
		)

Fl = Element(
		114,
		"Fl",
		"Flerovium",
		group=14,
		period=7,
		block='p',
		series=8,
		isotopes={
				285: (285.1837, 0.0),
				286: (286.18386, 0.0),
				287: (287.1856, 0.0),
				288: (288.18569, 0.0),
				289: (289.18728, 0.0),
				}
		)
