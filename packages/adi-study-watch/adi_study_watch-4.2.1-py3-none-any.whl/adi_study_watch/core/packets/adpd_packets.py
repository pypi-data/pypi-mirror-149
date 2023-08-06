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

from ..data_types.array import Array
from ..data_types.enums import Enums
from ..data_types.integer import Int
from ..data_types.binary import Binary
from .command_packet import CommandPacket
from ..enums.adpd_enums import ADPDDevice, ADPDSlot, Clock, ADPDLed, ADPDAppID
from ..enums.dcb_enums import DCBConfigBlockIndex


class ActiveSlotPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_SLOT_ACTIVE_RES: ['0x6B']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'slot_num': <ADPDSlot.SLOT_A: ['0x01']>,
                'slot_enabled': False
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["slot_num"] = Enums(1, enum_class=ADPDSlot)
        self._config["payload"]["slot_enabled"] = Binary(1)


class AgcControlPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xF',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.AGC_ON_OFF_RES: ['0x77']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 2,
                'data': [
                    [ <ADPDLed.LED_MWL: ['0x00']>, True ],
                    [ <ADPDLed.LED_GREEN: ['0x01']>, True ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2, data_types=[Binary(1), Enums(1, enum_class=ADPDLed)],
                                                reverse_inner_array=True)


class AgcInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x61',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.AGC_INFO_RES: ['0x7B']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'led_index': <ADPDLed.LED_GREEN: ['0x01']>,
                'ch1': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                'ch2': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                'dc0_led_current': 0,
                'tia_ch1': 0,
                'tia_ch2': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["led_index"] = Enums(1, enum_class=ADPDLed)
        self._config["payload"]["ch1"] = Array(40, dimension=1, data_types=[Int(4)])
        self._config["payload"]["ch2"] = Array(40, dimension=1, data_types=[Int(4)])
        self._config["payload"]["dc0_led_current"] = Int(2)
        self._config["payload"]["tia_ch1"] = Int(2)
        self._config["payload"]["tia_ch2"] = Int(2)


class AgcStatusPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.AGC_STATUS_RES: ['0x7D']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'agc_type': <ADPDLed.LED_GREEN: ['0x01']>,
                'agc_status': True
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["agc_type"] = Enums(1, enum_class=ADPDLed)
        self._config["payload"]["agc_status"] = Binary(1)


class ComModePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.COMMUNICATION_MODE_RES: ['0x69']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'com_mode': 2
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["com_mode"] = Int(1)


class SamplingFrequencyPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_SAMPLING_FREQUENCY_RES: ['0x73']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'odr': 100
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["odr"] = Int(2)


class SlotPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xF',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.GET_SLOT_RES: ['0x49']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'slot_num': <ADPDSlot.SLOT_F: ['0x06']>,
                'slot_enabled': True,
                'slot_format': 3,
                'channel_num': 3
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["slot_num"] = Enums(1, enum_class=ADPDSlot)
        self._config["payload"]["slot_enabled"] = Binary(1)
        self._config["payload"]["slot_format"] = Int(2, value_limit=[0, 4])
        self._config["payload"]["channel_num"] = Int(1, value_limit=[1, 3])


class TestCommandPacket(CommandPacket):

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["device_id"] = Array(2, data_types=[Int(1)], default=[0x00, 0x00])
        self._config["payload"]["data"] = Array(12, data_types=[Int(1, to_hex=True)])


class ADPDConfigPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x15',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.LOAD_CONFIG_RES: ['0x43']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'device_id': <ADPDDevice.DEVICE_GREEN: ['0x28']>,
                'data': [ 255, 255, 31, 0, 112, 7, 0, 99, 0, 0 ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["device_id"] = Enums(1, enum_class=ADPDDevice)
        self._config["payload"]["data"] = Array(10, data_types=[Int(1, to_hex=True)])


class ADPDPauseResumePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x15',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_PAUSE_RES: ['0x67']>,
                'status': <CommonStatus.ERROR: ['0x01']>,
                'device_id': <ADPDDevice.DEVICE_G_R_IR_B: ['0x2C']>,
                'pause': True
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["device_id"] = Enums(1, enum_class=ADPDDevice)
        self._config["payload"]["pause"] = Binary(10)


class ClockCalibrationPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.CLOCK_CALIBRATION_RES: ['0x45']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'clock_id': <Clock.CLOCK_1M_AND_32M: ['0x06']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["clock_id"] = Enums(1, enum_class=Clock)


class ExternalStreamData(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header':{
                'source': <Application.ADPD: ['0xC1','0x10']>,
                'destination': <Application.APP_USB: ['0xC7','0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
           'payload':{
                'command': <ADPDCommand.EXT_ADPD_DATA_STREAM: ['0x80']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_num': [ 2, 0, 0, 0 ],
                'data': [ 37, 26, 6, 0 ],
                'timestamp': [ 148, 201, 188, 2 ]
           }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["sequence_num"] = Int(4)
        self._config["payload"]["data"] = Int(4)
        self._config["payload"]["timestamp"] = Int(4)


class ExternalStreamODR(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_EXT_DATA_STREAM_ODR_RES: ['0x7F']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'odr': 50
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["odr"] = Int(2, value_limit=[25, 500])


class ADPDCreateDeviceConfiguration(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 19,
                'checksum': 0
            },
            'payload': {
                'command': <ADPDCommand.CREATE_DCFG_RES: ['0x71']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 2,
                'data': [
                    [ <ADPDSlot.SLOT_A: ['0x01']>, <ADPDAppID.APP_ECG: ['0x00']> ],
                    [ <ADPDSlot.SLOT_B: ['0x02']>, <ADPDAppID.APP_ADPD_GREEN: ['0x04']> ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Enums(2, enum_class=ADPDSlot, decode_with_int=True),
                                                    Enums(2, enum_class=ADPDAppID, decode_with_int=True)
                                                ])


class ADPDDCFGPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        [
            {
                'header': {
                    'source': <Application.ADPD: ['0xC1', '0x10']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 240,
                    'checksum': 0
                },
                'payload': {
                    'command': <CommonCommand.GET_DCFG_RES: ['0x26']>,
                    'status': <CommonStatus.OK: ['0x00']>,
                    'size': 57,
                    'packet_count': 2,
                    'data': [
                        [ '0x9', '0x97' ],
                        [ '0xB', '0x2E2' ],
                        ...
                        [ '0x1A5', '0x5' ],
                        [ '0x1A6', '0x0' ]
                    ]
                }
            },
            {
                'header': {
                    'source': <Application.ADPD: ['0xC1', '0x10']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 240,
                    'checksum': 0
                },
                'payload': {
                    'command': <CommonCommand.GET_DCFG_RES: ['0x26']>,
                    'status': <CommonStatus.OK: ['0x00']>,
                    'size': 10,
                    'packet_count': 2,
                    'data': [
                        [ '0x1A7', '0x120' ],
                        [ '0x1A8', '0x0' ],
                        ...
                        [ '0x1AF', '0x0' ],
                        [ '0x1B0', '0x4' ]
                    ]
                }
            }
        ]
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["packet_count"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(2, to_hex=True),
                                                    Int(2, to_hex=True)
                                                ], reverse_inner_array=True)


class ADPDDCBPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        [
            {
                'header': {
                    'source': <Application.ADPD: ['0xC1', '0x10']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 242,
                    'checksum': 0
                },
                'payload': {
                    'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                    'status': <DCBStatus.OK: ['0x97']>,
                    'size': 57,
                    'packet_count': 2,
                    'data': [
                        [ '0x9', '0x97' ],
                        [ '0xB', '0x6E2' ],
                        ...
                        [ '0x1A5', '0x5' ],
                        [ '0x1A6', '0x0' ]
                    ]
                }
            },
            {
                'header': {
                    'source': <Application.ADPD: ['0xC1', '0x10']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 242,
                    'checksum': 0
                },
                'payload': {
                    'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                    'status': <DCBStatus.OK: ['0x97']>,
                    'size': 10,
                    'packet_count': 2,
                    'data': [
                        [ '0x1A7', '0x120' ],
                        [ '0x1A8', '0x0' ],
                        ...
                        [ '0x1AF', '0x0' ],
                        [ '0x1B0', '0x4' ]
                    ]
                }
            }
        ]
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["packet_count"] = Int(2)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(2, to_hex=True),
                                                    Int(2, value_limit=[0x0000, 0x0277], to_hex=True)
                                                ], reverse_inner_array=True)


class ADPDDCBCommandPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.EDA: ['0xC3', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 20,
                'checksum': 0
            },
            'payload': {
                'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                'status': <DCBStatus.OK: ['0x97']>,
                'size': 1,
                'data': [
                    [ '0x0', '0x8' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["dcb_block_index"] = Enums(1, enum_class=DCBConfigBlockIndex,
                                                           default=DCBConfigBlockIndex.ADPD4000_BLOCK)


class ADPDRegisterReadPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 23,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.REGISTER_READ_RES: ['0x22']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 3,
                'data': [
                    [ '0x20', '0x2222' ],
                    [ '0x21', '0x0' ],
                    [ '0x22', '0x3' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(2, value_limit=[0x0000, 0x0277], to_hex=True),
                                                    Int(2, to_hex=True)
                                                ])


class ADPDRegisterWritePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 23,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.REGISTER_READ_RES: ['0x22']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 3,
                'data': [
                    [ '0x20', '0x2222' ],
                    [ '0x21', '0x0' ],
                    [ '0x22', '0x3' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(2, value_limit=[0x0000, 0x0277], to_hex=True),
                                                    Int(2, to_hex=True)
                                                ])


class ADPDLibraryConfigPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 14,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.WRITE_LCFG_RES: ['0x19']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 1,
                'data': [
                    [ '0x0', '0x1' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[
                                                    Int(1, value_limit=[0x0, 0x0], to_hex=True),
                                                    Int(2, to_hex=True)
                                                ])


class ADPDUCHRPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 13,
                'checksum': 0
            },
            'payload': {
                'command': <ADPDCommand.UC_HR_ENABLE_RES: ['0x83']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'enabled': True,
                'slot': <ADPDSlot.SLOT_F: ['0x06']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["enabled"] = Binary(1)
        self._config["payload"]["slot"] = Enums(2, enum_class=ADPDSlot, decode_with_int=True)


class SaturationCheckPacket(CommandPacket):
    """
    Packet Structure:

    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2,
                                                data_types=[Enums(1, enum_class=ADPDSlot), Binary(1)]
                                                )
