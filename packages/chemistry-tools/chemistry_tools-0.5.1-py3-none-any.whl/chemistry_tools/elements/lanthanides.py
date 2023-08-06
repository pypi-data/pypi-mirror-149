#!/usr/bin/env python3
#
#  lanthanides.py
r"""
Lanthanides (or lanthanoids) in the Periodic Table.

.. raw:: latex

	\begin{multicols}{2}

.. data:: La

	:class:`~chemistry_tools.elements.classes.Element` representing Lanthanum

.. data:: Ce

	:class:`~chemistry_tools.elements.classes.Element` representing Cerium

.. data:: Pr

	:class:`~chemistry_tools.elements.classes.Element` representing Praseodymium

.. data:: Nd

	:class:`~chemistry_tools.elements.classes.Element` representing Neodymium

.. data:: Pm

	:class:`~chemistry_tools.elements.classes.Element` representing Promethium

.. data:: Sm

	:class:`~chemistry_tools.elements.classes.Element` representing Samarium

.. data:: Eu

	:class:`~chemistry_tools.elements.classes.Element` representing Europium

.. data:: Gd

	:class:`~chemistry_tools.elements.classes.Element` representing Gadolinium

.. data:: Tb

	:class:`~chemistry_tools.elements.classes.Element` representing Terbium

.. data:: Dy

	:class:`~chemistry_tools.elements.classes.Element` representing Dysprosium

.. data:: Ho

	:class:`~chemistry_tools.elements.classes.Element` representing Holmium

.. data:: Er

	:class:`~chemistry_tools.elements.classes.Element` representing Erbium

.. data:: Tm

	:class:`~chemistry_tools.elements.classes.Element` representing Thulium

.. data:: Yb

	:class:`~chemistry_tools.elements.classes.Element` representing Ytterbium

.. data:: Lu

	:class:`~chemistry_tools.elements.classes.Element` representing Lutetium

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

__all__ = ("La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu")

# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.

La = Element(
		57,
		"La",
		"Lanthanum",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=138.90547,
		eleneg=1.1,
		eleaffin=0.47,
		covrad=1.69,
		atmrad=2.74,
		vdwrad=0.0,
		tboil=3737.0,
		tmelt=1191.0,
		density=6.16,
		eleconfig="[Xe] 5d 6s2",
		oxistates="3*",
		ionenergy=(5.5769, 11.06, 19.175),
		isotopes={
				117: (116.95007, 0.0),
				118: (117.94673, 0.0),
				119: (118.94099, 0.0),
				120: (119.93807, 0.0),
				121: (120.93301, 0.0),
				122: (121.93071, 0.0),
				123: (122.92624, 0.0),
				124: (123.92457, 0.0),
				125: (124.920816, 0.0),
				126: (125.91951, 0.0),
				127: (126.916375, 0.0),
				128: (127.91559, 0.0),
				129: (128.912693, 0.0),
				130: (129.912369, 0.0),
				131: (130.91007, 0.0),
				132: (131.9101, 0.0),
				133: (132.90822, 0.0),
				134: (133.908514, 0.0),
				135: (134.906977, 0.0),
				136: (135.90764, 0.0),
				137: (136.906494, 0.0),
				138: (137.907112, 0.0009),
				139: (138.9063533, 0.9991),
				140: (139.9094776, 0.0),
				141: (140.910962, 0.0),
				142: (141.914079, 0.0),
				143: (142.916063, 0.0),
				144: (143.9196, 0.0),
				145: (144.92165, 0.0),
				146: (145.92579, 0.0),
				147: (146.92824, 0.0),
				148: (147.93223, 0.0),
				149: (148.93473, 0.0),
				150: (149.93877, 0.0),
				151: (150.94172, 0.0),
				152: (151.94625, 0.0),
				153: (152.94962, 0.0),
				154: (153.9545, 0.0),
				155: (154.95835, 0.0),
				},
		description=(
				"(From the Greek word lanthanein, to line hidden) Silvery metallic "
				"element belonging to group 3 of the periodic table and oft "
				"considered to be one of the lanthanoids. Found in some rare-earth "
				"minerals. Twenty-five natural isotopes exist. La-139 which is "
				"stable, and La-138 which has a half-life of 10^10 to 10^15 years. "
				"The other twenty-three isotopes are radioactive. It resembles the "
				"lanthanoids chemically. Lanthanum has a low to moderate level of "
				"toxicity, and should be handled with care. Discovered in 1839 by "
				"C.G. Mosander."
				)
		)

Ce = Element(
		58,
		"Ce",
		"Cerium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=140.116,
		eleneg=1.12,
		eleaffin=0.5,
		covrad=1.65,
		atmrad=2.7,
		vdwrad=0.0,
		tboil=3715.0,
		tmelt=1071.0,
		density=6.77,
		eleconfig="[Xe] 4f 5d 6s2",
		oxistates="4, 3*",
		ionenergy=(5.5387, 10.85, 20.2, 36.72),
		isotopes={
				119: (118.95276, 0.0),
				120: (119.94664, 0.0),
				121: (120.94342, 0.0),
				122: (121.93791, 0.0),
				123: (122.9354, 0.0),
				124: (123.93041, 0.0),
				125: (124.92844, 0.0),
				126: (125.92397, 0.0),
				127: (126.92273, 0.0),
				128: (127.91891, 0.0),
				129: (128.9181, 0.0),
				130: (129.91474, 0.0),
				131: (130.91442, 0.0),
				132: (131.91146, 0.0),
				133: (132.911515, 0.0),
				134: (133.908925, 0.0),
				135: (134.909151, 0.0),
				136: (135.907172, 0.00185),
				137: (136.907806, 0.0),
				138: (137.905991, 0.00251),
				139: (138.906653, 0.0),
				140: (139.9054387, 0.8845),
				141: (140.9082763, 0.0),
				142: (141.909244, 0.11114),
				143: (142.912386, 0.0),
				144: (143.913647, 0.0),
				145: (144.91723, 0.0),
				146: (145.91876, 0.0),
				147: (146.92267, 0.0),
				148: (147.92443, 0.0),
				149: (148.9284, 0.0),
				150: (149.93041, 0.0),
				151: (150.93398, 0.0),
				152: (151.93654, 0.0),
				153: (152.94058, 0.0),
				154: (153.94342, 0.0),
				155: (154.94804, 0.0),
				156: (155.95126, 0.0),
				157: (156.95634, 0.0),
				},
		description=(
				"Silvery metallic element, belongs to the lanthanoids. Four natural "
				"isotopes exist, and fifteen radioactive isotopes have been "
				"identified. Used in some rare-earth alloys. The oxidized form is "
				"used in the glass industry. Discovered by Martin .H. Klaproth in "
				"1803."
				)
		)

Pr = Element(
		59,
		"Pr",
		"Praseodymium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=140.90766,
		eleneg=1.13,
		eleaffin=0.5,
		covrad=1.65,
		atmrad=2.67,
		vdwrad=0.0,
		tboil=3785.0,
		tmelt=1204.0,
		density=6.48,
		eleconfig="[Xe] 4f3 6s2",
		oxistates="4, 3*",
		ionenergy=(5.473, 10.55, 21.62, 38.95, 57.45),
		isotopes={
				121: (120.95536, 0.0),
				122: (121.95181, 0.0),
				123: (122.94596, 0.0),
				124: (123.94296, 0.0),
				125: (124.93783, 0.0),
				126: (125.93531, 0.0),
				127: (126.93083, 0.0),
				128: (127.92879, 0.0),
				129: (128.9251, 0.0),
				130: (129.92359, 0.0),
				131: (130.92026, 0.0),
				132: (131.91926, 0.0),
				133: (132.916331, 0.0),
				134: (133.91571, 0.0),
				135: (134.913112, 0.0),
				136: (135.912692, 0.0),
				137: (136.910705, 0.0),
				138: (137.910755, 0.0),
				139: (138.908938, 0.0),
				140: (139.909076, 0.0),
				141: (140.9076528, 1.0),
				142: (141.9100448, 0.0),
				143: (142.9108169, 0.0),
				144: (143.913305, 0.0),
				145: (144.914512, 0.0),
				146: (145.91764, 0.0),
				147: (146.918996, 0.0),
				148: (147.922135, 0.0),
				149: (148.92372, 0.0),
				150: (149.926673, 0.0),
				151: (150.928319, 0.0),
				152: (151.9315, 0.0),
				153: (152.93384, 0.0),
				154: (153.93752, 0.0),
				155: (154.94012, 0.0),
				156: (155.94427, 0.0),
				157: (156.94743, 0.0),
				158: (157.95198, 0.0),
				159: (158.9555, 0.0),
				},
		description=(
				"Soft silvery metallic element, belongs to the lanthanoids. Only "
				"natural isotope is Pr-141 which is not radioactive. Fourteen "
				"radioactive isotopes have been artificially produced. Used in "
				"rare-earth alloys. Discovered in 1885 by C.A. von Welsbach."
				)
		)

Nd = Element(
		60,
		"Nd",
		"Neodymium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=144.242,
		eleneg=1.14,
		eleaffin=0.5,
		covrad=1.64,
		atmrad=2.64,
		vdwrad=0.0,
		tboil=3347.0,
		tmelt=1294.0,
		density=7.0,
		eleconfig="[Xe] 4f4 6s2",
		oxistates="3*",
		ionenergy=(5.525, 10.72),
		isotopes={
				124: (123.95223, 0.0),
				125: (124.94888, 0.0),
				126: (125.94322, 0.0),
				127: (126.9405, 0.0),
				128: (127.93539, 0.0),
				129: (128.93319, 0.0),
				130: (129.92851, 0.0),
				131: (130.92725, 0.0),
				132: (131.923321, 0.0),
				133: (132.92235, 0.0),
				134: (133.91879, 0.0),
				135: (134.918181, 0.0),
				136: (135.914976, 0.0),
				137: (136.914567, 0.0),
				138: (137.91195, 0.0),
				139: (138.911978, 0.0),
				140: (139.90955, 0.0),
				141: (140.90961, 0.0),
				142: (141.9077233, 0.272),
				143: (142.9098143, 0.122),
				144: (143.9100873, 0.238),
				145: (144.9125736, 0.083),
				146: (145.9131169, 0.172),
				147: (146.9161004, 0.0),
				148: (147.916893, 0.057),
				149: (148.920149, 0.0),
				150: (149.920891, 0.056),
				151: (150.923829, 0.0),
				152: (151.924682, 0.0),
				153: (152.927698, 0.0),
				154: (153.92948, 0.0),
				155: (154.93293, 0.0),
				156: (155.93502, 0.0),
				157: (156.93903, 0.0),
				158: (157.9416, 0.0),
				159: (158.94609, 0.0),
				160: (159.94909, 0.0),
				161: (160.95388, 0.0),
				},
		description=(
				"Soft bright silvery metallic element, belongs to the lanthanoids. "
				"Seven natural isotopes, Nd-144 being the only radioactive one with "
				"a half-life of 10^10 to 10^15 years. Six artificial radioisotopes "
				"have been produced. The metal is used in glass works to color class "
				"a shade of violet-purple and make it dichroic. One of the more "
				"reactive rare-earth metals, quickly reacts with air. Used in some "
				"rare-earth alloys. Neodymium is used to color the glass used in "
				"welder's glasses. Neodymium is also used in very powerful, "
				"permanent magnets (Nd2Fe14B). Discovered by Carl F. Auer von "
				"Welsbach in Austria in 1885 by separating didymium into its "
				"elemental components Praseodymium and neodymium. The name comes "
				"from the Greek words 'neos didymos' which means 'new twin'. "
				"Neodymium should be considered highly toxic, however evidence would "
				"seem to show that it acts as little more than a skin and eye "
				"irritant. The dust however, presents a fire and explosion hazard."
				)
		)

Pm = Element(
		61,
		"Pm",
		"Promethium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=144.9128,
		eleneg=1.13,
		eleaffin=0.5,
		covrad=1.63,
		atmrad=2.62,
		vdwrad=0.0,
		tboil=3273.0,
		tmelt=1315.0,
		density=7.22,
		eleconfig="[Xe] 4f5 6s2",
		oxistates="3*",
		ionenergy=(5.582, 10.9),
		isotopes={
				126: (125.95752, 0.0),
				127: (126.95163, 0.0),
				128: (127.94842, 0.0),
				129: (128.94316, 0.0),
				130: (129.94045, 0.0),
				131: (130.93587, 0.0),
				132: (131.93375, 0.0),
				133: (132.92978, 0.0),
				134: (133.92835, 0.0),
				135: (134.92488, 0.0),
				136: (135.92357, 0.0),
				137: (136.920479, 0.0),
				138: (137.919548, 0.0),
				139: (138.916804, 0.0),
				140: (139.91604, 0.0),
				141: (140.913555, 0.0),
				142: (141.912874, 0.0),
				143: (142.910933, 0.0),
				144: (143.912591, 0.0),
				145: (144.912749, 0.0),
				146: (145.914696, 0.0),
				147: (146.9151385, 0.0),
				148: (147.917475, 0.0),
				149: (148.918334, 0.0),
				150: (149.920984, 0.0),
				151: (150.921207, 0.0),
				152: (151.923497, 0.0),
				153: (152.924117, 0.0),
				154: (153.92646, 0.0),
				155: (154.9281, 0.0),
				156: (155.93106, 0.0),
				157: (156.93304, 0.0),
				158: (157.93656, 0.0),
				159: (158.93897, 0.0),
				160: (159.94299, 0.0),
				161: (160.94586, 0.0),
				162: (161.95029, 0.0),
				163: (162.95368, 0.0),
				},
		description=(
				"Soft silvery metallic element, belongs to the lanthanoids. Pm-147, "
				"the only natural isotope, is radioactive and has a half-life of 252 "
				"years. Eighteen radioisotopes have been produced, but all have very "
				"short half-lives. Found only in nuclear decay waste. Pm-147 is of "
				"interest as a beta-decay source, however Pm-146 and Pm-148 have to "
				"be removed from it first, as they generate gamma radiation. "
				"Discovered by J.A. Marinsky, L.E. Glendenin and C.D. Coryell in "
				"1947."
				)
		)

Sm = Element(
		62,
		"Sm",
		"Samarium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=150.36,
		eleneg=1.17,
		eleaffin=0.5,
		covrad=1.62,
		atmrad=2.59,
		vdwrad=0.0,
		tboil=2067.0,
		tmelt=1347.0,
		density=7.54,
		eleconfig="[Xe] 4f6 6s2",
		oxistates="3*, 2",
		ionenergy=(5.6437, 11.07),
		isotopes={
				128: (127.95808, 0.0),
				129: (128.95464, 0.0),
				130: (129.94892, 0.0),
				131: (130.94611, 0.0),
				132: (131.94069, 0.0),
				133: (132.93867, 0.0),
				134: (133.93397, 0.0),
				135: (134.93252, 0.0),
				136: (135.928276, 0.0),
				137: (136.92697, 0.0),
				138: (137.923244, 0.0),
				139: (138.922297, 0.0),
				140: (139.918995, 0.0),
				141: (140.918476, 0.0),
				142: (141.915198, 0.0),
				143: (142.914628, 0.0),
				144: (143.911999, 0.0307),
				145: (144.91341, 0.0),
				146: (145.913041, 0.0),
				147: (146.9148979, 0.1499),
				148: (147.9148227, 0.1124),
				149: (148.9171847, 0.1382),
				150: (149.9172755, 0.0738),
				151: (150.9199324, 0.0),
				152: (151.9197324, 0.2675),
				153: (152.9220974, 0.0),
				154: (153.9222093, 0.2275),
				155: (154.9246402, 0.0),
				156: (155.925528, 0.0),
				157: (156.92836, 0.0),
				158: (157.92999, 0.0),
				159: (158.93321, 0.0),
				160: (159.93514, 0.0),
				161: (160.93883, 0.0),
				162: (161.94122, 0.0),
				163: (162.94536, 0.0),
				164: (163.94828, 0.0),
				165: (164.95298, 0.0),
				},
		description=(
				"Soft silvery metallic element, belongs to the lanthanoids. Seven "
				"natural isotopes, Sm-147 is the only radioisotope, and has a "
				"half-life of 2.5*10^11 years. Used for making special alloys needed "
				"in the production of nuclear reactors. Also used as a neutron "
				"absorber. Small quantities of samarium oxide is used in special "
				"optical glasses. The largest use of the element is its "
				"ferromagnetic alloy which produces permanent magnets that are five "
				"times stronger than magnets produced by any other material. "
				"Discovered by Francois Lecoq de Boisbaudran in 1879."
				)
		)

Eu = Element(
		63,
		"Eu",
		"Europium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=151.964,
		eleneg=1.2,
		eleaffin=0.5,
		covrad=1.85,
		atmrad=2.56,
		vdwrad=0.0,
		tboil=1800.0,
		tmelt=1095.0,
		density=5.25,
		eleconfig="[Xe] 4f7 6s2",
		oxistates="3*, 2",
		ionenergy=(5.6704, 11.25),
		isotopes={
				130: (129.96357, 0.0),
				131: (130.95775, 0.0),
				132: (131.95437, 0.0),
				133: (132.94924, 0.0),
				134: (133.94651, 0.0),
				135: (134.94182, 0.0),
				136: (135.9396, 0.0),
				137: (136.93557, 0.0),
				138: (137.93371, 0.0),
				139: (138.929792, 0.0),
				140: (139.92809, 0.0),
				141: (140.924931, 0.0),
				142: (141.92343, 0.0),
				143: (142.920298, 0.0),
				144: (143.918817, 0.0),
				145: (144.916265, 0.0),
				146: (145.917206, 0.0),
				147: (146.916746, 0.0),
				148: (147.918086, 0.0),
				149: (148.917931, 0.0),
				150: (149.919702, 0.0),
				151: (150.9198502, 0.4781),
				152: (151.9217445, 0.0),
				153: (152.9212303, 0.5219),
				154: (153.9229792, 0.0),
				155: (154.9228933, 0.0),
				156: (155.924752, 0.0),
				157: (156.925424, 0.0),
				158: (157.92785, 0.0),
				159: (158.929089, 0.0),
				160: (159.93197, 0.0),
				161: (160.93368, 0.0),
				162: (161.93704, 0.0),
				163: (162.93921, 0.0),
				164: (163.94299, 0.0),
				165: (164.94572, 0.0),
				166: (165.94997, 0.0),
				167: (166.95321, 0.0),
				},
		description=(
				"Soft silvery metallic element belonging to the lanthanoids. Eu-151 "
				"and Eu-153 are the only two stable isotopes, both of which are "
				"Neutron absorbers. Discovered in 1889 by Sir William Crookes."
				)
		)

Gd = Element(
		64,
		"Gd",
		"Gadolinium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=157.25,
		eleneg=1.2,
		eleaffin=0.5,
		covrad=1.61,
		atmrad=2.54,
		vdwrad=0.0,
		tboil=3545.0,
		tmelt=1585.0,
		density=7.89,
		eleconfig="[Xe] 4f7 5d 6s2",
		oxistates="3*",
		ionenergy=(6.1498, 12.1),
		isotopes={
				134: (133.95537, 0.0),
				135: (134.95257, 0.0),
				136: (135.94734, 0.0),
				137: (136.94502, 0.0),
				138: (137.94012, 0.0),
				139: (138.93824, 0.0),
				140: (139.93367, 0.0),
				141: (140.932126, 0.0),
				142: (141.92812, 0.0),
				143: (142.92675, 0.0),
				144: (143.92296, 0.0),
				145: (144.921709, 0.0),
				146: (145.918311, 0.0),
				147: (146.919094, 0.0),
				148: (147.918115, 0.0),
				149: (148.919341, 0.0),
				150: (149.918659, 0.0),
				151: (150.920348, 0.0),
				152: (151.919791, 0.002),
				153: (152.9217495, 0.0),
				154: (153.9208656, 0.0218),
				155: (154.922622, 0.148),
				156: (155.9221227, 0.2047),
				157: (156.9239601, 0.1565),
				158: (157.9241039, 0.2484),
				159: (158.9263887, 0.0),
				160: (159.9270541, 0.2186),
				161: (160.9296692, 0.0),
				162: (161.930985, 0.0),
				163: (162.93399, 0.0),
				164: (163.93586, 0.0),
				165: (164.93938, 0.0),
				166: (165.9416, 0.0),
				167: (166.94557, 0.0),
				168: (167.94836, 0.0),
				169: (168.95287, 0.0),
				},
		description=(
				"Soft silvery metallic element belonging to the lanthanoids. Seven "
				"natural, stable isotopes are known in addition to eleven artificial "
				"isotopes. Gd-155 and Gd-157 and the best neutron absorbers of all "
				"elements. Gadolinium compounds are used in electronics. Discovered "
				"by J.C.G Marignac in 1880."
				)
		)

Tb = Element(
		65,
		"Tb",
		"Terbium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=158.92535,
		eleneg=1.2,
		eleaffin=0.5,
		covrad=1.59,
		atmrad=2.51,
		vdwrad=0.0,
		tboil=3500.0,
		tmelt=1629.0,
		density=8.25,
		eleconfig="[Xe] 4f9 6s2",
		oxistates="4, 3*",
		ionenergy=(5.8638, 11.52),
		isotopes={
				136: (135.96138, 0.0),
				137: (136.95598, 0.0),
				138: (137.95316, 0.0),
				139: (138.94829, 0.0),
				140: (139.94581, 0.0),
				141: (140.94145, 0.0),
				142: (141.93874, 0.0),
				143: (142.93512, 0.0),
				144: (143.93305, 0.0),
				145: (144.92927, 0.0),
				146: (145.92725, 0.0),
				147: (146.924045, 0.0),
				148: (147.924272, 0.0),
				149: (148.923246, 0.0),
				150: (149.92366, 0.0),
				151: (150.923103, 0.0),
				152: (151.92407, 0.0),
				153: (152.923435, 0.0),
				154: (153.92468, 0.0),
				155: (154.923505, 0.0),
				156: (155.924747, 0.0),
				157: (156.9240246, 0.0),
				158: (157.9254131, 0.0),
				159: (158.9253468, 1.0),
				160: (159.9271676, 0.0),
				161: (160.9275699, 0.0),
				162: (161.92949, 0.0),
				163: (162.930648, 0.0),
				164: (163.93335, 0.0),
				165: (164.93488, 0.0),
				166: (165.93799, 0.0),
				167: (166.94005, 0.0),
				168: (167.94364, 0.0),
				169: (168.94622, 0.0),
				170: (169.95025, 0.0),
				171: (170.9533, 0.0),
				},
		description=(
				"Silvery metallic element belonging to the lanthanoids. Tb-159 is "
				"the only stable isotope, there are seventeen artificial isotopes. "
				"Discovered by G.G. Mosander in 1843."
				)
		)

Dy = Element(
		66,
		"Dy",
		"Dysprosium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=162.5,
		eleneg=1.22,
		eleaffin=0.5,
		covrad=1.59,
		atmrad=2.49,
		vdwrad=0.0,
		tboil=2840.0,
		tmelt=1685.0,
		density=8.56,
		eleconfig="[Xe] 4f10 6s2",
		oxistates="3*",
		ionenergy=(5.9389, 11.67),
		isotopes={
				138: (137.96249, 0.0),
				139: (138.95954, 0.0),
				140: (139.95401, 0.0),
				141: (140.95135, 0.0),
				142: (141.94637, 0.0),
				143: (142.94383, 0.0),
				144: (143.93925, 0.0),
				145: (144.93743, 0.0),
				146: (145.932845, 0.0),
				147: (146.931092, 0.0),
				148: (147.92715, 0.0),
				149: (148.927305, 0.0),
				150: (149.925585, 0.0),
				151: (150.926185, 0.0),
				152: (151.924718, 0.0),
				153: (152.925765, 0.0),
				154: (153.924424, 0.0),
				155: (154.925754, 0.0),
				156: (155.924283, 0.00056),
				157: (156.925466, 0.0),
				158: (157.924409, 0.00095),
				159: (158.9257392, 0.0),
				160: (159.9251975, 0.02329),
				161: (160.9269334, 0.18889),
				162: (161.9267984, 0.25475),
				163: (162.9287312, 0.24896),
				164: (163.9291748, 0.2826),
				165: (164.9317033, 0.0),
				166: (165.9328067, 0.0),
				167: (166.93566, 0.0),
				168: (167.93713, 0.0),
				169: (168.94031, 0.0),
				170: (169.94239, 0.0),
				171: (170.9462, 0.0),
				172: (171.94876, 0.0),
				173: (172.953, 0.0),
				},
		description=(
				"Metallic with a bright silvery-white lustre. Dysprosium belongs to "
				"the lanthanoids. It is relatively stable in air at room "
				"temperatures, it will however dissolve in mineral acids, evolving "
				"hydrogen. It is found in from rare-earth minerals. There are seven "
				"natural isotopes of dysprosium, and eight radioisotopes, Dy-154 "
				"being the most stable with a half-life of 3*10^6 years. Dysprosium "
				"is used as a neutron absorber in nuclear fission reactions, and in "
				"compact disks. It was discovered by Paul Emile Lecoq de Boisbaudran "
				"in 1886 in France. Its name comes from the Greek word dysprositos, "
				"which means hard to obtain."
				)
		)

Ho = Element(
		67,
		"Ho",
		"Holmium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=164.93033,
		eleneg=1.23,
		eleaffin=0.5,
		covrad=1.58,
		atmrad=2.47,
		vdwrad=0.0,
		tboil=2968.0,
		tmelt=1747.0,
		density=8.78,
		eleconfig="[Xe] 4f11 6s2",
		oxistates="3*",
		ionenergy=(6.0215, 11.8),
		isotopes={
				140: (139.96854, 0.0),
				141: (140.9631, 0.0),
				142: (141.95977, 0.0),
				143: (142.95461, 0.0),
				144: (143.95148, 0.0),
				145: (144.9472, 0.0),
				146: (145.94464, 0.0),
				147: (146.94006, 0.0),
				148: (147.93772, 0.0),
				149: (148.933775, 0.0),
				150: (149.933496, 0.0),
				151: (150.931688, 0.0),
				152: (151.931714, 0.0),
				153: (152.930199, 0.0),
				154: (153.930602, 0.0),
				155: (154.929103, 0.0),
				156: (155.92984, 0.0),
				157: (156.928256, 0.0),
				158: (157.928941, 0.0),
				159: (158.927712, 0.0),
				160: (159.928729, 0.0),
				161: (160.927855, 0.0),
				162: (161.929096, 0.0),
				163: (162.9287339, 0.0),
				164: (163.9302335, 0.0),
				165: (164.9303221, 1.0),
				166: (165.9322842, 0.0),
				167: (166.933133, 0.0),
				168: (167.93552, 0.0),
				169: (168.936872, 0.0),
				170: (169.93962, 0.0),
				171: (170.94147, 0.0),
				172: (171.94482, 0.0),
				173: (172.94729, 0.0),
				174: (173.95115, 0.0),
				175: (174.95405, 0.0),
				},
		description=(
				"Relatively soft and malleable silvery-white metallic element, "
				"which is stable in dry air at room temperature. It oxidizes in "
				"moist air and at high temperatures. It belongs to the lanthanoids. "
				"A rare-earth metal, it is found in the minerals monazite and "
				"gadolinite. It possesses unusual magnetic properties. One natural "
				"isotope, Ho-165 exists, six radioisotopes exist, the most stable "
				"being Ho-163 with a half-life of 4570 years. Holmium is used in "
				"some metal alloys, it is also said to stimulate the metabolism. "
				"Discovered by Per Theodor Cleve and J.L. Soret in Switzerland in "
				"1879. The name homium comes from the Greek word Holmia which means "
				"Sweden. While all holmium compounds should be considered highly "
				"toxic, initial evidence seems to indicate that they do not pose "
				"much danger. The metal's dust however, is a fire hazard."
				)
		)

Er = Element(
		68,
		"Er",
		"Erbium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=167.259,
		eleneg=1.24,
		eleaffin=0.5,
		covrad=1.57,
		atmrad=2.45,
		vdwrad=0.0,
		tboil=3140.0,
		tmelt=1802.0,
		density=9.05,
		eleconfig="[Xe] 4f12 6s2",
		oxistates="3*",
		ionenergy=(6.1077, 11.93),
		isotopes={
				143: (142.96634, 0.0),
				144: (143.96038, 0.0),
				145: (144.95739, 0.0),
				146: (145.952, 0.0),
				147: (146.94949, 0.0),
				148: (147.94455, 0.0),
				149: (148.94231, 0.0),
				150: (149.937914, 0.0),
				151: (150.937449, 0.0),
				152: (151.93505, 0.0),
				153: (152.935063, 0.0),
				154: (153.932783, 0.0),
				155: (154.933209, 0.0),
				156: (155.931065, 0.0),
				157: (156.93192, 0.0),
				158: (157.929893, 0.0),
				159: (158.930684, 0.0),
				160: (159.929083, 0.0),
				161: (160.929995, 0.0),
				162: (161.928778, 0.00139),
				163: (162.930033, 0.0),
				164: (163.9292, 0.01601),
				165: (164.930726, 0.0),
				166: (165.9302931, 0.33503),
				167: (166.9320482, 0.22869),
				168: (167.9323702, 0.26978),
				169: (168.9345904, 0.0),
				170: (169.9354643, 0.1491),
				171: (170.9380298, 0.0),
				172: (171.939356, 0.0),
				173: (172.9424, 0.0),
				174: (173.94423, 0.0),
				175: (174.94777, 0.0),
				176: (175.95008, 0.0),
				177: (176.95405, 0.0),
				},
		description=(
				"Soft silvery metallic element which belongs to the lanthanoids. "
				"Six natural isotopes that are stable. Twelve artificial isotopes "
				"are known. Used in nuclear technology as a neutron absorber. It is "
				"being investigated for other possible uses. Discovered by Carl G. "
				"Mosander in 1843."
				)
		)

Tm = Element(
		69,
		"Tm",
		"Thulium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=168.93422,
		eleneg=1.25,
		eleaffin=0.5,
		covrad=1.56,
		atmrad=2.42,
		vdwrad=0.0,
		tboil=2223.0,
		tmelt=1818.0,
		density=9.32,
		eleconfig="[Xe] 4f13 6s2",
		oxistates="3*, 2",
		ionenergy=(6.1843, 12.05, 23.71),
		isotopes={
				145: (144.97007, 0.0),
				146: (145.96643, 0.0),
				147: (146.96096, 0.0),
				148: (147.95784, 0.0),
				149: (148.95272, 0.0),
				150: (149.94996, 0.0),
				151: (150.945483, 0.0),
				152: (151.94442, 0.0),
				153: (152.942012, 0.0),
				154: (153.941568, 0.0),
				155: (154.939199, 0.0),
				156: (155.93898, 0.0),
				157: (156.93697, 0.0),
				158: (157.93698, 0.0),
				159: (158.93498, 0.0),
				160: (159.93526, 0.0),
				161: (160.93355, 0.0),
				162: (161.933995, 0.0),
				163: (162.932651, 0.0),
				164: (163.93356, 0.0),
				165: (164.932435, 0.0),
				166: (165.933554, 0.0),
				167: (166.9328516, 0.0),
				168: (167.934173, 0.0),
				169: (168.9342133, 1.0),
				170: (169.9358014, 0.0),
				171: (170.9364294, 0.0),
				172: (171.9384, 0.0),
				173: (172.939604, 0.0),
				174: (173.94217, 0.0),
				175: (174.94384, 0.0),
				176: (175.94699, 0.0),
				177: (176.94904, 0.0),
				178: (177.95264, 0.0),
				179: (178.95534, 0.0),
				},
		description=(
				"Soft grey metallic element that belongs to the lanthanoids. One "
				"natural isotope exists, Tm-169, and seventeen artificial isotopes "
				"have been produced. No known uses for the element. Discovered in "
				"1879 by Per Theodor Cleve."
				)
		)

Yb = Element(
		70,
		"Yb",
		"Ytterbium",
		group=3,
		period=6,
		block='f',
		series=9,
		mass=173.054,
		eleneg=1.1,
		eleaffin=0.5,
		covrad=1.74,
		atmrad=2.4,
		vdwrad=0.0,
		tboil=1469.0,
		tmelt=1092.0,
		density=9.32,
		eleconfig="[Xe] 4f14 6s2",
		oxistates="3*, 2",
		ionenergy=(6.2542, 12.17, 25.2),
		isotopes={
				148: (147.96742, 0.0),
				149: (148.96404, 0.0),
				150: (149.95842, 0.0),
				151: (150.9554, 0.0),
				152: (151.95029, 0.0),
				153: (152.94948, 0.0),
				154: (153.946394, 0.0),
				155: (154.945782, 0.0),
				156: (155.942818, 0.0),
				157: (156.942628, 0.0),
				158: (157.939866, 0.0),
				159: (158.94005, 0.0),
				160: (159.937552, 0.0),
				161: (160.937902, 0.0),
				162: (161.935768, 0.0),
				163: (162.936334, 0.0),
				164: (163.934489, 0.0),
				165: (164.93528, 0.0),
				166: (165.933882, 0.0),
				167: (166.93495, 0.0),
				168: (167.933897, 0.0013),
				169: (168.93519, 0.0),
				170: (169.9347618, 0.0304),
				171: (170.9363258, 0.1428),
				172: (171.9363815, 0.2183),
				173: (172.9382108, 0.1613),
				174: (173.9388621, 0.3183),
				175: (174.9412765, 0.0),
				176: (175.9425717, 0.1276),
				177: (176.9452608, 0.0),
				178: (177.946647, 0.0),
				179: (178.95017, 0.0),
				180: (179.95233, 0.0),
				181: (180.95615, 0.0),
				},
		description=(
				"Silvery metallic element of the lanthanoids. Seven natural "
				"isotopes and ten artificial isotopes are known. Used in certain "
				"steels. Discovered by J.D.G. Marignac in 1878."
				)
		)

Lu = Element(
		71,
		"Lu",
		"Lutetium",
		group=3,
		period=6,
		block='d',
		series=9,
		mass=174.9668,
		eleneg=1.27,
		eleaffin=0.5,
		covrad=1.56,
		atmrad=2.25,
		vdwrad=0.0,
		tboil=3668.0,
		tmelt=1936.0,
		density=9.84,
		eleconfig="[Xe] 4f14 5d 6s2",
		oxistates="3*",
		ionenergy=(5.4259, 13.9),
		isotopes={
				150: (149.97323, 0.0),
				151: (150.96758, 0.0),
				152: (151.96412, 0.0),
				153: (152.95877, 0.0),
				154: (153.95752, 0.0),
				155: (154.954316, 0.0),
				156: (155.95303, 0.0),
				157: (156.950098, 0.0),
				158: (157.949313, 0.0),
				159: (158.94663, 0.0),
				160: (159.94603, 0.0),
				161: (160.94357, 0.0),
				162: (161.94328, 0.0),
				163: (162.94118, 0.0),
				164: (163.94134, 0.0),
				165: (164.939407, 0.0),
				166: (165.93986, 0.0),
				167: (166.93827, 0.0),
				168: (167.93874, 0.0),
				169: (168.937651, 0.0),
				170: (169.938475, 0.0),
				171: (170.9379131, 0.0),
				172: (171.939086, 0.0),
				173: (172.9389306, 0.0),
				174: (173.9403375, 0.0),
				175: (174.9407718, 0.9741),
				176: (175.9426863, 0.0259),
				177: (176.9437581, 0.0),
				178: (177.945955, 0.0),
				179: (178.947327, 0.0),
				180: (179.94988, 0.0),
				181: (180.95197, 0.0),
				182: (181.95504, 0.0),
				183: (182.95757, 0.0),
				184: (183.96091, 0.0),
				},
		description=(
				"Silvery-white rare-earth metal which is relatively stable in air. "
				"It happens to be the most expensive rare-earth metal. Its found "
				"with almost all rare-earth metals, but is very difficult to "
				"separate from other elements. Least abundant of all natural "
				"elements. Used in metal alloys, and as a catalyst in various "
				"processes. There are two natural, stable isotopes, and seven "
				"radioisotopes, the most stable being Lu-174 with a half-life of 3.3 "
				"years. The separation of lutetium from Ytterbium was described by "
				"Georges Urbain in 1907. It was discovered at approximately the same "
				"time by Carl Auer von Welsbach. The name comes from the Greek word "
				"lutetia which means Paris."
				)
		)
