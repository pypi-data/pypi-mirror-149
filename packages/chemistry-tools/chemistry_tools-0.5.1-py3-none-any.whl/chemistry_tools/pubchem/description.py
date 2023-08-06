#!/usr/bin/env python3
#
#  description.py
"""
Functions to access the name and description of compounds in the PubChem database.
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

# stdlib
from typing import Any, Dict, List, Sequence, Union

# this package
from chemistry_tools.pubchem.enums import PubChemNamespace
from chemistry_tools.pubchem.properties import rest_get_properties_json
from chemistry_tools.pubchem.pug_rest import do_rest_get

__all__ = [
		"get_iupac_name",
		"get_description",
		"get_common_name",
		"get_compound_id",
		"rest_get_description",
		"parse_description"
		]


def get_iupac_name(name: str) -> str:
	"""
	Returns the systematic IUPAC name for the compound with the given name.

	:param name:
	"""

	data = rest_get_properties_json(name, PubChemNamespace.name, properties="IUPACName")
	iupac_name = data["PropertyTable"]["Properties"][0]["IUPACName"]
	return str(iupac_name)


def get_description(name: str) -> str:
	"""
	Returns the description compound with the given name.

	:param name:
	"""

	data = rest_get_description(name, PubChemNamespace.name)
	parsed_data = parse_description(data)
	return parsed_data[0]["Description"]


def get_common_name(name: str) -> str:
	"""
	Returns the common name for the compound with the given name.

	:param name:
	"""

	data = rest_get_description(name, PubChemNamespace.name)
	parsed_data = parse_description(data)
	return parsed_data[0]["Title"]


def get_compound_id(name: str) -> str:
	"""
	Returns the compound ID (CID) for the compound with the given name.

	:param name:
	"""

	data = rest_get_description(name, PubChemNamespace.name)
	parsed_data = parse_description(data)
	return parsed_data[0]["CID"]


def rest_get_description(
		identifier: Union[str, int, Sequence[Union[str, int]]],
		namespace: Union[PubChemNamespace, str] = PubChemNamespace.name,
		**kwargs,
		):
	"""
	Obtains the description for the given compound from the PubChem REST API.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:param namespace: The type of identifier to look up. Valid values are in :class:`~.PubChemNamespace`.
	:param kwargs: Optional arguments that ``json.loads`` takes.

	:raises ValueError: If the response body does not contain valid JSON.

	:return: Parsed JSON data
	"""

	return do_rest_get(namespace, identifier, domain="description").json(**kwargs)


def parse_description(description_data: Dict[str, Any]) -> List[Dict]:
	"""
	Parse raw data from the ``description`` endpoint of the REST API.

	:param description_data:

	:return: A list of dictionaries containing the CID, Title and Description for each compound
	"""

	compounds = {}
	fields = {"Title", "Description"}

	for entry in description_data["InformationList"]["Information"]:

		cid = entry["CID"]

		if cid not in compounds:
			compounds[cid] = {var: None for var in fields}
			compounds[cid]["CID"] = cid

		for var in fields:
			if var in entry:
				compounds[cid][var] = entry[var]

	return list(compounds.values())
