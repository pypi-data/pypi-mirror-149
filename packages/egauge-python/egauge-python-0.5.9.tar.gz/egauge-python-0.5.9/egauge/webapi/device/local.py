#
# Copyright (c) 2020-2021 eGauge Systems LLC
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
import decimal
import json

from .register_row import RegisterRow


def sensor_port_name(index):
    """Sensor port name for sensor port with index INDEX, which must be
    in the range from 0..SENSOR_PORT_COUNT-1.

    """
    return "S%u" % (index + 1)


class Local:
    """Fetch data from /api/local."""

    # Sensor parameter spec strings:
    #   For l=...:
    SPEC_L1 = "L1"
    SPEC_L2 = "L2"
    SPEC_L3 = "L3"
    SPEC_L1_L2 = "L12"
    SPEC_L2_L3 = "L23"
    SPEC_L3_L1 = "L31"
    SPEC_LDC = "Ldc"

    # Sensor names as they appear in the output:
    NAME_L1 = "L1"
    NAME_L2 = "L2"
    NAME_L3 = "L3"
    NAME_L1_L2 = "L1-L2"
    NAME_L2_L3 = "L2-L3"
    NAME_L3_L1 = "L3-L1"
    NAME_LDC = "Ldc"
    NAME_TEMP_PCB = "Tpcb"
    NAME_HUMID_PCB = "Hpcb"

    METRIC_RATE = "rate"
    METRIC_CUMUL = "cumul"
    METRIC_TYPE = "type"

    MEASUREMENT_NORMAL = "n"
    MEASUREMENT_MEAN = "m"
    MEASUREMENT_FREQ = "f"

    SECTION_VALUES = "values"
    SECTION_ENERGY = "energy"
    SECTION_APPARENT = "apparent"

    def __init__(self, dev, params, **kwargs):
        self.raw = dev.get("/local", params=params, **kwargs)

    def ts(self):
        """Return the timestamp of the local data as a Decimal()."""
        if self.raw is None:
            return None
        return decimal.Decimal(self.raw["ts"])

    def type_code(self, sensor_name):
        """Return the type-code of sensor SENSOR_NAME."""
        if self.raw is None:
            return None
        try:
            return self.raw["values"][sensor_name]["type"]
        except KeyError:
            pass
        return None

    def rate(
        self,
        sensor_name,
        measurement=MEASUREMENT_NORMAL,
        section=SECTION_VALUES,
    ):
        """Return the rate of change value of sensor SENSOR_NAME.  By default,
        the normal value for the sensor is returned.  The mean value
        or frequency can be requested by passing MEASUREMENT_MEAN or
        MEASUREMENT_FREQ, respectively, as MEASUREMENT.  If the value
        is not available, None is returned.

        """
        if self.raw is None:
            return None
        try:
            m = self.raw[section][sensor_name]["rate"]
            if section == Local.SECTION_VALUES:
                return m[measurement]
            return m
        except KeyError:
            pass
        return None

    def cumul(
        self,
        sensor_name,
        measurement=MEASUREMENT_NORMAL,
        section=SECTION_VALUES,
    ):
        """Return the cumulative value of sensor SENSOR_NAME.  By default, the
        normal value for the sensor is returned.  The mean value or
        frequency can be requested by passing MEASUREMENT_MEAN or
        MEASUREMENT_FREQ, respectively, as MEASUREMENT.  If the value
        is not available, None is returned.

        """
        if self.raw is None:
            return None
        try:
            m = self.raw[section][sensor_name]["cumul"]
            if section == Local.SECTION_VALUES:
                return int(m[measurement])
            return int(m)
        except KeyError:
            pass
        return None

    def row(
        self,
        metric=METRIC_CUMUL,
        measurement=MEASUREMENT_NORMAL,
        section=SECTION_VALUES,
    ):
        """Return a timestamped row of register data.  By default, the
        cumulative normal values of section "values" is returned.
        Non-default rows can be selected by passing the desired values
        for METRIC, MEASUREMENT, and/or SECTION.

        """
        if self.raw is None:
            return None
        section = self.raw[section]
        regs = {}
        for key, metrics in section.items():
            if metric == Local.METRIC_TYPE:
                val = metrics[metric]
            else:
                val = metrics[metric]
                if section == Local.SECTION_VALUES:
                    val = val[measurement]
                if metric == Local.METRIC_CUMUL:
                    val = int(val)  # convert from decimal string to integer
            regs[key] = val
        return RegisterRow(self.ts(), regs)

    def __str__(self):
        return json.dumps(self.raw)
