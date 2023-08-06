#!/usr/bin/env python3
#
#  full_record.py
"""
Functions for access the complete set of data held by PubChem for a compound.
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
from typing import Dict, List, Sequence, Union

# this package
from chemistry_tools.pubchem.enums import PubChemNamespace
from chemistry_tools.pubchem.properties import _parse_record_property
from chemistry_tools.pubchem.pug_rest import do_rest_get

__all__ = ["parse_full_record", "rest_get_full_record"]


def parse_full_record(record: Dict) -> List[Dict]:
	"""
	Parse the complete PubChem record for a compound.

	:param record:
	"""

	parsed_records = []

	for compound in record["PC_Compounds"]:
		cid = compound["id"]["id"]["cid"]
		# print(cid)

		counts = compound["count"]
		# pprint(counts)

		properties = []
		for prop in compound["props"]:
			prop = _parse_record_property(prop)
			properties.append(prop)

		if "bonds" in compound:
			bonds = compound["bonds"]
		else:
			bonds = {}

		if "charge" in compound:
			charge = compound["charge"]
		else:
			charge = 0

		parsed_records.append(
				dict(
						atoms=compound["atoms"],
						bonds=bonds,
						charge=charge,
						coords=compound["coords"],
						properties=properties,
						cid=cid,
						counts=counts
						)
				)

	return parsed_records


def rest_get_full_record(
		identifier: Union[str, int, Sequence[Union[str, int]]],
		namespace: Union[PubChemNamespace, str] = PubChemNamespace.name,
		record_type: str = "2d",
		**kwargs,
		) -> Dict:
	"""
	Obtains the full record for the given compound from the PubChem REST API.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:param namespace: The type of identifier to look up. Valid values are in :class:`~.PubChemNamespace`.
	:param record_type:
	:param kwargs: Optional arguments that ``json.loads`` takes.

	:raises ValueError: If the response body does not contain valid JSON.

	:return: Parsed JSON data
	"""

	return do_rest_get(namespace, identifier, record_type=record_type).json(**kwargs)
