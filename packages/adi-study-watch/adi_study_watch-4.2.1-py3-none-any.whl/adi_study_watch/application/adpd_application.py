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
import math
import time
import logging
from typing import Dict, List, Union, Tuple, Callable

from tqdm import tqdm

from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.packets.command_packet import CommandPacket
from ..core.packets.common_packets import StreamStatusPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.stream_data_packets import ADPDDataPacket, AGCDataPacket
from ..core.packets.common_packets import VersionPacket, DecimationFactorPacket
from ..core.enums.adpd_enums import ADPDDevice, ADPDCommand, ADPDSlot, Clock, ADPDLed, ADPDAppID
from ..core.packets.adpd_packets import SamplingFrequencyPacket, ADPDConfigPacket, ADPDUCHRPacket
from ..core.packets.adpd_packets import SlotPacket, ActiveSlotPacket, ComModePacket, AgcControlPacket
from ..core.packets.adpd_packets import ClockCalibrationPacket, ADPDPauseResumePacket, ADPDDCBCommandPacket, \
    SaturationCheckPacket
from ..core.packets.adpd_packets import ExternalStreamODR, ExternalStreamData, ADPDCreateDeviceConfiguration, \
    ADPDDCFGPacket, ADPDDCBPacket, ADPDRegisterReadPacket, ADPDRegisterWritePacket, ADPDLibraryConfigPacket

logger = logging.getLogger(__name__)


class ADPDApplication(CommonStream):
    """
    ADPD Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_adpd_application()

    """

    STREAM_ADPD1 = Stream.ADPD1
    STREAM_ADPD2 = Stream.ADPD2
    STREAM_ADPD3 = Stream.ADPD3
    STREAM_ADPD4 = Stream.ADPD4
    STREAM_ADPD5 = Stream.ADPD5
    STREAM_ADPD6 = Stream.ADPD6
    STREAM_ADPD7 = Stream.ADPD7
    STREAM_ADPD8 = Stream.ADPD8
    STREAM_ADPD9 = Stream.ADPD9
    STREAM_ADPD10 = Stream.ADPD10
    STREAM_ADPD11 = Stream.ADPD11
    STREAM_ADPD12 = Stream.ADPD12
    STREAM_STATIC_AGC = Stream.STATIC_AGC_STREAM

    DEVICE_GREEN = ADPDDevice.DEVICE_GREEN
    DEVICE_RED = ADPDDevice.DEVICE_RED
    DEVICE_INFRARED = ADPDDevice.DEVICE_INFRARED
    DEVICE_BLUE = ADPDDevice.DEVICE_BLUE
    DEVICE_G_R_IR_B = ADPDDevice.DEVICE_G_R_IR_B

    SLOT_A = ADPDSlot.SLOT_A
    SLOT_B = ADPDSlot.SLOT_B
    SLOT_C = ADPDSlot.SLOT_C
    SLOT_D = ADPDSlot.SLOT_D
    SLOT_E = ADPDSlot.SLOT_E
    SLOT_F = ADPDSlot.SLOT_F
    SLOT_G = ADPDSlot.SLOT_G
    SLOT_H = ADPDSlot.SLOT_H
    SLOT_I = ADPDSlot.SLOT_I
    SLOT_J = ADPDSlot.SLOT_J
    SLOT_K = ADPDSlot.SLOT_K
    SLOT_L = ADPDSlot.SLOT_L

    NO_CLOCK = Clock.NO_CLOCK
    CLOCK_32K = Clock.CLOCK_32K
    CLOCK_1M = Clock.CLOCK_1M
    CLOCK_32M = Clock.CLOCK_32M
    CLOCK_32K_AND_1M = Clock.CLOCK_32K_AND_1M
    CLOCK_1M_AND_32M = Clock.CLOCK_1M_AND_32M

    LED_MWL = ADPDLed.LED_MWL
    LED_GREEN = ADPDLed.LED_GREEN
    LED_RED = ADPDLed.LED_RED
    LED_IR = ADPDLed.LED_IR
    LED_BLUE = ADPDLed.LED_BLUE

    APP_ECG = ADPDAppID.APP_ECG
    APP_PPG = ADPDAppID.APP_PPG
    APP_TEMPERATURE_THERMISTOR = ADPDAppID.APP_TEMPERATURE_THERMISTOR
    APP_TEMPERATURE_RESISTOR = ADPDAppID.APP_TEMPERATURE_RESISTOR
    APP_ADPD_GREEN = ADPDAppID.APP_ADPD_GREEN
    APP_ADPD_RED = ADPDAppID.APP_ADPD_RED
    APP_ADPD_INFRARED = ADPDAppID.APP_ADPD_INFRARED
    APP_ADPD_BLUE = ADPDAppID.APP_ADPD_BLUE

    def __init__(self, packet_manager):
        super().__init__(Application.ADPD, Stream.ADPD6, packet_manager)
        self._dcb_size = 57

    def _adpd_stream_helper(self, stream: Stream) -> Stream:
        """
        Confirms stream is from list of Enums.
        """
        if stream in self.get_supported_streams():
            return stream
        else:
            logger.warning(f"{stream} is not supported stream, choosing {self.get_supported_streams()[5]} "
                           f"as default stream. use get_supported_streams() to know all supported streams.")
            return self.get_supported_streams()[5]

    def calibrate_clock(self, clock_id: Clock) -> Dict:
        """
        Calibrate clock to specified clock ID.

        :param clock_id: Clock ID to calibrate, use get_supported_clocks() to list all supported clock ID.
        :type clock_id: Clock
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5,8

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_clocks()
            print(x)
            # [<Clock.NO_CLOCK: ['0x0']>, ... , <Clock.CLOCK_32K_AND_1M: ['0x5']>, <Clock.CLOCK_1M_AND_32M: ['0x6']>]
            x = application.calibrate_clock(application.CLOCK_1M_AND_32M)
            print(x["payload"]["clock_id"])
            # Clock.CLOCK_1M_AND_32M

        """
        request_packet = ClockCalibrationPacket(self._destination, ADPDCommand.CLOCK_CALIBRATION_REQ)
        request_packet.set_payload("clock_id", clock_id)
        response_packet = ClockCalibrationPacket(self._destination, ADPDCommand.CLOCK_CALIBRATION_RES)
        return self._send_packet(request_packet, response_packet)

    def create_device_configuration(self, slot_app_ids: List[List[Union[ADPDSlot, ADPDAppID]]]) -> Dict:
        """
        Create ADPD device configuration.

        :param slot_app_ids: List of slot ID and APP ID to write, use get_supported_slots() to list all
                            | supported slot ID, and get_supported_app_id() to list all supported app ID.
        :type slot_app_ids: List[List[ADPDSlot, ADPDAppID]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.get_supported_app_id()
            print(x)
            # [<ADPDAppID.APP_PPG: ['0x1']>, <ADPDAppID.APP_ECG: ['0x0']>, ... , <ADPDAppID.APP_ADPD_BLUE: ['0x7']>]
            x = application.create_device_configuration([[application.SLOT_A, application.APP_ECG],
                                                        [application.SLOT_B, application.APP_ADPD_GREEN]])
            print(x["payload"]["data"])
            # [[<ADPDSlot.SLOT_A: ['0x1']>, <ADPDAppID.APP_ECG: ['0x0']>], ... ]
        """
        request_packet = ADPDCreateDeviceConfiguration(self._destination, ADPDCommand.CREATE_DCFG_REQ)
        request_packet.set_payload("size", len(slot_app_ids))
        request_packet.set_payload("data", slot_app_ids)
        response_packet = ADPDCreateDeviceConfiguration(self._destination, ADPDCommand.CREATE_DCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes ADPD Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.delete_device_configuration_block()
        """
        request_packet = ADPDDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        response_packet = ADPDDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_agc(self, led_list: List[ADPDLed]) -> Dict:
        """
        Disables AGC for LED in list.

        :param led_list: list of led to disable agc, use get_supported_led_ids() to list all supported led ID.
        :type led_list: List[ADPDLed]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x0']>, <ADPDLed.LED_RED: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x3']>]
            x = application.disable_agc([application.LED_GREEN, application.LED_RED])
            print(x["payload"]["agc_data"])
            # [[<ADPDLed.LED_MWL: ['0x0']>, False], [<ADPDLed.LED_GREEN: ['0x1']>, False]]
        """
        led_list = [[led, 0] for led in led_list]
        request_packet = AgcControlPacket(self._destination, ADPDCommand.AGC_ON_OFF_REQ)
        request_packet.set_payload("size", len(led_list))
        request_packet.set_payload("data", led_list)
        response_packet = AgcControlPacket(self._destination, ADPDCommand.AGC_ON_OFF_RES)
        return self._send_packet(request_packet, response_packet)

    # def disable_slot(self, slot_num: ADPDSlot) -> Dict:
    #     """
    #     Disable Specified ADPD Slot.
    #
    #     :param slot_num: slot_num to disable, use get_supported_slots() to list all supported slot ID.
    #     :type slot_num: ADPDSlot
    #     :return: A response packet as dictionary.
    #     :rtype: Dict
    #
    #     .. code-block:: python3
    #         :emphasize-lines: 5
    #
    #         from adi_study_watch import SDK
    #
    #         sdk = SDK("COM4")
    #         application = sdk.get_adpd_application()
    #         x = application.get_supported_slots()
    #         print(x)
    #         # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
    #         x = application.disable_slot(application.SLOT_A)
    #         print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
    #         # ADPDSlot.SLOT_A False
    #     """
    #     request_packet = ActiveSlotPacket(self._destination, ADPDCommand.SET_SLOT_ACTIVE_REQ)
    #     request_packet.set_payload("slot_num", slot_num)
    #     request_packet.set_payload("slot_enabled", 0)
    #     response_packet = ActiveSlotPacket(self._destination, ADPDCommand.SET_SLOT_ACTIVE_RES)
    #     return self._send_packet(request_packet, response_packet)

    def enable_agc(self, led_list: List[ADPDLed]) -> Dict:
        """
        Enables AGC for LEDs in list.

        :param led_list: list of led to enable agc, use get_supported_led_ids() to list all supported led ID.
        :type led_list: List[ADPDLed]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x0']>, <ADPDLed.LED_RED: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x3']>]
            x = application.enable_agc([application.LED_GREEN, application.LED_RED])
            print(x["payload"]["agc_data"])
            # [[<ADPDLed.LED_MWL: ['0x0']>, True], [<ADPDLed.LED_GREEN: ['0x1']>, True]]
        """
        led_list = [[led, 1] for led in led_list]
        request_packet = AgcControlPacket(self._destination, ADPDCommand.AGC_ON_OFF_REQ)
        request_packet.set_payload("size", len(led_list))
        request_packet.set_payload("data", led_list)
        response_packet = AgcControlPacket(self._destination, ADPDCommand.AGC_ON_OFF_RES)
        return self._send_packet(request_packet, response_packet)

    # def enable_slot(self, slot_num: ADPDSlot) -> Dict:
    #     """
    #     Enable Specified ADPD Slot.
    #
    #     :param slot_num: slot_num to enable, use get_supported_slots() to list all supported slot ID.
    #     :type slot_num: ADPDSlot
    #     :return: A response packet as dictionary.
    #     :rtype: Dict
    #
    #     .. code-block:: python3
    #         :emphasize-lines: 5
    #
    #         from adi_study_watch import SDK
    #
    #         sdk = SDK("COM4")
    #         application = sdk.get_adpd_application()
    #         x = application.get_supported_slots()
    #         print(x)
    #         # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
    #         x = application.enable_slot(application.SLOT_A)
    #         print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
    #         # ADPDSlot.SLOT_A  True
    #     """
    #     request_packet = ActiveSlotPacket(self._destination, ADPDCommand.SET_SLOT_ACTIVE_REQ)
    #     request_packet.set_payload("slot_num", slot_num)
    #     request_packet.set_payload("slot_enabled", 1)
    #     response_packet = ActiveSlotPacket(self._destination, ADPDCommand.SET_SLOT_ACTIVE_RES)
    #     return self._send_packet(request_packet, response_packet)

    def get_communication_mode(self) -> Dict:
        """
        Get ADPD communication mode.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_communication_mode()
            print(x["payload"]["com_mode"])
            # 2
        """
        request_packet = CommandPacket(self._destination, ADPDCommand.COMMUNICATION_MODE_REQ)
        response_packet = ComModePacket(self._destination, ADPDCommand.COMMUNICATION_MODE_RES)
        return self._send_packet(request_packet, response_packet)

    def get_decimation_factor(self, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Returns stream decimation factor.

        :param stream: Stream to get decimation factor.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            x = application.get_decimation_factor(application.STREAM_ADPD6)
            print(x["payload"]["decimation_factor"])
            # 1

        """
        stream = self._adpd_stream_helper(stream)
        request_packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_REQ)
        request_packet.set_payload("stream_address", stream)
        response_packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_RES)
        return self._send_packet(request_packet, response_packet)

    def get_device_configuration(self) -> List[Dict]:
        """
        Returns device configuration data.

        :return: A response packet as dictionary.
        :rtype: List[Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_device_configuration()
            print(x[0]["payload"]["data"])
            # [['0x9', '0x97'], ['0x7', '0x8FFF'], ['0xB', '0x2F6'], ... ]
        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_DCFG_REQ)
        response_packet = ADPDDCFGPacket(self._destination, CommonCommand.GET_DCFG_RES)
        return self._send_packet_multi_response(request_packet, response_packet)

    def get_sensor_status(self, stream=STREAM_ADPD6) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_sensor_status(application.STREAM_ADPD6)
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0
        """
        stream = self._adpd_stream_helper(stream)
        request_packet = StreamStatusPacket(self._destination, CommonCommand.GET_SENSOR_STATUS_REQ)
        request_packet.set_payload("stream_address", stream)
        response_packet = StreamStatusPacket(self._destination, CommonCommand.GET_SENSOR_STATUS_RES)
        return self._send_packet(request_packet, response_packet)

    def get_slot(self, slot_num: ADPDSlot) -> Dict:
        """
        Get Specified ADPD Slot Detail.

        :param slot_num: slot_num to get slot detail, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ..., <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.get_slot(application.SLOT_A)
            print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
            # <ADPDSlot.SLOT_A: ['0x1']> True
            print(x["payload"]["slot_format"], x["payload"]["channel_num"])
            # 3 3
        """
        request_packet = SlotPacket(self._destination, ADPDCommand.GET_SLOT_REQ)
        request_packet.set_payload("slot_num", slot_num)
        response_packet = SlotPacket(self._destination, ADPDCommand.GET_SLOT_RES)
        return self._send_packet(request_packet, response_packet)

    def get_slot_status(self, slot_num) -> Dict:
        """
        Returns whether slot is enabled or not.

        :param slot_num: slot_num to get status, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ..., <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.get_slot_status(application.SLOT_A)
            print(x["payload"]["slot_enabled"])
            # True
        """
        request_packet = ActiveSlotPacket(self._destination, ADPDCommand.GET_SLOT_ACTIVE_REQ)
        request_packet.set_payload("slot_num", slot_num)
        response_packet = ActiveSlotPacket(self._destination, ADPDCommand.GET_SLOT_ACTIVE_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_app_id() -> List[ADPDAppID]:
        """
        List all supported Apps for ADPD.

        :return: Array of APP ID enums.
        :rtype: List[ADPDAppID]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_app_id()
            print(x)
            # [<ADPDAppID.APP_PPG: ['0x1']>, <ADPDAppID.APP_ECG: ['0x0']>, ... , <ADPDAppID.APP_ADPD_BLUE: ['0x7']>]
        """
        return [ADPDApplication.APP_PPG, ADPDApplication.APP_ECG, ADPDApplication.APP_TEMPERATURE_THERMISTOR,
                ADPDApplication.APP_TEMPERATURE_RESISTOR, ADPDApplication.APP_ADPD_GREEN, ADPDApplication.APP_ADPD_RED,
                ADPDApplication.APP_ADPD_INFRARED, ADPDApplication.APP_ADPD_BLUE]

    @staticmethod
    def get_supported_clocks() -> List[Clock]:
        """
        List all supported clocks for ADPD.

        :return: Array of clock ID enums.
        :rtype: List[Clock]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_clocks()
            print(x)
            # [<Clock.NO_CLOCK: ['0x0']>, <Clock.CLOCK_32K: ['0x1']>, ... , <Clock.CLOCK_1M_AND_32M: ['0x6']>]
        """
        return [ADPDApplication.NO_CLOCK, ADPDApplication.CLOCK_32K, ADPDApplication.CLOCK_1M,
                ADPDApplication.CLOCK_32M, ADPDApplication.CLOCK_32K_AND_1M, ADPDApplication.CLOCK_1M_AND_32M]

    @staticmethod
    def get_supported_devices() -> List[ADPDDevice]:
        """
        List all supported devices for ADPD.

        :return: Array of device ID enums.
        :rtype: List[ADPDDevice]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_devices()
            print(x)
            # [<ADPDDevice.DEVICE_GREEN: ['0x28']>, ... , <ADPDDevice.DEVICE_G_R_IR_B: ['0x2C']>]
        """
        return [ADPDApplication.DEVICE_GREEN, ADPDApplication.DEVICE_RED, ADPDApplication.DEVICE_INFRARED,
                ADPDApplication.DEVICE_BLUE, ADPDApplication.DEVICE_G_R_IR_B]

    @staticmethod
    def get_supported_led_ids() -> List[ADPDLed]:
        """
        List all supported led IDs for ADPD.

        :return: Array of Led ID enums.
        :rtype: List[ADPDLed]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x4']>, <ADPDLed.LED_MWL: ['0x0']>]
        """
        return [ADPDApplication.LED_GREEN, ADPDApplication.LED_RED, ADPDApplication.LED_IR, ADPDApplication.LED_BLUE,
                ADPDApplication.LED_MWL]

    @staticmethod
    def get_supported_slots() -> List[ADPDSlot]:
        """
        List all supported slots for ADPD.

        :return: Array of slot ID enums.
        :rtype: List[ADPDSlot]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
        """
        return [ADPDApplication.SLOT_A, ADPDApplication.SLOT_B, ADPDApplication.SLOT_C, ADPDApplication.SLOT_D,
                ADPDApplication.SLOT_E, ADPDApplication.SLOT_F, ADPDApplication.SLOT_G, ADPDApplication.SLOT_H,
                ADPDApplication.SLOT_I, ADPDApplication.SLOT_J, ADPDApplication.SLOT_K, ADPDApplication.SLOT_L]

    @staticmethod
    def get_supported_streams() -> List[Stream]:
        """
        List all supported streams for ADPD.

        :return: Array of stream ID enums.
        :rtype: List[Stream]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD12: ['0xC2', '0x1D']>]
        """
        return [ADPDApplication.STREAM_ADPD1, ADPDApplication.STREAM_ADPD2, ADPDApplication.STREAM_ADPD3,
                ADPDApplication.STREAM_ADPD4, ADPDApplication.STREAM_ADPD5, ADPDApplication.STREAM_ADPD6,
                ADPDApplication.STREAM_ADPD7, ADPDApplication.STREAM_ADPD8, ADPDApplication.STREAM_ADPD9,
                ADPDApplication.STREAM_ADPD10, ADPDApplication.STREAM_ADPD11, ADPDApplication.STREAM_ADPD12,
                ADPDApplication.STREAM_STATIC_AGC]

    def get_version(self) -> Dict:
        """
        Returns ADPD version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_version()
            print(x["payload"]["major_version"])
            # 0
            print(x["payload"]["minor_version"])
            # 3
            print(x["payload"]["patch_version"])
            # 1
            print(x["payload"]["version_string"])
            # ADPD_App
            print(x["payload"]["build_version"])
            # TEST ADPD4000_VERSION STRING
        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        response_packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_RES)
        return self._send_packet(request_packet, response_packet)

    def load_configuration(self, device_id: ADPDDevice = DEVICE_GREEN) -> Dict:
        """
        Loads specified device id configuration.

        :param device_id: Device ID to load, use get_supported_devices() to list all supported devices.
        :type device_id: ADPDDevice
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5,8

             from adi_study_watch import SDK

             sdk = SDK("COM4")
             application = sdk.get_adpd_application()
             x = application.get_supported_devices()
             print(x)
             # [<ADPDDevice.DEVICE_GREEN: ['0x28']>, ... , <ADPDDevice.DEVICE_G_R_IR_B: ['0x2C']>]
             x = application.load_configuration(application.DEVICE_GREEN)
             print(x["payload"]["device_id"])
             # ADPDDevice.DEVICE_GREEN
         """
        request_packet = ADPDConfigPacket(self._destination, ADPDCommand.LOAD_CONFIG_REQ)
        request_packet.set_payload("device_id", device_id)
        response_packet = ADPDConfigPacket(self._destination, ADPDCommand.LOAD_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def pause(self) -> Dict:
        """
        Pause ADPDDevice.DEVICE_G_R_IR_B.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.pause()
            print(x["payload"]["device_id"], x["payload"]["pause"])
            # ADPDDevice.DEVICE_G_R_IR_B True
        """
        request_packet = ADPDPauseResumePacket(self._destination, ADPDCommand.SET_PAUSE_REQ)
        request_packet.set_payload("device_id", ADPDDevice.DEVICE_G_R_IR_B)
        request_packet.set_payload("pause", 1)
        response_packet = ADPDPauseResumePacket(self._destination, ADPDCommand.SET_PAUSE_RES)
        return self._send_packet(request_packet, response_packet)

    def read_device_configuration_block(self) -> [Dict]:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["data"])
        """
        request_packet = ADPDDCBCommandPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        response_packet = ADPDDCBPacket(self._destination, DCBCommand.READ_CONFIG_RES)
        return self._send_packet_multi_response(request_packet, response_packet)

    def read_library_configuration(self, fields: List[int]) -> Dict:
        """
        Reads library configuration from specified field values.

        :param fields: List of field values to read.
        :type fields: List[int]
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Fields Lower Limit
             - Fields Upper Limit
           * - 0x00
             - 0x00

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x12C']]
        """
        data = [[field, 0] for field in fields]
        request_packet = ADPDLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_REQ)
        request_packet.set_payload("size", len(data))
        request_packet.set_payload("data", data)
        response_packet = ADPDLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def read_register(self, addresses: List[int]) -> Dict:
        """
        Reads the register values of specified addresses. This function takes a list of addresses to read,
        and returns a response packet as dictionary containing addresses and values.

        :param addresses: List of register addresses to read.
        :type addresses: List[int]
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.read_register([0x15, 0x20, 0x2E])
            print(x["payload"]["data"])
            # [['0x15', '0x0'], ['0x20', '0x0'], ['0x2E', '0x0']]
        """
        data = [[address, 0] for address in addresses]
        request_packet = ADPDRegisterReadPacket(self._destination, CommonCommand.REGISTER_READ_REQ)
        request_packet.set_payload("size", len(data))
        request_packet.set_payload("data", data)
        response_packet = ADPDRegisterReadPacket(self._destination, CommonCommand.REGISTER_READ_RES)
        return self._send_packet(request_packet, response_packet)

    def resume(self) -> Dict:
        """
        Resumes ADPDDevice.DEVICE_G_R_IR_B.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.resume()
            print(x["payload"]["device_id"], x["payload"]["pause"])
            # ADPDDevice.DEVICE_G_R_IR_B False
        """
        request_packet = ADPDPauseResumePacket(self._destination, ADPDCommand.SET_PAUSE_REQ)
        request_packet.set_payload("device_id", ADPDDevice.DEVICE_G_R_IR_B)
        request_packet.set_payload("pause", 0)
        response_packet = ADPDPauseResumePacket(self._destination, ADPDCommand.SET_PAUSE_RES)
        return self._send_packet(request_packet, response_packet)

    # noinspection PyTypeChecker
    def set_callback(self, callback_function: Callable, args: Tuple = (), stream: Stream = STREAM_ADPD6) -> None:
        """
        Sets the callback for the stream data.

        :param callback_function: callback function for specified adpd stream.
        :param args: optional arguments that will be passed with the callback.
        :param stream: Callback for specified stream.
        :type stream: Stream
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2), stream=application.STREAM_ADPD6)
        """
        stream = self._adpd_stream_helper(stream)
        self._callback_function[stream] = callback_function
        self._args[stream] = args

    def set_decimation_factor(self, decimation_factor: int, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Sets decimation factor for specified ADPD stream.

        :param stream: Stream to set decimation factor.
        :type stream: Stream
        :param decimation_factor: decimation factor for stream
        :type decimation_factor: int
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Decimation Lower Limit
             - Decimation Upper Limit
           * - 0x01
             - 0x05

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            x = application.set_decimation_factor(2, application.STREAM_ADPD6)
            print(x["payload"]["decimation_factor"])
            # 2
        """
        stream = self._adpd_stream_helper(stream)
        request_packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_REQ)
        request_packet.set_payload("stream_address", stream)
        request_packet.set_payload("decimation_factor", decimation_factor)
        response_packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_RES)
        return self._send_packet(request_packet, response_packet)

    def set_sampling_frequency(self, odr: int) -> Dict:
        """
        Set ADPD sampling frequency, ODR value in Hz.

        :param odr: ODR frequency in Hz.
        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.set_sampling_frequency(100)
            print(x["payload"]["odr"])
            # 100
        """
        request_packet = SamplingFrequencyPacket(self._destination, ADPDCommand.SET_SAMPLING_FREQUENCY_REQ)
        request_packet.set_payload("odr", odr)
        response_packet = SamplingFrequencyPacket(self._destination, ADPDCommand.SET_SAMPLING_FREQUENCY_RES)
        return self._send_packet(request_packet, response_packet)

    def set_slot(self, slot_num: ADPDSlot, slot_enable: bool, slot_format: int, channel_num: int) -> Dict:
        """
        Set Slot with slot format.

        :param slot_num: slot_num to set slot, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :param slot_enable: enable or disable slot.
        :type slot_enable: bool
        :param slot_format: format of the slot, possible values are 0,1,2,3,4.
        :type slot_format: int
        :param channel_num: channel for the slot, possible values are 1,3.
        :type channel_num: int
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ..., <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.set_slot(application.SLOT_A, True, 3, 3)
            print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
            # ADPDSlot.SLOT_A True
            print(x["payload"]["slot_format"], x["payload"]["channel_num"])
            # 3 3

        """
        if not (channel_num == 0x1 or channel_num == 0x3):
            logger.warning(f"{'0x%X' % channel_num} is out of range, allowed values are: 1,3")
        request_packet = SlotPacket(self._destination, ADPDCommand.SET_SLOT_REQ)
        request_packet.set_payload("slot_num", slot_num)
        request_packet.set_payload("slot_enabled", slot_enable)
        request_packet.set_payload("slot_format", slot_format)
        request_packet.set_payload("channel_num", channel_num)
        response_packet = SlotPacket(self._destination, ADPDCommand.SET_SLOT_RES)
        return self._send_packet(request_packet, response_packet)

    def set_external_stream_sampling_frequency(self, odr: int) -> Dict:
        """
        Set ADPD external stream sampling frequency, ODR value in Hz.

        :param odr: ODR frequency in Hz.
        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.set_external_stream_sampling_frequency(50)
            print(x["payload"]["odr"])
            # 100
        """
        request_packet = ExternalStreamODR(self._destination, ADPDCommand.SET_EXT_DATA_STREAM_ODR_REQ)
        request_packet.set_payload("odr", odr)
        response_packet = ExternalStreamODR(self._destination, ADPDCommand.SET_EXT_DATA_STREAM_ODR_RES)
        return self._send_packet(request_packet, response_packet)

    def set_external_stream_data(self, csv_filename: str, start_row: int, column_index: int,
                                 display_progress: bool = False) -> None:
        """
        Set csv file data for external adpd stream.

        :param csv_filename: csv file to load stream data.
        :param start_row: start row index of data.
        :param column_index: column index of data
        :param display_progress: display detail progress bar.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.set_external_stream_data("12104AD0_ADPDAppStream_SlotFChannel2.csv", 6, 2,
                                                    display_progress=True)
        """
        timestamp = []
        data = []
        try:
            with open(csv_filename, 'r') as file:
                index_count = 1
                line = file.readline()
                csv_time = line.split(',')[2].strip()
                tz_seconds = int(line.split(',')[4].strip())
                hours = int(csv_time[0:2])
                minutes = int(csv_time[3:5])
                seconds = int(csv_time[6:8])
                absolute_time_ms = ((hours * 3600) + (minutes * 60) + seconds + tz_seconds) * 1000
                for line in file:
                    line = line.strip().split(",")
                    if index_count >= start_row:
                        timestamp.append(float(line[0].strip()))
                        data.append(int(line[column_index].strip()))
                    index_count += 1
        except Exception as e:
            logger.error(f"Error while reading the {csv_filename} file, reason :: {e}.", exc_info=True)
            return None
        progress_bar = None
        max_ticks_24_hr = 2764800000

        if display_progress:
            progress_bar = tqdm(total=len(data))
        sequence_number = 1
        for timestamp_value, data_value in zip(timestamp, data):
            request_packet = ExternalStreamData(self._destination, ADPDCommand.EXT_ADPD_DATA_STREAM)
            # converting ms to ticks
            timestamp_value = int(((timestamp_value + absolute_time_ms) * 32.768) % max_ticks_24_hr)
            request_packet.set_payload("sequence_num", sequence_number)
            request_packet.set_payload("data", data_value)
            request_packet.set_payload("timestamp", timestamp_value)
            sequence_number += 1
            time.sleep(0.001)
            if display_progress:
                progress_bar.update(1)
            self._packet_manager.send_packet(request_packet)
        if display_progress:
            progress_bar.close()
        return None

    def start_and_subscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Tuple[Dict, Dict]:
        """
        Starts ADPD sensor and also subscribe to the specified ADPD stream.

        :param stream: Stream to subscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        stream = self._adpd_stream_helper(stream)
        return super().start_and_subscribe_stream(stream)

    def stop_and_unsubscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Tuple[Dict, Dict]:
        """
        Stops ADPD sensor and also Unsubscribe the specified ADPD stream.

        :param stream: Stream to unsubscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        stream = self._adpd_stream_helper(stream)
        return super().stop_and_unsubscribe_stream(stream)

    def subscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Subscribe to the specified ADPD stream.

        :param stream: Stream to subscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        stream = self._adpd_stream_helper(stream)
        return super().subscribe_stream(stream)

    def unsubscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Unsubscribe the specified ADPD stream.

        :param stream: Stream to unsubscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        stream = self._adpd_stream_helper(stream)
        return super().unsubscribe_stream(stream)

    def write_device_configuration_block(self, addresses_values: List[List[int]]) -> [Dict]:
        """
        Writes the device configuration block values of specified addresses.
        This function takes a list of addresses and values to write, and returns a response packet as
        dictionary containing addresses and values.

        :param addresses_values: List of addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["size"])
            # 2
        """
        result = []
        packets = math.ceil(len(addresses_values) / self._dcb_size)
        for packet in range(packets):
            addresses_value = addresses_values[packet * self._dcb_size:(packet + 1) * self._dcb_size]
            request_packet = ADPDDCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
            request_packet.set_payload("size", len(addresses_value))
            request_packet.set_payload("packet_count", packets)
            request_packet.set_payload("data", addresses_value)
            response_packet = ADPDDCBCommandPacket(self._destination, DCBCommand.WRITE_CONFIG_RES)
            result.append(self._send_packet(request_packet, response_packet))
        return result

    def write_device_configuration_block_from_file(self, filename: str) -> [Dict]:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.write_device_configuration_block_from_file("adpd4000_dcb.dcfg")
        """
        result = self.device_configuration_file_to_list(filename)
        if result:
            return self.write_device_configuration_block(result)

    def write_library_configuration(self, fields_values: List[List[int]]) -> Dict:
        """
        Writes library configuration from List of fields and values.

        :param fields_values: List of fields and values to write.
        :type fields_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Fields Lower Limit
             - Fields Upper Limit
           * - 0x00
             - 0x00

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.write_library_configuration([[0x00, 0x12c]])
            print(x["payload"]["data"])
            # [['0x0', '0x12C']]
        """
        request_packet = ADPDLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        request_packet.set_payload("size", len(fields_values))
        request_packet.set_payload("data", fields_values)
        response_packet = ADPDLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def write_register(self, addresses_values: List[List[int]]) -> Dict:
        """
        Writes the register values of specified addresses. This function takes a list of addresses and values to write,
        and returns a response packet as dictionary containing addresses and values.

        :param addresses_values: List of register addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
            print(x["payload"]["data"])
            # [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']]
        """
        request_packet = ADPDRegisterWritePacket(self._destination, CommonCommand.REGISTER_WRITE_REQ)
        request_packet.set_payload("size", len(addresses_values))
        request_packet.set_payload("data", addresses_values)
        response_packet = ADPDRegisterWritePacket(self._destination, CommonCommand.REGISTER_WRITE_RES)
        return self._send_packet(request_packet, response_packet)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None, stream=None):
        """
        Process and returns the data back to user's callback function.
        """
        stream = Stream(packet[:2])
        if stream == self.STREAM_STATIC_AGC:
            self._callback_data_helper(packet, AGCDataPacket(), stream)
        else:
            self._callback_data_helper(packet, ADPDDataPacket(), stream)

    def enable_csv_logging(self, filename, header=None, stream: Stream = STREAM_ADPD6) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :param stream: ADPD Stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.enable_csv_logging("adpd6.csv", stream=application.STREAM_ADPD6)
        """
        stream = self._adpd_stream_helper(stream)
        if header is None:
            if stream == self.STREAM_ADPD1:
                header = ["Slot A", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD2:
                header = ["Slot B", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD3:
                header = ["Slot C", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD4:
                header = ["Slot D", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD5:
                header = ["Slot E", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD6:
                header = ["Slot F", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD7:
                header = ["Slot G", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD8:
                header = ["Slot H", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD9:
                header = ["Slot I", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD10:
                header = ["Slot J", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD11:
                header = ["Slot K", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD12:
                header = ["Slot L", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            if stream == self.STREAM_STATIC_AGC:
                header = ["Timestamp", ] + [f"MTS{i}" for i in range(0, 6)] + [f"Setting{i}" for i in range(0, 10)]
                self._csv_logger[stream] = CSVLogger(filename, header)
            else:
                self._csv_logger[stream] = CSVLogger(filename, header, write_header=False)

    def disable_csv_logging(self, stream: Stream = STREAM_ADPD6) -> None:
        """
        Stops logging stream data into CSV.

        :param stream: ADPD Stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.disable_csv_logging(stream=application.STREAM_ADPD6)
        """
        stream = self._adpd_stream_helper(stream)
        if self._csv_logger.get(stream):
            self._csv_logger[stream].stop_logging()
        self._csv_logger[stream] = None

    def enable_uc_hr(self, slot: ADPDSlot):
        """
        Enable UC HR.

        :param slot: use get_supported_slots() to list all supported slot ID.
        :type slot: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.enable_uc_hr(application.SLOT_F)

        """
        request_packet = ADPDUCHRPacket(self._destination, ADPDCommand.UC_HR_ENABLE_REQ)
        request_packet.set_payload("enabled", True)
        request_packet.set_payload("slot", slot)
        response_packet = ADPDUCHRPacket(self._destination, ADPDCommand.UC_HR_ENABLE_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_uc_hr(self, slot: ADPDSlot):
        """
        Disable UC HR.

        :param slot: use get_supported_slots() to list all supported slot ID.
        :type slot: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.disable_uc_hr(application.SLOT_F)
        """
        request_packet = ADPDUCHRPacket(self._destination, ADPDCommand.UC_HR_ENABLE_REQ)
        request_packet.set_payload("enabled", False)
        request_packet.set_payload("slot", slot)
        response_packet = ADPDUCHRPacket(self._destination, ADPDCommand.UC_HR_ENABLE_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_saturation_check(self, slot_list: List[ADPDSlot]) -> Dict:
        """
        Enables Saturation for slots in list.

        :param slot_list: list of slots to enable saturation check,
         use get_supported_slots() to list all supported slots.
        :type slot_list: List[ADPDSlot]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.enable_saturation_check([application.SLOT_A, application.SLOT_B])
        """
        slot_list = [[slot, 1] for slot in slot_list]
        request_packet = SaturationCheckPacket(self._destination, ADPDCommand.SATURATION_CHECK_ENABLE_REQ)
        request_packet.set_payload("size", len(slot_list))
        request_packet.set_payload("data", slot_list)
        response_packet = SaturationCheckPacket(self._destination, ADPDCommand.SATURATION_CHECK_ENABLE_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_saturation_check(self, slot_list: List[ADPDSlot]) -> Dict:
        """
        Disables Saturation for slots in list.

        :param slot_list: list of slots to enable saturation check,
         use get_supported_slots() to list all supported slots.
        :type slot_list: List[ADPDSlot]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.disable_saturation_check([application.SLOT_A, application.SLOT_B])
        """
        slot_list = [[slot, 0] for slot in slot_list]
        request_packet = SaturationCheckPacket(self._destination, ADPDCommand.SATURATION_CHECK_ENABLE_REQ)
        request_packet.set_payload("size", len(slot_list))
        request_packet.set_payload("data", slot_list)
        response_packet = SaturationCheckPacket(self._destination, ADPDCommand.SATURATION_CHECK_ENABLE_RES)
        return self._send_packet(request_packet, response_packet)
