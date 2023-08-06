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
from typing import List, Dict, Callable, Optional

from tqdm import tqdm

from .fs_application import FSApplication
from ..core.enums.ppg_enums import PPGCommand
from ..core.enums.bia_enums import BIACommand
from ..core.enums.adxl_enums import ADXLCommand
from .common_application import CommonApplication
from ..core.enums.fs_enums import FSCommand, FSStatus
from ..core.packets.common_packets import StreamPacket
from ..core.packets.ppg_packets import PPGStatesPacket
from ..core.packets.command_packet import CommandPacket
from ..core.enums.adpd_enums import ADPDCommand, ADPDLed
from ..core.enums.display_enums import DisplayColor, DisplayCommand
from ..core.packets.adpd_packets import AgcInfoPacket, TestCommandPacket
from ..core.packets.bia_packets import FDSStatusPacket, DCBTimingInfoPacket
from ..core.enums.pm_enums import PMCommand, PowerMode, LDO, ElectrodeSwitch
from ..core.packets.display_packets import SetDisplayPacket, EnableDisplayPacket
from ..core.packets.fs_packets import StreamDebugInfoPacket, FileInfoResponsePacket
from ..core.enums.common_enums import Application, CommonCommand, Stream, CommonStatus
from ..core.packets.pm_packets import LDOControlPacket, SwitchControlPacket, PingPacket
from ..core.packets.stream_data_packets import KeyStreamDataPacket, CapSenseStreamDataPacket
from ..core.packets.pm_packets import AppsHealthPacket, ControlPacket, PowerStatePacket, BatteryThresholdPacket
from ..core.packets.fs_packets import PatternWritePacket, DebugInfoPacket, BadBlockPacket, PageInfoRequestPacket, \
    PageInfoResponsePacket, FileInfoRequestPacket

logger = logging.getLogger(__name__)


class TestApplication(CommonApplication):
    WHITE = DisplayColor.WHITE
    BLACK = DisplayColor.BLACK
    RED = DisplayColor.RED
    GREEN = DisplayColor.GREEN
    BLUE = DisplayColor.BLUE

    POWER_MODE_ACTIVE = PowerMode.ACTIVE
    POWER_MODE_HIBERNATE = PowerMode.HIBERNATE
    POWER_MODE_SHUTDOWN = PowerMode.SHUTDOWN

    LDO_FS = LDO.FS
    LDO_OPTICAL = LDO.OPTICAL
    LDO_EPHYZ = LDO.EPHYZ

    SWITCH_AD8233 = ElectrodeSwitch.AD8233
    SWITCH_AD5940 = ElectrodeSwitch.AD5940
    SWITCH_ADPD4000 = ElectrodeSwitch.ADPD4000

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
    STREAM_ADXL = Stream.ADXL
    STREAM_BCM = Stream.BIA
    STREAM_ECG = Stream.ECG
    STREAM_EDA = Stream.EDA
    STREAM_PEDOMETER = Stream.PEDOMETER
    STREAM_PPG = Stream.PPG
    STREAM_TEMPERATURE1 = Stream.TEMPERATURE1
    STREAM_TEMPERATURE2 = Stream.TEMPERATURE2
    STREAM_TEMPERATURE3 = Stream.TEMPERATURE3
    STREAM_TEMPERATURE4 = Stream.TEMPERATURE4
    STREAM_TEMPERATURE5 = Stream.TEMPERATURE5
    STREAM_TEMPERATURE6 = Stream.TEMPERATURE6
    STREAM_TEMPERATURE7 = Stream.TEMPERATURE7
    STREAM_TEMPERATURE8 = Stream.TEMPERATURE8
    STREAM_TEMPERATURE9 = Stream.TEMPERATURE9
    STREAM_TEMPERATURE10 = Stream.TEMPERATURE10
    STREAM_TEMPERATURE11 = Stream.TEMPERATURE11
    STREAM_TEMPERATURE12 = Stream.TEMPERATURE12
    STREAM_SYNC_PPG = Stream.SYNC_PPG
    STREAM_SQI = Stream.SQI

    LED_MWL = ADPDLed.LED_MWL
    LED_GREEN = ADPDLed.LED_GREEN
    LED_RED = ADPDLed.LED_RED
    LED_IR = ADPDLed.LED_IR
    LED_BLUE = ADPDLed.LED_BLUE

    def __init__(self, key_press_callback_function, cap_sense_callback_function, packet_manager):
        super().__init__(Application.FS, packet_manager)
        self._key_press_callback = key_press_callback_function
        self._cap_sense_callback = cap_sense_callback_function

    # PM
    def flash_reset(self) -> Dict:
        """
        Resets device flash.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.flash_reset()
            print(x["payload"]["status"])
            # PMStatus.OK

        """
        request_packet = CommandPacket(Application.PM, PMCommand.FLASH_RESET_REQ)
        response_packet = CommandPacket(Application.PM, PMCommand.FLASH_RESET_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_power_states() -> List[PowerMode]:
        """
        List all supported power states for PM.

        :return: Array of power states enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_power_states()
            print(x)
            # [<PowerState.ACTIVE_MODE: ['0x0']>, ... , <PowerState.SHUTDOWN_MODE: ['0x3']>]
        """
        return [TestApplication.POWER_MODE_ACTIVE, TestApplication.POWER_MODE_HIBERNATE,
                TestApplication.POWER_MODE_SHUTDOWN]

    def set_power_mode(self, power_state: PowerMode) -> Dict:
        """
        Set specified power state to PM.

        :param power_state: power state to set, use get_supported_power_states() to list all supported power states.
        :type power_state: PowerMode
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_power_states()
            print(x)
            # [<PowerState.ACTIVE_MODE: ['0x0']>, ... , <PowerState.SHUTDOWN_MODE: ['0x3']>]
            x = application.set_power_mode(application.ACTIVE_MODE)
            print(x["payload"]["power_state"])
            # PowerState.ACTIVE_MODE

        """
        request_packet = PowerStatePacket(Application.PM, PMCommand.SET_POWER_STATE_REQ)
        request_packet.set_payload("power_state", power_state)
        response_packet = PowerStatePacket(Application.PM, PMCommand.SET_POWER_STATE_RES)
        return self._send_packet(request_packet, response_packet)

    def set_battery_threshold(self, low_level: int, critical_level: int) -> Dict:
        """
        Set low and critical level threshold for device battery.

        :param low_level: low level threshold for device battery.
        :type low_level: int
        :param critical_level: critical level threshold for device battery.
        :type critical_level: int
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.set_battery_threshold(20, 5)
            print(x["payload"]["status"])
            # PMStatus.OK

        """
        request_packet = BatteryThresholdPacket(Application.PM, PMCommand.SET_BAT_THR_REQ)
        request_packet.set_payload("low_level", low_level)
        request_packet.set_payload("critical_level", critical_level)
        response_packet = CommandPacket(Application.PM, PMCommand.SET_BAT_THR_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_ldo() -> List[LDO]:
        """
        List all supported ldo for PM.

        :return: Array of ldo enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_ldo()
            print(x)
            # [<LDO.LDO_FS: ['0x1']>, <LDO.OPTICAL_LDO: ['0x2']>, <LDO.LDO_EPHYZ: ['0x3']>]
        """
        return [TestApplication.LDO_FS, TestApplication.LDO_OPTICAL, TestApplication.LDO_EPHYZ]

    def disable_ldo(self, ldo_id: LDO) -> Dict:
        """
        Disables specified ldo ID.

        :param ldo_id: ldo ID to disable, use get_supported_ldo() to list all supported ldo IDs.
        :type ldo_id: LDO
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_ldo()
            print(x)
            # [<LDO.LDO_FS: ['0x1']>, <LDO.OPTICAL_LDO: ['0x2']>, <LDO.LDO_EPHYZ: ['0x3']>]
            x = application.disable_ldo(application.LDO_OPTICAL)
            print(x["payload"]["ldo_name"], x["payload"]["enabled"])
            # LDO.OPTICAL False

        """
        request_packet = LDOControlPacket(Application.PM, PMCommand.LDO_CONTROL_REQ)
        request_packet.set_payload("ldo_name", ldo_id)
        request_packet.set_payload("enabled", 0)
        response_packet = LDOControlPacket(Application.PM, PMCommand.LDO_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_ldo(self, ldo_id: LDO) -> Dict:
        """
        Enables specified ldo ID.

        :param ldo_id: ldo ID to enable, use get_supported_ldo() to list all supported ldo IDs.
        :type ldo_id: LDO
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_ldo()
            print(x)
            # [<LDO.LDO_FS: ['0x1']>, <LDO.OPTICAL_LDO: ['0x2']>, <LDO.LDO_EPHYZ: ['0x3']>]
            x = application.enable_ldo(application.LDO_OPTICAL)
            print(x["payload"]["ldo_name"], x["payload"]["enabled"])
            # LDO.OPTICAL True

        """
        request_packet = LDOControlPacket(Application.PM, PMCommand.LDO_CONTROL_REQ)
        request_packet.set_payload("ldo_name", ldo_id)
        request_packet.set_payload("enabled", 1)
        response_packet = LDOControlPacket(Application.PM, PMCommand.LDO_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_switches() -> List[ElectrodeSwitch]:
        """
        List all supported switches for PM.

        :return: Array of switches enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_switches()
            print(x)
            # [<ElectrodeSwitch.SWITCH_AD8233: ['0x0']>, ... , <ElectrodeSwitch.SWITCH_ADPD4000: ['0x2']>]
        """
        return [TestApplication.SWITCH_AD8233, TestApplication.SWITCH_AD5940, TestApplication.SWITCH_ADPD4000]

    def enable_electrode_switch(self, switch_name: ElectrodeSwitch) -> Dict:
        """
        Enables specified electrode switch.

        :param switch_name: electrode switch to enable, use get_supported_switches() to list all supported switches.
        :type switch_name: ElectrodeSwitch
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_switches()
            print(x)
            # [<ElectrodeSwitch.AD8233_SWITCH: ['0x0']>, ... , <ElectrodeSwitch.ADPD4000_SWITCH: ['0x2']>]
            x = application.enable_electrode_switch(application.SWITCH_AD5940)
            print(x["payload"]["switch_name"], x["payload"]["enabled"])
            # ElectrodeSwitch.AD5940 True

        """
        request_packet = SwitchControlPacket(Application.PM, PMCommand.SW_CONTROL_REQ)
        request_packet.set_payload("switch_name", switch_name)
        request_packet.set_payload("enabled", 1)
        response_packet = SwitchControlPacket(Application.PM, PMCommand.SW_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_electrode_switch(self, switch_name: ElectrodeSwitch) -> Dict:
        """
        Disables specified electrode switch.

        :param switch_name: electrode switch to disable, use get_supported_switches() to list all supported switches.
        :type switch_name: ElectrodeSwitch
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_switches()
            print(x)
            # [<ElectrodeSwitch.AD8233_SWITCH: ['0x0']>, ... , <ElectrodeSwitch.ADPD4000_SWITCH: ['0x2']>]
            x = application.disable_electrode_switch(application.SWITCH_AD5940)
            print(x["payload"]["switch_name"], x["payload"]["enabled"])
            # ElectrodeSwitch.AD5940 False

        """
        request_packet = SwitchControlPacket(Application.PM, PMCommand.SW_CONTROL_REQ)
        request_packet.set_payload("switch_name", switch_name)
        request_packet.set_payload("enabled", 0)
        response_packet = SwitchControlPacket(Application.PM, PMCommand.SW_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def get_apps_health_status(self) -> Dict:
        """
        Returns ISR count of ad5940, adpd, adxl.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_apps_health_status()
            print(x["payload"]["ad5940_isr_count"], x["payload"]["adpd_isr_count"], x["payload"]["adxl_isr_count"])
            # 0 0 0
        """
        request_packet = CommandPacket(Application.PM, PMCommand.GET_APPS_HEALTH_REQ)
        response_packet = AppsHealthPacket(Application.PM, PMCommand.GET_APPS_HEALTH_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_cap_sense_test(self) -> Dict:
        """
        Disable cap sense test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.disable_cap_sense_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = ControlPacket(Application.PM, PMCommand.CAP_SENSE_TEST_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = ControlPacket(Application.PM, PMCommand.CAP_SENSE_TEST_RES)
        data_packet_id = self._get_packet_id(PMCommand.CAP_SENSE_STREAM_DATA, Application.PM)
        self._packet_manager.unsubscribe(data_packet_id, self._cap_sense_callback_data)
        return self._send_packet(request_packet, response_packet)

    def enable_cap_sense_test(self) -> Dict:
        """
        Enables cap sense test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_cap_sense_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = ControlPacket(Application.PM, PMCommand.CAP_SENSE_TEST_REQ)
        request_packet.set_payload("enabled", 1)
        response_packet = ControlPacket(Application.PM, PMCommand.CAP_SENSE_TEST_RES)
        data_packet_id = self._get_packet_id(PMCommand.CAP_SENSE_STREAM_DATA, Application.PM)
        self._packet_manager.subscribe(data_packet_id, self._cap_sense_callback_data)
        return self._send_packet(request_packet, response_packet)

    def set_cap_sense_callback(self, callback_function: Callable) -> None:
        """
        Sets the callback for the stream data.

        :param callback_function: callback function for stream key test data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 7

            from adi_study_watch import SDK

            def callback(data):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.set_cap_sense_callback(callback)
        """
        self._cap_sense_callback = callback_function

    # noinspection PyUnusedLocal
    def _cap_sense_callback_data(self, packet, packet_id) -> None:
        """
        Callback for data packets.
        """
        if self._cap_sense_callback:
            try:
                response_packet = CapSenseStreamDataPacket()
                response_packet.decode_packet(packet)
                self._cap_sense_callback(response_packet.get_dict())
            except Exception as e:
                logger.error(f"Can't send packet back to user callback function, reason :: {e}", exc_info=True)
        else:
            logger.warning("No callback function provided")

    def ping(self, num_pings: int, packet_size: int) -> List[Dict]:
        """
        Pings the device to send response of specified packet size and specified times (num_pings).

        :param num_pings: number of times packets to be sent from device.
        :type num_pings: int
        :param packet_size: size of the ping packet from device, must be between 15 and 244.
        :type packet_size: int
        :return: list of response packet as dictionary.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.ping(3, 16)
            for packet in x:
                print(packet["payload"]["sequence_num"])
            # 1
            # 2
            # 3

        """
        if not (15 <= packet_size <= 244):
            logger.error("packet_size must be between 15 and 244")
            return []

        request_packet = PingPacket(Application.PM, CommonCommand.PING_REQ)
        request_packet.set_header("length", packet_size)
        request_packet.set_payload("sequence_num", num_pings)
        request_packet.set_payload("data", [0x00] * (packet_size - 11))
        packet_id = self._get_packet_id(CommonCommand.PING_RES, Application.PM)
        queue = self._get_queue(packet_id)
        self._packet_manager.subscribe(packet_id, self._callback_command)
        self._packet_manager.send_packet(request_packet)
        result = []
        for _ in range(num_pings):
            start_time = time.time()
            data = self._get_queue_data(queue)
            response_packet = PingPacket()
            response_packet.decode_packet(data)
            packet_dict = response_packet.get_dict()
            elapsed_time = time.time() - start_time
            packet_dict["payload"]["elapsed_time"] = elapsed_time
            result.append(packet_dict)
        self._packet_manager.unsubscribe(packet_id, self._callback_command)
        return result

    # BIA
    def get_fds_status(self) -> Dict:
        """
        FDS status.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.get_fds_status()
        """
        request_packet = CommandPacket(Application.BIA, BIACommand.FDS_STATUS_REQ)
        response_packet = FDSStatusPacket(Application.BIA, BIACommand.FDS_STATUS_RES)
        return self._send_packet(request_packet, response_packet)

    def read_device_configuration_block_info(self) -> Dict:
        """
        Read Device config block info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.read_device_configuration_block_info()
        """
        request_packet = CommandPacket(Application.BIA, BIACommand.DCB_TIMING_INFO_REQ)
        response_packet = DCBTimingInfoPacket(Application.BIA, BIACommand.DCB_TIMING_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    # FS
    def pattern_write(self, file_size: int, scale_type: int, scale_factor: int, base: int,
                      num_files_to_write: int, display_progress=False) -> List[Dict]:
        """
        Pattern Write.
        16384 0 2 1 2 (linear scale)
        16384 1 2 2 2 (log scale)
        16384 2 2 2 2 (exp scale)

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.pattern_write(16384, 0, 2, 1, 2)
        """
        result = []
        progress_bar = None
        file_count = 0
        if display_progress:
            progress_bar = tqdm(total=num_files_to_write)
        while file_count < num_files_to_write:
            request_packet = PatternWritePacket(Application.FS, FSCommand.PATTERN_WRITE_REQ)
            request_packet.set_payload("file_size", file_size)
            request_packet.set_payload("scale_type", scale_type)
            request_packet.set_payload("scale_factor", scale_factor)
            request_packet.set_payload("num_files_to_write", num_files_to_write)
            response_packet = PatternWritePacket(Application.FS, FSCommand.PATTERN_WRITE_RES)
            response_packet = self._send_packet(request_packet, response_packet)
            result.append(response_packet)
            if response_packet["payload"]["status"] == CommonStatus.OK:
                if scale_type == 0:
                    file_size *= scale_factor
                elif scale_type == 1 and not scale_factor == 1:
                    file_size *= int(math.log(base, scale_factor))
                elif scale_type == 2:
                    file_size *= int(math.exp(scale_factor))
            else:
                if response_packet["payload"]["status"] == FSStatus.ERR_MEMORY_FULL:
                    logger.error("Memory full breaking loop as new files cannot be written!")
                    break
                elif response_packet["payload"]["status"] == FSStatus.ERR_MAX_FILE_COUNT:
                    logger.error("Max file count crossed!")
                    break
            file_count += 1
            if display_progress:
                progress_bar.update(1)
        if display_progress:
            progress_bar.close()
        return result

    def fs_log_test(self) -> Dict:
        """
        Log test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.fs_log_test()
        """
        request_packet = CommandPacket(Application.FS, FSCommand.TEST_LOG_REQ)
        response_packet = CommandPacket(Application.FS, FSCommand.TEST_LOG_RES)
        return self._send_packet(request_packet, response_packet)

    def get_debug_info(self) -> Dict:
        """
        Returns debug info of FS.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_debug_info()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = CommandPacket(Application.FS, FSCommand.GET_DEBUG_INFO_REQ)
        response_packet = DebugInfoPacket(Application.FS, FSCommand.GET_DEBUG_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    def get_bad_blocks(self) -> Dict:
        """
        Returns a packet containing number of bad blocks in the file system.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_bad_blocks()
            print(x["payload"]["bad_blocks"])
            # 0
        """
        request_packet = CommandPacket(Application.FS, FSCommand.GET_BAD_BLOCKS_REQ)
        response_packet = BadBlockPacket(Application.FS, FSCommand.GET_BAD_BLOCKS_RES)
        return self._send_packet(request_packet, response_packet)

    def get_stream_debug_info(self, stream: Stream) -> Dict:
        """
        Returns specified stream debug info of FS.

        :param stream: stream to obtain debug info, use get_supported_streams() to list all supported streams.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.SQI: ['0xC8', '0x0D']>]
            x = application.get_stream_debug_info(application.STREAM_ADXL)
            print(x["payload"]["stream_address"], x["payload"]["packets_received"], x["payload"]["packets_missed"])
            # Stream.ADXL 0 0
        """
        request_packet = StreamPacket(Application.FS, FSCommand.STREAM_DEBUG_INFO_REQ)
        request_packet.set_payload("stream_address", stream)
        response_packet = StreamDebugInfoPacket(Application.FS, FSCommand.STREAM_DEBUG_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    def get_file_info(self, file_index: int) -> Dict:
        """
        File info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_file_info(4)

        """
        request_packet = FileInfoRequestPacket(Application.FS, FSCommand.GET_FILE_INFO_REQ)
        request_packet.set_payload("file_index", file_index)
        response_packet = FileInfoResponsePacket(Application.FS, FSCommand.GET_FILE_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    def file_read_test(self, filename: str) -> Optional[dict]:
        """
        File read test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.file_read_test("03124671.LOG")

        """
        fs_app = FSApplication(self._packet_manager)
        files = fs_app.ls()
        file_index = 0
        file_found = False
        for file in files:
            if not file_found:
                file_index += 1
            if file["payload"]["filename"] == filename:
                file_found = True
        if not file_found:
            logger.error(f"{filename} is not present on the device, use ls() to list all the files.")
            return None
        response_packet = self.get_file_info(file_index)
        return response_packet

    def page_read_test(self, page_num: int, num_bytes: int) -> Dict:
        """
        Page read test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.page_read_test(300, 20)

        """
        request_packet = PageInfoRequestPacket(Application.FS, FSCommand.PAGE_READ_TEST_REQ)
        request_packet.set_payload("page_num", page_num)
        request_packet.set_payload("num_bytes", num_bytes)
        response_packet = PageInfoResponsePacket(Application.FS, FSCommand.PAGE_READ_TEST_RES)
        return self._send_packet(request_packet, response_packet)

    # Display
    @staticmethod
    def get_supported_display_colors() -> List[DisplayColor]:
        """
        List all supported Display colors for Display Application.

        :return: Array of Display color enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_display_colors()
            print(x)
            # [<DisplayColor.WHITE: ['0x0']>, <DisplayColor.BLACK: ['0x1']>, ... , <DisplayColor.BLUE: ['0x4']>]
        """
        return [TestApplication.WHITE, TestApplication.BLACK, TestApplication.RED, TestApplication.GREEN,
                TestApplication.BLUE]

    def disable_back_light(self) -> Dict:
        """
        Disables the back light of the watch.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.disable_back_light()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.BACKLIGHT_CONTROL_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.BACKLIGHT_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_key_press_test(self) -> Dict:
        """"
        Disables and unsubscribe to key press test data.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_key_press_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.KEY_TEST_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.KEY_TEST_RES)
        data_packet_id = self._get_packet_id(DisplayCommand.KEY_STREAM_DATA, Application.DISPLAY)
        self._packet_manager.unsubscribe(data_packet_id, self._key_press_callback_data)
        return self._send_packet(request_packet, response_packet)

    def enable_key_press_test(self) -> Dict:
        """"
        Enables and subscribe to key press test data.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_key_press_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.KEY_TEST_REQ)
        request_packet.set_payload("enabled", 1)
        response_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.KEY_TEST_RES)
        data_packet_id = self._get_packet_id(DisplayCommand.KEY_STREAM_DATA, Application.DISPLAY)
        self._packet_manager.subscribe(data_packet_id, self._key_press_callback_data)
        return self._send_packet(request_packet, response_packet)

    def enable_back_light(self) -> Dict:
        """"
        Enables the back light of the watch.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_back_light()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.BACKLIGHT_CONTROL_REQ)
        request_packet.set_payload("enabled", 1)
        response_packet = EnableDisplayPacket(Application.DISPLAY, DisplayCommand.BACKLIGHT_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def set_display_color(self, color: DisplayColor) -> Dict:
        """
        Set the specified color to watch screen, to check for pixel damage.

        :param color: color to set on watch screen, use get_supported_display_colors() to list all supported colors.
        :type color: DisplayColor
        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_display_colors()
            print(x)
            # [<DisplayColor.WHITE: ['0x0']>, <DisplayColor.BLACK: ['0x1']>, ... , <DisplayColor.BLUE: ['0x4']>]
            x = application.set_display_color(application.BLUE)
            print(x["payload"]["color"])
            # DisplayColor.BLUE
        """
        request_packet = SetDisplayPacket(Application.DISPLAY, DisplayCommand.SET_DISPLAY_REQ)
        request_packet.set_payload("color", color)
        response_packet = SetDisplayPacket(Application.DISPLAY, DisplayCommand.SET_DISPLAY_RES)
        return self._send_packet(request_packet, response_packet)

    # noinspection PyUnusedLocal
    def _key_press_callback_data(self, packet, packet_id) -> None:
        """
        Callback for key test
        """
        if self._key_press_callback:
            try:
                response_packet = KeyStreamDataPacket()
                response_packet.decode_packet(packet)
                self._key_press_callback(response_packet.get_dict())
            except Exception as e:
                logger.error(f"Can't send packet back to user callback function, reason :: {e}", exc_info=True)
        else:
            logger.warning("No callback function provided.")

    def set_key_press_callback(self, callback_function: Callable) -> None:
        """
        Sets the callback for the stream data.

        :param callback_function: callback function for stream key test data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 7

            from adi_study_watch import SDK

            def callback(data):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.set_callback(callback)

        """
        self._key_press_callback = callback_function

    # ADPD
    @staticmethod
    def get_supported_led_ids() -> List[ADPDLed]:
        """
        List all supported led IDs for ADPD.

        :return: Array of Led ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_MWL: ['0x0']>, <ADPDLed.LED_GREEN: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x4']>]
        """
        return [TestApplication.LED_MWL, TestApplication.LED_GREEN, TestApplication.LED_RED, TestApplication.LED_IR,
                TestApplication.LED_BLUE]

    def get_agc_info(self, led_index: ADPDLed) -> Dict:
        """
        Returns AGC info of specified led index.

        :param led_index: led_index to obtain info, use get_supported_led_ids() to list all supported led ID.
        :type led_index: ADPDLed
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x0']>, <ADPDLed.LED_RED: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x3']>]
            x = application.get_agc_info(application.LED_GREEN)
            print(x["payload"]["led_index"])
            # ADPDLed.LED_GREEN
            print(x["payload"]["ch1"])
            # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            print(x["payload"]["ch2"])
            # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            print(x["payload"]["dc0_led_current"])
            # 0
            print(x["payload"]["tia_ch1"])
            # 0
            print(x["payload"]["tia_ch2"])
            # 0
        """
        request_packet = AgcInfoPacket(Application.ADPD, ADPDCommand.AGC_INFO_REQ)
        request_packet.set_payload("led_index", led_index)
        response_packet = AgcInfoPacket(Application.ADPD, ADPDCommand.AGC_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    def test_command1(self, data: int) -> Dict:
        """
        ADPD test command.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.test_command1()

        """
        request_packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST1_REQ)
        data = [data] + [0] * 11
        request_packet.set_payload("data", data)
        response_packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST1_RES)
        return self._send_packet(request_packet, response_packet)

    def test_command2(self, data: int) -> Dict:
        """
        ADPD test command.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.test_command2()

        """
        request_packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST2_REQ)
        data = [data] + [0] * 11
        request_packet.set_payload("data", data)
        response_packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST2_RES)
        return self._send_packet(request_packet, response_packet)

    def test_command3(self, data: int) -> Dict:
        """
        ADPD test command.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.test_command3()

        """
        request_packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST3_REQ)
        data = [data] + [0] * 11
        request_packet.set_payload("data", data)
        response_packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST3_RES)
        return self._send_packet(request_packet, response_packet)

    # PPG
    def get_ppg_states(self) -> Dict:
        """
        Get PPG states.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_states()
            print(x["payload"]["states"])
            # [0,0,0, ... ,0,0]

        """
        request_packet = CommandPacket(Application.PPG, PPGCommand.GET_LAST_STATES_REQ)
        response_packet = PPGStatesPacket(Application.PPG, PPGCommand.GET_LAST_STATES_RES)
        return self._send_packet(request_packet, response_packet)

    # ADXL
    def adxl_self_test(self) -> Dict:
        """
        ADXL self test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.adxl_self_test()

        """
        request_packet = CommandPacket(Application.ADXL, ADXLCommand.SELF_TEST_REQ)
        response_packet = CommandPacket(Application.ADXL, ADXLCommand.SELF_TEST_RES)
        return self._send_packet(request_packet, response_packet)
