#!/usr/bin/env python3
#
#  synonyms.py
"""
Functions for obtaining the synonyms of a compound from the PubChem database.
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
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
from chemistry_tools.pubchem.pug_rest import do_rest_get

__all__ = ["Synonyms", "get_synonyms", "rest_get_synonyms"]


class Synonyms(List[str]):
	"""
	Contains a list of synonyms for a compound.

	:param initlist: The content to initialise the list with.
	"""

	def __init__(self, initlist):
		super().__init__()

		for val in initlist:
			self.append(str(val))

	def __contains__(self, synonym) -> bool:
		"""
		Return ``synonym in self``.

		The comparison treats hyphens and underscores as whitespace.

		:param synonym:
		"""

		for v in self:
			if self._prep_contains(v) == self._prep_contains(synonym):
				return True
		return False

	def append(self, synonym: str):
		"""
		Append ``synonym`` to the end of the list.

		:param synonym:
		"""

		if synonym not in self:
			super().append(str(synonym))

	@staticmethod
	def _prep_contains(val: str) -> str:
		val = val.casefold()

		for remove in ['-', '_', ' ']:
			val = val.replace(remove, ' ')

		return val


def get_synonyms(
		identifier: Union[str, int, Sequence[Union[str, int]]],
		namespace: Union[PubChemNamespace, str] = PubChemNamespace.name,
		) -> List[Dict]:
	"""
	Returns a list of synonyms for the compound with the given identifier.
	As more than one compound may be identified the results are returned in a list.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:param namespace: The type of identifier to look up.
		Valid values are in :class:`~.PubChemNamespace`.

	:return: List of dictionaries containing the CID and a list of synonyms for the compounds.
	"""

	data = rest_get_synonyms(identifier, namespace)

	results = []

	for compound in data["InformationList"]["Information"]:
		parsed_data = {
				"CID": compound["CID"],
				"synonyms": Synonyms(compound["Synonym"][:20]),
				}

		results.append(parsed_data)

	return results


def rest_get_synonyms(
		identifier: Union[str, int, Sequence[Union[str, int]]],
		namespace: Union[PubChemNamespace, str] = PubChemNamespace.name,
		**kwargs,
		) -> Dict:
	"""
	Get the list of synonyms for the given compound.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:param namespace: The type of identifier to look up. Valid values are in :class:`~.PubChemNamespace`
	:param kwargs: Optional arguments that ``json.loads`` takes.

	:raises ValueError: If the response body does not contain valid JSON.

	:return: Parsed JSON data.
	"""

	return do_rest_get(namespace, identifier, domain="synonyms").json(**kwargs)
