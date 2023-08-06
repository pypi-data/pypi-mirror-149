#!/usr/bin/env python
#
#  property_format.py
"""
Format Physical Properties for Chemicals.
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# stdlib
import re
from decimal import Decimal

__all__ = ["degC", "equals", "scientific", "uscg1999", "f2c", "property_format"]

deg_c_re = re.compile(r"(\s*)(deg|DEG)(\s*)(C)")
dec_c_symbol = "°C"
mmath_space = '\u205f'
equals_re = re.compile(r"\s*=\s*")
scientific_regex = re.compile("X10.[0-9]+")
f2c_regex = re.compile(r"\d*\.?\d+ *° *F")


def degC(string: str) -> str:
	"""
	Correctly format a temperature in degrees Celsius.

	:param string:
	"""

	return deg_c_re.sub(f"{mmath_space}{dec_c_symbol}", string)


def equals(string: str) -> str:
	"""
	Correctly format an equals sign in a string.

	:param string:
	"""

	return equals_re.sub(" = ", string)


def scientific(string: str) -> str:
	"""
	Correctly format a string containing scientific notation.

	..TODO: Finish

	:param string:
	"""

	try:
		magnitude = scientific_regex.findall(string)[0].replace("X10", '').replace('-', '−')
	except IndexError:  # no scientific notation to format
		return string

	# print(magnitude)

	return scientific_regex.sub(f"×10<sup>{magnitude}</sup>", string)


def uscg1999(string: str) -> str:
	"""
	Strip references to the USCG dataset from the values.

	:param string:
	"""

	return string.replace("(USCG, 1999)", '')


def f2c(string: str) -> str:
	"""
	Convert temperature strings in degrees Fahrenheit to degrees Celsius.

	:param string:
	"""

	try:
		temperature = f2c_regex.findall(string)[0].replace('F', '').replace('°', '').replace(' ', '')
	except IndexError:
		return string

	# Convert to Celsius and strip trailing 0s and decimal points
	temperature = str((Decimal(temperature) - 32) * (Decimal(5) / Decimal(9)))
	if '.' in temperature:
		temperature = temperature.rstrip('0').rstrip('.')
	return f2c_regex.sub(f"{temperature}°C", string)


def property_format(string: str) -> str:
	"""
	Apply all property formatting functions to the string.

	:param string:
	"""

	return f2c(uscg1999(scientific(degC(equals(string))))).rstrip(' ')
