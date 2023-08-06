#!/usr/bin/env python3
#
#  toxnet.py
"""
Read data from National Library of Medicine TOXNET.
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
from decimal import Decimal
from typing import Any, Dict

# 3rd party
import requests
from bs4 import BeautifulSoup  # type: ignore  # nodep

# this package
from .property_format import *

__all__ = ["toxnet"]


def toxnet(cas: str):
	"""
	Obtain physical properties for the compound with the given CAS number from the ToxNet database.

	:param cas:
	"""

	try:
		base_url = "https://toxnet.nlm.nih.gov"
		origin_url = f"{base_url}/cgi-bin/sis/search2/r?dbs+hsdb:@term+@rn+@rel+{cas}"
		origin_page = requests.get(origin_url)
		origin_soup = BeautifulSoup(origin_page.text, "html.parser")
		# print(origin_url)
		# print(origin_soup.find("a", {"id": "anch_103"}))
		# print(origin_soup.find("input", {"name": "dfield"}))
		data_url = origin_soup.find("input", {"name": "dfield"}).find_next_sibling('a')["href"][:-4] + "cpp"
		# print(data_url)
		data_page = requests.get(base_url + data_url)
		data_soup = BeautifulSoup(data_page.text, "html.parser")
	except AttributeError:
		raise ValueError(f"No Record was found for {cas}")

	physical_properties: Dict[str, Any] = {}

	for prop in data_soup.findAll("h3"):
		prop_name = str(prop).replace("<h3>", '').replace(":</h3>", '')
		prop_value_and_unit = prop.nextSibling.replace('\n', '')

		if prop_name in ["Molecular Formula", "Molecular Weight"]:
			continue

		if prop_name == "Solubilities":
			prop_name = "Solubility"

		# elif prop_name == "Vapor Density":
		# 	physical_properties[prop_name] = prop_value_and_unit.replace(" (Air= 1)",'')
		# else:
		# 	physical_properties[prop_name] = property_format(prop_value_and_unit)

		physical_properties[prop_name] = {}

		# Parse values
		# Temperatures
		if prop_name in ["Boiling Point", "Melting Point"]:
			prop_value = prop_value_and_unit.split(" deg C")[0]
			try:
				physical_properties[prop_name]["Value"] = Decimal(prop_value)
			except:
				physical_properties[prop_name]["Value"] = property_format(prop_value)
			physical_properties[prop_name]["Unit"] = "°C"
			physical_properties[prop_name]["Description"] = None

		# Strings
		elif prop_name in [
				"Color/Form",
				"Odor",
				"Other Chemical/Physical Properties",
				"Solubility",
				"Spectral Properties",
				]:
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Unit"] = None
			physical_properties[prop_name]["Description"] = None

		# Custom Units &c.
		elif prop_name == "Density/Specific Gravity":
			try:
				physical_properties[prop_name]["Value"] = Decimal(prop_value_and_unit)
			except:
				physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Unit"] = "kg/m<sup>3</sup>"
			physical_properties[prop_name]["Description"] = None
		elif prop_name == "Vapor Density":
			# prop_value = prop_value_and_unit.split(" ")[0]
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit.replace(" (Air= 1)", ''))
			physical_properties[prop_name]["Unit"] = "None"
			physical_properties[prop_name]["Description"] = "Air=1"

		# TODO
		elif prop_name == "Dissociation Constants":
			# prop_value_list = prop_value_and_unit.split(" ")
			# prop_value = prop_value_list[2]
			# physical_properties[prop_name]["Value"] = prop_value
			# physical_properties[prop_name]["Unit"] = f"pKa @ {prop_value_list[4]}°C"
			physical_properties[prop_name]["Unit"] = None
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Description"] = None
		elif prop_name == "Heat of Combustion":
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Unit"] = None
			physical_properties[prop_name]["Description"] = None
		# TODO Extract J/KG value from string
		elif prop_name == "Octanol/Water Partition Coefficient":
			# prop_value = prop_value_and_unit.split("log Kow = ")[1]
			# print(prop_value)
			# print(prop_value_and_unit.split("log Kow = "))
			# TODO Fix
			# physical_properties[prop_name]["Value"] = prop_value
			# physical_properties[prop_name]["Unit"] = "log Kow"
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Unit"] = None
			physical_properties[prop_name]["Description"] = None
		elif prop_name == "Surface Tension":
			# prop_value_list = prop_value_and_unit.split(" ")
			# prop_value = prop_value_list[3]
			# print(prop_value_list)
			# physical_properties[prop_name]["Value"] = prop_value
			# physical_properties[prop_name]["Unit"] = f"N/M @ {prop_value_list[6]}°C"
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Unit"] = None
			physical_properties[prop_name]["Description"] = None
		elif prop_name == "Vapor Pressure":
			# prop_value_list = prop_value_and_unit.split(" ")
			# prop_value = prop_value_list[0]
			# physical_properties[prop_name]["Value"] = prop_value
			# physical_properties[prop_name]["Unit"] = f"mm Hg @ {prop_value_list[4]}°C"
			physical_properties[prop_name]["Value"] = property_format(prop_value_and_unit)
			physical_properties[prop_name]["Unit"] = None
			physical_properties[prop_name]["Description"] = None
	# else:
	# 	physical_properties[prop_name] = prop_value_and_unit

	return physical_properties


# Soup CAMEO Link from PubChem page if necessary

if __name__ == "__main__":
	# stdlib
	import pprint

	pprint.pprint(toxnet("122-39-4"))
# pprint.pprint(toxnet("85-98-3")) # No Record
# pprint.pprint(toxnet("71-43-2"))
