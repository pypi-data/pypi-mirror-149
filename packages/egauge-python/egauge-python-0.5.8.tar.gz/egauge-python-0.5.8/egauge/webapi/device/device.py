#
# Copyright (c) 2020 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""Module to provide access to a device's JSON WebAPI."""

from .. import json_api

from ..error import Error


class DeviceError(Error):
    """Raised if for device related errors."""


class Device:
    """This class provides access to an eGauge device's JSON WebAPI.
    See "Web API Design" document for details."""

    def __init__(self, dev_uri, auth=None):
        """Return a device object that can be used to access the device a
        address DEV_URI.  An example DEV_URI would be
        "http://proto1.egaug.es".  AUTH should be an authentication object
        that provides the credentials to access the device.  Typically,
        this should be a JWTAuth object.

        """
        self.api_uri = dev_uri + "/api"
        self.auth = auth
        self._reg_idx = None
        self._reg_formula = None

    def get(self, resource, **kwargs):
        """Issue GET request for /api resource RESOURCE and return the parsed
        JSON data or None if the request failed or returned invalid
        JSON data.  Additional keyword arguments are passed on to
        requests.get().

        """
        return json_api.get(self.api_uri + resource, auth=self.auth, **kwargs)

    def put(self, resource, json_data, **kwargs):
        """Issue PUT request with JSON_DATA as body to /api resource RESOURCE
        and return parsed JSON reply or None if the request failed or
        returned invalid JSON data.  Additional keyword arguments are
        passed on to requests.put().

        """
        return json_api.put(
            self.api_uri + resource, json_data, auth=self.auth, **kwargs
        )

    def post(self, resource, json_data, **kwargs):
        """Issue POST request with JSON_DATA as body to /api resource RESOURCE
        and return parsed JSON reply or None if the request failed or
        returned invalid JSON data.  Additional keyword arguments are
        passed on to requests.post().

        """
        return json_api.post(
            self.api_uri + resource, json_data, auth=self.auth, **kwargs
        )

    def delete(self, resource, **kwargs):
        """Issue DELETE request for /api resource RESOURCE and return parsed
        JSON reply or None if the request failed or returned invalid
        JSON data.  Additional keyword arguments are passed on to
        requests.post().

        """
        return json_api.delete(
            self.api_uri + resource, auth=self.auth, **kwargs
        )

    def _fetch_reg_info(self):
        """Fetch register info, including type and virtual register
        formulas."""
        reply = self.get("/register", params={"virtual": "formula"})
        if reply is None or "registers" not in reply:
            raise DeviceError("Failed to fetch register info.", reply)
        self._reg_idx = {}
        self._reg_formula = {}
        for reg in reply["registers"]:
            self._reg_idx[reg["name"]] = reg["idx"]
            self._reg_formula[reg["name"]] = reg.get("formula")

    def reg_idx(self, regname):
        """Return the register index for the register with name REGNAME.  This
        information is cached in the device since it is relatively
        expensive to get (requires a separate call to /api/register).

        """
        if self._reg_idx is None:
            self._fetch_reg_info()
        return self._reg_idx[regname]

    def reg_formula(self, regname):
        """Return the register formula for the register with name REGNAME.
        This information is cached in the device since it is
        relatively expensive to get (requires a separate call to
        /api/register).

        """
        if self._reg_formula is None:
            self._fetch_reg_info()
        return self._reg_formula[regname]
