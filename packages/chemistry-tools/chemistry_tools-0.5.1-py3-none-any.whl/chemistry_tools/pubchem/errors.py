#  !/usr/bin/env python
#
#  errors.py
"""
Error handling.
"""
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
#  Based on PubChemPy https://github.com/mcs07/PubChemPy/blob/master/LICENSE
#  |  Copyright 2014 Matt Swain <m.swain@me.com>
#  |  Licensed under the MIT License
#  |
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# stdlib
import json

__all__ = [
		"ResponseParseError",
		"PubChemHTTPError",
		"BadRequestError",
		"NotFoundError",
		"MethodNotAllowedError",
		"TimeoutError",
		"HTTPTimeoutError",
		"UnimplementedError",
		"ServerError",
		"HTTP_ERROR_CODES",
		]

#: Numerical list of HTTP status codes considered to be errors.
HTTP_ERROR_CODES = [
		400,  # Bad Request
		401,  # Unauthorized
		402,  # Payment Required
		403,  # Forbidden
		404,  # Not Found
		405,  # Method Not Allowed
		406,  # Not Acceptable
		407,  # Proxy Authentication Required
		408,  # Request Timeout
		409,  # Conflict
		410,  # Gone
		411,  # Length Required
		412,  # Precondition Failed
		413,  # Payload Too Large
		414,  # URI Too Long
		415,  # Unsupported Media Type
		416,  # Range Not Satisfiable
		417,  # Expectation Failed
		421,  # Misdirected Request
		422,  # Unprocessable Entity
		423,  # Locked
		424,  # Failed Dependency
		425,  # Too Early
		426,  # Upgrade Required
		428,  # Precondition Required
		429,  # Too Many Requests
		431,  # Request Header Fields Too Large
		451,  # Unavailable For Legal Reasons
		500,  # Internal Server Error
		501,  # Not Implemented
		502,  # Bad Gateway
		503,  # Service Unavailable
		504,  # Gateway Timeout
		505,  # HTTP Version Not Supported
		506,  # Variant Also Negotiates
		507,  # Insufficient Storage
		508,  # Loop Detected
		509,  # Not Extended
		511,  # Network Authentication Required
		]


class ResponseParseError(Exception):
	"""
	PubChem response is uninterpretable.
	"""


class PubChemHTTPError(Exception):
	"""
	Generic error class to handle all HTTP error codes.
	"""

	def __init__(self, e):
		self.code = e.status_code
		self.msg = e.reason
		try:
			self.msg += f': {json.loads(e.content.decode())["Fault"]["Details"][0]}'
		except (ValueError, IndexError, KeyError):
			pass
		if self.code == 400:
			raise BadRequestError(self.msg)
		elif self.code == 404:
			raise NotFoundError(self.msg)
		elif self.code == 405:
			raise MethodNotAllowedError(self.msg)
		elif self.code == 504:
			raise HTTPTimeoutError(self.msg)
		elif self.code == 501:
			raise UnimplementedError(self.msg)
		elif self.code == 500:
			raise ServerError(self.msg)

	def __str__(self) -> str:
		return repr(self.msg)


class BadRequestError(PubChemHTTPError):
	"""
	Request is improperly formed (syntax error in the URL, POST body, etc.).
	"""

	def __init__(self, msg="Request is improperly formed"):
		self.msg = msg


class NotFoundError(PubChemHTTPError):
	"""
	The input record was not found (e.g. invalid CID).
	"""

	def __init__(self, msg="The input record was not found"):
		self.msg = msg


class MethodNotAllowedError(PubChemHTTPError):
	"""
	Request not allowed (such as invalid MIME type in the HTTP Accept header).
	"""

	def __init__(self, msg="Request not allowed"):
		self.msg = msg


class HTTPTimeoutError(PubChemHTTPError):
	"""
	The request timed out, from server overload or too broad a request.

	.. versionchanged:: 0.4.0  Renamed from TimeoutErrpr
	"""

	def __init__(self, msg="The request timed out"):
		self.msg = msg


TimeoutError = HTTPTimeoutError  # noqa: A001  # pylint: disable=redefined-builtin


class UnimplementedError(PubChemHTTPError):
	"""
	The requested operation has not (yet) been implemented by the server.
	"""

	def __init__(self, msg="The requested operation has not been implemented"):
		self.msg = msg


class ServerError(PubChemHTTPError):
	"""
	Some problem on the server side (such as a database server down, etc.).
	"""

	def __init__(self, msg="Some problem on the server side"):
		self.msg = msg
