#!/usr/bin/env python3
#
#  _table.py
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
#

# stdlib
from typing import Dict, Tuple

__all__ = ("PERIODS", "BLOCKS", "GROUPS", "SERIES")

PERIODS: Dict[int, str] = {1: 'K', 2: 'L', 3: 'M', 4: 'N', 5: 'O', 6: 'P', 7: 'Q'}

BLOCKS = {'s': '', 'g': '', 'f': '', 'd': '', 'p': ''}

GROUPS: Dict[int, Tuple[str, str]] = {
		1: ("IA", "Alkali metals"),
		2: ("IIA", "Alkaline earths"),
		3: ("IIIB", ''),
		4: ("IVB", ''),
		5: ("VB", ''),
		6: ("VIB", ''),
		7: ("VIIB", ''),
		8: ("VIIIB", ''),
		9: ("VIIIB", ''),
		10: ("VIIIB", ''),
		11: ("IB", "Coinage metals"),
		12: ("IIB", ''),
		13: ("IIIA", "Boron group"),
		14: ("IVA", "Carbon group"),
		15: ("VA", "Pnictogens"),
		16: ("VIA", "Chalcogens"),
		17: ("VIIA", "Halogens"),
		18: ("VIIIA", "Noble gases"),
		}

SERIES: Dict[int, str] = {
		1: "Nonmetals",
		2: "Noble gases",
		3: "Alkali metals",
		4: "Alkaline earth metals",
		5: "Metalloids",
		6: "Halogens",
		7: "Poor metals",
		8: "Transition metals",
		9: "Lanthanides",
		10: "Actinides",
		}
