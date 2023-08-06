#!/usr/bin/env python3
#
#  dataarray.py
"""
Provides a base class which can output data as a :class:`pandas.DataFrame`,
to CSV, or as a pretty-printed table in a variety of formats.
"""  # noqa: D400
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
from abc import abstractmethod
#  3rd party
from typing import Any, Dict, List, Optional, Set

# 3rd party
import pandas  # type: ignore
import tabulate  # nodep
from cawdrey import FrozenOrderedDict  # nodep
from domdf_python_tools.doctools import prettify_docstrings

__all__ = ["DataArray"]


@prettify_docstrings
class DataArray(FrozenOrderedDict):
	"""
	A class which can output data as a :class:`pandas.DataFrame`, to CSV,
	or as a pretty-printed table in a variety of formats.

	To use this class it must first be subclassed.
	Subclasses must implement :meth:`~DataArray.as_array` which handles the
	conversion of the data to a list of lists of values.

	:param formula: The formula in hill notation
	:param data: A dictionary of data to add to the internal :class:`~cawdrey.FrozenOrderedDict`
	"""  # noqa: D400

	_as_array_kwargs: Set[str] = set()
	_as_table_alignment: List[str] = []
	_as_table_float_format: List[Optional[str]] = []

	def __init__(self, formula: str, data: Dict):
		super().__init__(**data)
		self.formula: str = formula

	def as_csv(self, *args, sep: str = ',', **kwargs) -> str:
		r"""
		Returns the data as a CSV formatted string.

		:param \*args: Arguments passed to :meth:`~.DataArray.as_array`.
		:param sep: The separator for the CSV data.
		:param \*\*kwargs: Additional keyword arguments passed to :meth:`~.DataArray.as_array`.
		"""

		return '\n'.join(sep.join(x) for x in self.as_array(*args, **kwargs))

	@abstractmethod
	def as_array(self, sort_by: Any, reverse: bool = False) -> List[List[Any]]:
		"""
		Must be implemented in subclasses to hand the conversion of the data to a list of lists of values.

		:param sort_by:
		:param reverse:
		"""

	def as_dataframe(self, *args, **kwargs) -> pandas.DataFrame:
		"""
		Returns the isotope distribution data as a :class:`pandas.DataFrame`.

		Any arguments taken by :meth:`~.DataArray.as_array` can also be used here.
		"""

		array = self.as_array(*args, **kwargs)
		return pandas.DataFrame.from_records(array[1:], columns=array[0])

	def as_table(self, *args, **kwargs) -> str:
		"""
		Returns the isotope distribution data as a table using
		`tabulate <https://github.com/astanin/python-tabulate>`_.

		Any arguments taken by :meth:`~.DataArray.as_array` can also be used here.

		Additionally, any valid keyword argument for :func:`tabulate.tabulate` can be used.
		"""  # noqa: D400

		tabulate_kwargs: Dict[str, Any] = {}
		array_kwargs: Dict[str, Any] = {}

		for arg, val in kwargs.items():
			if arg in self._as_array_kwargs:
				array_kwargs[arg] = val
			else:
				tabulate_kwargs[arg] = val

		if "colalign" not in tabulate_kwargs:
			tabulate_kwargs["colalign"] = self._as_table_alignment

		if "floatfmt" not in tabulate_kwargs:
			tabulate_kwargs["floatfmt"] = self._as_table_float_format

		array = self.as_array(*args, **array_kwargs)

		return tabulate.tabulate(array[1:], array[0], **tabulate_kwargs)

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}({self.formula})>"
