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
from .sqi_enum import SQICommand
from .bia_enums import BIACommand
from .ecg_enums import ECGCommand
from .eda_enums import EDACommand
from .ppg_enums import PPGCommand
from .adxl_enums import ADXLCommand
from .adpd_enums import ADPDCommand
from .low_touch_enum import LTCommand
from .ad7156_enums import AD7156Command
from .fs_enums import FSCommand, FSStatus
from .display_enums import DisplayCommand
from .dcb_enums import DCBCommand, DCBStatus
from .pedometer_enums import PedometerCommand
from .user0_enums import User0Command, User0Status
from .pm_enums import PMCommand, PMStatus, UICRCustomerRegisterAccessStatus


def get_command(command, source):
    """
    Helper method for decoding commands.
    """
    if command[0] < CommonCommand.HIGHEST.value[0]:
        return CommonCommand
    elif command in [DCBCommand.READ_CONFIG_RES.value, DCBCommand.WRITE_CONFIG_RES.value,
                     DCBCommand.ERASE_CONFIG_RES.value, DCBCommand.QUERY_STATUS_RES.value]:
        return DCBCommand
    elif source == Application.PM:
        return PMCommand
    elif source == Application.ADPD:
        return ADPDCommand
    elif source == Application.ADXL:
        return ADXLCommand
    elif source == Application.FS or source == Stream.FS:
        return FSCommand
    elif source == Application.PPG:
        return PPGCommand
    elif source == Application.SQI:
        return SQICommand
    elif source == Application.DISPLAY:
        return DisplayCommand
    elif source == Application.AD7156:
        return AD7156Command
    elif source == Application.BIA:
        return BIACommand
    elif source == Application.EDA:
        return EDACommand
    elif source == Application.LT_APP:
        return LTCommand
    elif source == Application.ECG:
        return ECGCommand
    elif source == Application.PEDOMETER:
        return PedometerCommand
    elif source == Application.USER0_APP:
        return User0Command
    else:
        return CommonCommand


def get_status(status, source, command):
    """
    Helper method for decoding status.
    """
    if command[0] == CommonCommand.ALARM_NOTIFICATION.value[0]:
        return AlarmStatus
    elif command in [PMCommand.WRITE_UICR_CUSTOMER_REG_RES.value, PMCommand.READ_UICR_CUSTOMER_REG_RES.value]:
        return UICRCustomerRegisterAccessStatus
    elif status[0] < CommonStatus.HIGHEST.value[0]:
        return CommonStatus
    elif command in [DCBCommand.READ_CONFIG_RES.value, DCBCommand.WRITE_CONFIG_RES.value,
                     DCBCommand.ERASE_CONFIG_RES.value]:
        return DCBStatus
    elif source == Application.PM:
        return PMStatus
    elif source == Application.USER0_APP:
        return User0Status
    elif source == Application.FS or source == Stream.FS:
        return FSStatus
    else:
        return CommonStatus


@unique
class CommonCommand(Enum):
    """
    CommonCommand Enum
    """
    NO_RESPONSE = [-1]
    GET_VERSION_REQ = [0x0]
    GET_VERSION_RES = [0x1]
    START_SENSOR_REQ = [0x4]
    START_SENSOR_RES = [0x5]
    STOP_SENSOR_REQ = [0x6]
    STOP_SENSOR_RES = [0x7]
    SUBSCRIBE_STREAM_REQ = [0xC]
    SUBSCRIBE_STREAM_RES = [0xD]
    UNSUBSCRIBE_STREAM_REQ = [0xE]
    UNSUBSCRIBE_STREAM_RES = [0xF]
    GET_SENSOR_STATUS_REQ = [0x10]
    GET_SENSOR_STATUS_RES = [0x11]
    GET_LCFG_REQ = [0x12]
    GET_LCFG_RES = [0x13]
    SET_LCFG_REQ = [0x14]
    SET_LCFG_RES = [0x15]
    READ_LCFG_REQ = [0x16]
    READ_LCFG_RES = [0x17]
    WRITE_LCFG_REQ = [0x18]
    WRITE_LCFG_RES = [0x19]
    PING_REQ = [0x1A]
    PING_RES = [0x1B]
    ALARM_NOTIFICATION = [0x1C]
    REGISTER_READ_REQ = [0x21]
    REGISTER_READ_RES = [0x22]
    REGISTER_WRITE_REQ = [0x23]
    REGISTER_WRITE_RES = [0x24]
    GET_DCFG_REQ = [0x25]
    GET_DCFG_RES = [0x26]
    STREAM_DATA = [0x28]
    GET_STREAM_DEC_FACTOR_REQ = [0x29]
    GET_STREAM_DEC_FACTOR_RES = [0x2A]
    SET_STREAM_DEC_FACTOR_REQ = [0x2B]
    SET_STREAM_DEC_FACTOR_RES = [0x2C]
    REGISTER_READ_32_REQ = [0x2D]
    REGISTER_READ_32_RES = [0x2E]
    REGISTER_WRITE_32_REQ = [0x2F]
    REGISTER_WRITE_32_RES = [0x30]
    HIGHEST = [0x40]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class CommonStatus(Enum):
    """
    CommonStatus Enum
    """
    NO_RESPONSE = [-1]
    OK = [0x0]
    ERROR = [0x1]
    STREAM_STARTED = [0x2]
    STREAM_STOPPED = [0x3]
    STREAM_IN_PROGRESS = [0x4]
    STREAM_DEACTIVATED = [0x5]
    STREAM_COUNT_DECREMENT = [0x6]
    STREAM_NOT_STARTED = [0x7]
    STREAM_NOT_STOPPED = [0x8]
    SUBSCRIBER_ADDED = [0x9]
    SUBSCRIBER_REMOVED = [0xA]
    SUBSCRIBER_COUNT_DECREMENT = [0xB]
    HIGHEST = [0x20]
    NEW_STREAM_STATUS = [0x43]  # some stream such as EDA has 0x43 as status instead of 0x0

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class Stream(Enum):
    """
    Stream Enum
    """
    NULL = [0x00, 0x00]
    ADPD1 = [0xc2, 0x11]
    ADPD2 = [0xc2, 0x12]
    ADPD3 = [0xc2, 0x13]
    ADPD4 = [0xc2, 0x14]
    ADPD5 = [0xc2, 0x15]
    ADPD6 = [0xc2, 0x16]
    ADPD7 = [0xc2, 0x17]
    ADPD8 = [0xc2, 0x18]
    ADPD9 = [0xc2, 0x19]
    ADPD10 = [0xc2, 0x1a]
    ADPD11 = [0xc2, 0x1b]
    ADPD12 = [0xc2, 0x1c]
    ADXL = [0xc2, 0x02]
    BIA = [0xC4, 0x07]
    ECG = [0xc4, 0x01]
    EDA = [0xc4, 0x02]
    FS = [0xC6, 0x01]
    PEDOMETER = [0xc4, 0x04]
    PPG = [0xC4, 0x00]
    # TEMPERATURE = [0xc4, 0x06]
    SYNC_PPG = [0xC4, 0x05]
    SQI = [0xC8, 0x0D]
    BATTERY = [0xC6, 0x91]
    DYNAMIC_AGC_STREAM = [0xC6, 0xB0]
    STATIC_AGC_STREAM = [0xC6, 0xB1]
    HRV = [0xC6, 0xC0]
    AD7156 = [0xC8, 0x15]
    TEMPERATURE1 = [0xC8, 0x16]
    TEMPERATURE2 = [0xC8, 0x17]
    TEMPERATURE3 = [0xC8, 0x18]  # C
    TEMPERATURE4 = [0xC4, 0x06]  # D
    TEMPERATURE5 = [0xC8, 0x1A]
    TEMPERATURE6 = [0xC8, 0x1B]
    TEMPERATURE7 = [0xC8, 0x1C]
    TEMPERATURE8 = [0xC8, 0x1D]
    TEMPERATURE9 = [0xC8, 0x1E]
    TEMPERATURE10 = [0xC8, 0x1F]  # J
    TEMPERATURE11 = [0xC8, 0x20]  # K
    TEMPERATURE12 = [0xC8, 0x21]  # L

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class Application(Enum):
    """
    Application Enum.
    """
    POST_OFFICE = [0xC0, 0x0]
    EXTERNAL = [0xC0, 0x01]
    ADXL = [0xc1, 0x02]
    ADPD = [0xc1, 0x10]
    PPG = [0xC3, 0x00]
    ECG = [0xc3, 0x01]
    EDA = [0xc3, 0x02]
    PEDOMETER = [0xc3, 0x04]
    TEMPERATURE = [0xc3, 0x06]
    BIA = [0xC3, 0x07]
    FS = [0xC5, 0x01]
    PS = [0xc5, 0x80]
    PM = [0xc5, 0x00]
    DISPLAY = [0xC5, 0x03]
    APP_ANDROID = [0xC7, 0x0]
    APP_IOS = [0xC7, 0x1]
    APP_VS = [0xC7, 0x2]
    APP_WT = [0xC7, 0x3]
    APP_NFE = [0xC7, 0x4]
    APP_USB = [0xc7, 0x05]
    SQI = [0xC8, 0x0C]
    AD7156 = [0xC8, 0x0B]
    APP_BLE = [0xC8, 0x08]
    LT_APP = [0xC8, 0x0A]
    USER0_APP = [0xC8, 0x0F]
    NULL = [0x0, 0x0]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class AlarmStatus(Enum):
    BATTERY_LEVEL_LOW = [0x0]
    BATTERY_LEVEL_CRITICAL = [0x1]
    BATTERY_LEVEL_FULL = [0x2]
    USER_CONFIG_LOG_ENABLED = [0x3]
    ENABLE_USER_CONFIG_LOG_FAILED = [0x4]
    USER_CONFIG_LOG_DISABLED = [0x5]
    DISABLE_USER_CONFIG_LOG_FAILED = [0x6]
    DCB_CONFIG_LOG_ENABLED = [0x7]
    ENABLE_DCB_CONFIG_LOG_FAILED = [0x8]
    DCB_CONFIG_LOG_DISABLED = [0x9]
    DISABLE_DCB_CONFIG_LOG_FAILED = [0xA]
    LOW_TOUCH_LOGGING_ALREADY_STARTED = [0xB]
    CONFIG_FILE_NOT_FOUND = [0xC]
    CONFIG_FILE_READ_ERR = [0xD]
    LOW_TOUCH_MEMORY_FULL_ERR = [0xE]
    LOW_TOUCH_MAX_FILE_ERR = [0xF]
    FS_STOP_LOGGING = [0x10]
    FS_MEMORY_FULL = [0x11]
    FS_BATTERY_CRITICAL = [0x12]
    FS_PWR_STATE_SHUTDOWN = [0x13]
    HIGHEST = [0x20]
