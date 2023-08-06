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
"""This module provides a helper class for a row of time-stamped
register data."""
import copy
import json


class RegisterRow:
    """A row of register data contains a timestamp and the (signed 64-bit)
    values for that timestamp.  The timestamp is stored in member TS
    and the register values are stored in dictionary REGS, indexed by
    register name.

    """

    def __init__(self, ts, regs=None):
        self.ts = ts
        if regs is None:
            regs = {}
        self.regs = copy.copy(regs)

    def avg(self, regname):
        """Return the time-average of the register value."""
        return self.regs[regname] / self.ts

    def __sub__(self, subtrahend):
        """Subtract two register rows from each other and return the result.
        The SUBTRAHEND must have values for all of the registers in
        the minuend row.

        """
        ret = RegisterRow(self.ts, self.regs)
        ret.ts = float(ret.ts - subtrahend.ts)
        for name in self.regs:
            ret.regs[name] -= subtrahend.regs[name]
        return ret

    def __str__(self):
        return "%s: %s" % (self.ts, json.dumps(self.regs))
