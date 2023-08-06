# ******************************************************************************
# Copyright (c) 2019 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************

from enum import Enum, unique

from .. import utils


@unique
class ADPDCommand(Enum):
    """
    ADPDCommand Enum
    """
    LOWEST = [0x40]
    LOAD_CONFIG_REQ = [0x42]
    LOAD_CONFIG_RES = [0x43]
    CLOCK_CALIBRATION_REQ = [0x44]
    CLOCK_CALIBRATION_RES = [0x45]
    SET_SLOT_REQ = [0x46]
    SET_SLOT_RES = [0x47]
    GET_SLOT_REQ = [0x48]
    GET_SLOT_RES = [0x49]
    COMMAND_DO_TEST1_REQ = [0x60]
    COMMAND_DO_TEST1_RES = [0x61]
    COMMAND_DO_TEST2_REQ = [0x62]
    COMMAND_DO_TEST2_RES = [0x63]
    COMMAND_DO_TEST3_REQ = [0x64]
    COMMAND_DO_TEST3_RES = [0x65]
    SET_PAUSE_REQ = [0x66]
    SET_PAUSE_RES = [0x67]
    COMMUNICATION_MODE_REQ = [0x68]
    COMMUNICATION_MODE_RES = [0x69]
    SET_SLOT_ACTIVE_REQ = [0x6A]
    SET_SLOT_ACTIVE_RES = [0x6B]
    GET_SLOT_ACTIVE_REQ = [0x6C]
    GET_SLOT_ACTIVE_RES = [0x6D]
    CREATE_DCFG_REQ = [0x70]
    CREATE_DCFG_RES = [0x71]
    SET_SAMPLING_FREQUENCY_REQ = [0x72]
    SET_SAMPLING_FREQUENCY_RES = [0x73]
    AGC_ON_OFF_REQ = [0x76]
    AGC_ON_OFF_RES = [0x77]
    AGC_INFO_REQ = [0x7A]
    AGC_INFO_RES = [0x7B]
    AGC_STATUS_REQ = [0x7C]
    AGC_STATUS_RES = [0x7D]
    SET_EXT_DATA_STREAM_ODR_REQ = [0x7E]
    SET_EXT_DATA_STREAM_ODR_RES = [0x7F]
    EXT_ADPD_DATA_STREAM = [0x80]
    UC_HR_ENABLE_REQ = [0x82]
    UC_HR_ENABLE_RES = [0x83]
    SATURATION_CHECK_ENABLE_REQ = [0x84]
    SATURATION_CHECK_ENABLE_RES = [0x85]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


class ADPDDevice(Enum):
    """
    ADPDDevice Enum
    """
    NULL = [0x0]
    DEVICE_GREEN = [0x28]
    DEVICE_RED = [0x29]
    DEVICE_INFRARED = [0x2A]
    DEVICE_BLUE = [0x2B]
    DEVICE_G_R_IR_B = [0x2C]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


class ADPDLed(Enum):
    """
    ADPDLed Enum
    """
    LED_MWL = [0x0]
    LED_GREEN = [0x1]
    LED_RED = [0x2]
    LED_IR = [0x3]
    LED_BLUE = [0x4]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


class ADPDSlot(Enum):
    """
    ADPDSlot Enum
    """
    NULL = [0x0]
    SLOT_A = [0x01]
    SLOT_B = [0x02]
    SLOT_C = [0x03]
    SLOT_D = [0x04]
    SLOT_E = [0x05]
    SLOT_F = [0x06]
    SLOT_G = [0x07]
    SLOT_H = [0x08]
    SLOT_I = [0x09]
    SLOT_J = [0x0A]
    SLOT_K = [0x0B]
    SLOT_L = [0x0C]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


class Clock(Enum):
    """
    Clock Enum
    """
    NO_CLOCK = [0x00]
    CLOCK_32K = [0x01]
    CLOCK_1M = [0x02]
    CLOCK_32M = [0x04]
    CLOCK_32K_AND_1M = [0x05]
    CLOCK_1M_AND_32M = [0x06]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


class ADPDAppID(Enum):
    """
    ADPDAppID Enum
    """
    APP_ECG = [0]
    APP_PPG = [1]
    APP_TEMPERATURE_THERMISTOR = [2]
    APP_TEMPERATURE_RESISTOR = [3]
    APP_ADPD_GREEN = [4]
    APP_ADPD_RED = [5]
    APP_ADPD_INFRARED = [6]
    APP_ADPD_BLUE = [7]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))
