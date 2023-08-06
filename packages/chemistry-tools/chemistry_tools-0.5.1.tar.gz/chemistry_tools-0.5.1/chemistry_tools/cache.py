#!/usr/bin/env python3
#
#  cache.py
"""
Cache for HTTP requests.
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

# 3rd party
from apeye import rate_limiter

__all__ = [
		"cache",
		"cache_dir",
		"cached_requests",
		"clear_cache",
		]

#: The cache object.
cache = rate_limiter.HTTPCache("chemistry_tools")

#: Instance of :class:`requests.Session` with a rate limit of 5 requests per second and a 28 day on-disk cache.
cached_requests = cache.session

#: The cache directory
cache_dir = cache.cache_dir


def clear_cache() -> None:
	"""
	Clear the cache.
	"""

	cache.clear()
