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

import time
import logging
from datetime import datetime
from typing import Dict, List, Callable, Tuple

from ..core import utils
from .csv_logging import CSVLogger
from ..core.enums.dcb_enums import DCBCommand
from .common_application import CommonApplication
from ..core.enums.pm_enums import PMCommand, ChipID
from ..core.packets.command_packet import CommandPacket
from ..core.packets.common_packets import VersionPacket, StreamPacket
from ..core.enums.common_enums import Application, CommonCommand, Stream
from ..core.packets.pm_packets import MCUVersionPacket, SystemInfoPacket, DateTimePacket, UICRCustomerRegistersPacket, \
    PMDCBCommandPacket, TopTouchControlPacket
from ..core.packets.pm_packets import MCUVersionPacket, SystemInfoPacket, DateTimePacket, SyncTimerPacket
from ..core.packets.pm_packets import BatteryInfoPacket, DCBStatusPacket, ChipIDPacket, PMDCBPacket, \
    PMRegisterReadPacket, PMRegisterWritePacket

logger = logging.getLogger(__name__)


class PMApplication(CommonApplication):
    """
    PM Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_pm_application()
    """

    CHIP_ADPD4K = ChipID.ADPD4K
    CHIP_AD5940 = ChipID.AD5940
    CHIP_AD7156 = ChipID.AD7156
    CHIP_ADXL362 = ChipID.ADXL362
    CHIP_ADP5360 = ChipID.ADP5360
    CHIP_NAND_FLASH = ChipID.NAND_FLASH

    STREAM_BATTERY = Stream.BATTERY

    def __init__(self, packet_manager):
        super().__init__(Application.PM, packet_manager)
        self._args = {}
        self._csv_logger = {}
        self._last_timestamp = {}
        self._callback_function = {}
        self._dcb_size = 57

    def device_configuration_block_status(self) -> Dict:
        """
        Display dcb status of all applications.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.device_configuration_block_status()
            print(x["payload"]["adxl_block"], x["payload"]["adpd4000_block"], x["payload"]["ppg_block"])
            # 0 0 0
        """
        request_packet = CommandPacket(self._destination, DCBCommand.QUERY_STATUS_REQ)
        response_packet = DCBStatusPacket(self._destination, DCBCommand.QUERY_STATUS_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_touch_sensor(self) -> Dict:
        """
        Disables touch sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.disable_touch_sensor()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        request_packet = CommandPacket(self._destination, PMCommand.DEACTIVATE_TOUCH_SENSOR_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.DEACTIVATE_TOUCH_SENSOR_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_touch_sensor(self) -> Dict:
        """
        Enables touch sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.enable_touch_sensor()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        request_packet = CommandPacket(self._destination, PMCommand.ACTIVATE_TOUCH_SENSOR_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.ACTIVATE_TOUCH_SENSOR_RES)
        return self._send_packet(request_packet, response_packet)

    def enter_boot_loader_mode(self) -> Dict:
        """
        Sets the device to boot loader mode.

        :return: A empty dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.enter_boot_loader_mode()
        """
        request_packet = CommandPacket(self._destination, PMCommand.ENTER_BOOTLOADER_REQ)
        return self._send_packet_no_response(request_packet)

    def get_battery_info(self) -> Dict:
        """
        Returns device current battery information.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_battery_info()
            print(x["payload"]["battery_status"], x["payload"]["battery_level"])
            # BatteryStatus.COMPLETE 100
        """
        request_packet = CommandPacket(self._destination, PMCommand.GET_BAT_INFO_REQ)
        response_packet = BatteryInfoPacket(self._destination, PMCommand.GET_BAT_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    def get_chip_id(self, chip_name: ChipID) -> Dict:
        """
        Returns chip id for specified chip name.

        :param chip_name: get chip id of the chip_name, use get_supported_chips() to list all support chip names.
        :type chip_name: ChipID
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_supported_chips()
            print(x)
            # [<ChipID.CHIP_ADXL362: ['0x1']>, ... , <ChipID.CHIP_AD7156: ['0x6']>]
            x = application.get_chip_id(application.CHIP_ADPD4K)
            print(x["payload"]["chip_name"], x["payload"]["chip_id"])
            # ChipID.ADPD4K 192
        """
        request_packet = ChipIDPacket(self._destination, PMCommand.CHIP_ID_REQ)
        request_packet.set_payload("chip_name", chip_name)
        response_packet = ChipIDPacket(self._destination, PMCommand.CHIP_ID_RES)
        return self._send_packet(request_packet, response_packet)

    def get_datetime(self) -> Dict:
        """
        Returns device current datetime.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_datetime()
            print(f"{x['payload']['year']}-{x['payload']['month']}-{x['payload']['day']}")
            # 2020-12-16
            print(f"{x['payload']['hour']}:{x['payload']['minute']}:{x['payload']['second']}")
            # 15:17:57
        """
        request_packet = CommandPacket(self._destination, PMCommand.GET_DATE_TIME_REQ)
        response_packet = DateTimePacket(self._destination, PMCommand.GET_DATE_TIME_RES)
        return self._send_packet(request_packet, response_packet)

    def get_low_touch_status(self) -> Dict:
        """
        Returns low touch status.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_low_touch_status()
            print(x["payload"]["status"])
            # PMStatus.LOW_TOUCH_LOGGING_NOT_STARTED
        """
        request_packet = CommandPacket(self._destination, PMCommand.GET_LOW_TOUCH_LOGGING_STATUS_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.GET_LOW_TOUCH_LOGGING_STATUS_RES)
        return self._send_packet(request_packet, response_packet)

    def get_mcu_version(self) -> Dict:
        """
        Returns Device MCU version.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_mcu_version()
            print(x["payload"]["mcu"])
            # MCUType.MCU_M4
        """
        request_packet = CommandPacket(self._destination, PMCommand.GET_MCU_VERSION_REQ)
        response_packet = MCUVersionPacket(self._destination, PMCommand.GET_MCU_VERSION_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_chips() -> List[ChipID]:
        """
        List all supported chips for PM.

        :return: Array of chips enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_supported_chips()
            print(x)
            # [<ChipID.CHIP_ADXL362: ['0x1']>, ... , <ChipID.CHIP_AD7156: ['0x6']>]
        """
        return [PMApplication.CHIP_ADXL362, PMApplication.CHIP_ADPD4K, PMApplication.CHIP_ADP5360,
                PMApplication.CHIP_AD5940, PMApplication.CHIP_NAND_FLASH, PMApplication.CHIP_AD7156]

    def get_system_info(self) -> Dict:
        """
        Returns Device system info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_system_info()
            print(x["payload"]["version"])
            # 0
            print(x["payload"]["mac_address"])
            # C5-05-CA-F1-67-D5
            print(x["payload"]["device_id"])
            # 0
        """
        request_packet = CommandPacket(self._destination, PMCommand.SYS_INFO_REQ)
        response_packet = SystemInfoPacket(self._destination, PMCommand.SYS_INFO_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_battery_charging(self) -> Dict:
        """
        Enable battery charging.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.enable_battery_charging()
        """
        request_packet = CommandPacket(self._destination, PMCommand.ENABLE_BAT_CHARGE_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.ENABLE_BAT_CHARGE_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_battery_charging(self) -> Dict:
        """
        Disable battery charging.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.disable_battery_charging()
        """
        request_packet = CommandPacket(self._destination, PMCommand.DISABLE_BAT_CHARGE_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.DISABLE_BAT_CHARGE_RES)
        return self._send_packet(request_packet, response_packet)

    def get_version(self) -> Dict:
        """
        Returns Device version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_version()
            print(x["payload"]["major_version"])
            # 1
            print(x["payload"]["minor_version"])
            # 0
            print(x["payload"]["patch_version"])
            # 1
            print(x["payload"]["version_string"])
            # -Perseus
            print(x["payload"]["build_version"])
            # |298b4ce1_Rl|2020-12-14 12:34:31 -0500
        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        response_packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_RES)
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
           * - 0x00
             - 0x36

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.read_register([0x15, 0x20, 0x2E])
            print(x["payload"]["data"])
            # [['0x15', '0x0'], ['0x20', '0x0'], ['0x2E', '0x0']]

        """
        data = [[address, 0] for address in addresses]
        request_packet = PMRegisterReadPacket(self._destination, CommonCommand.REGISTER_READ_REQ)
        request_packet.set_payload("size", len(data))
        request_packet.set_payload("data", data)
        response_packet = PMRegisterReadPacket(self._destination, CommonCommand.REGISTER_READ_RES)
        return self._send_packet(request_packet, response_packet)

    def set_datetime(self, date_time: datetime) -> Dict:
        """
        Set specified datetime to device.

        :param date_time: datetime for device.
        :type date_time: datetime
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK
            import datetime

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            now = datetime.datetime.now()
            x = application.set_datetime(now)
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset = - (time.altzone if is_dst else time.timezone)
        request_packet = DateTimePacket(self._destination, PMCommand.SET_DATE_TIME_REQ)
        request_packet.set_payload("year", date_time.year)
        request_packet.set_payload("month", date_time.month)
        request_packet.set_payload("day", date_time.day)
        request_packet.set_payload("hour", date_time.hour)
        request_packet.set_payload("minute", date_time.minute)
        request_packet.set_payload("second", date_time.second)
        request_packet.set_payload("tz_sec", utc_offset)
        response_packet = CommandPacket(self._destination, PMCommand.SET_DATE_TIME_RES)
        return self._send_packet(request_packet, response_packet)

    def system_hardware_reset(self) -> Dict:
        """
        Reset device hardware.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.system_hardware_reset()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        request_packet = CommandPacket(self._destination, PMCommand.SYSTEM_HW_RESET_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.SYSTEM_HW_RESET_RES)
        return self._send_packet(request_packet, response_packet)

    def system_reset(self) -> Dict:
        """
        Reset device system.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.system_reset()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        request_packet = CommandPacket(self._destination, PMCommand.SYSTEM_RESET_REQ)
        response_packet = CommandPacket(self._destination, PMCommand.SYSTEM_RESET_RES)
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
           :widths: 75
           :header-rows: 1

           * - Address ranges
           * - [0x2-0x7], [0xA-0xE], [0x11-0x22], [0x27-0x2E], [0x30-0x33], [0x36]


        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
            print(x["payload"]["data"])
            # [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']]
        """
        size = len(addresses_values)
        for i in range(size):
            if not (0x2 <= addresses_values[i][0] <= 0x7 or 0xA <= addresses_values[i][0] <= 0xE or
                    0x11 <= addresses_values[i][0] <= 0x22 or 0x27 <= addresses_values[i][0] <= 0x2E or
                    0x30 <= addresses_values[i][0] <= 0x33 or addresses_values[i][0] == 0x36):
                logger.warning(f"{'0x%X' % addresses_values[i][0]} is out of range, allowed ranges are: [0x2-0x7], "
                               f"[0xA-0xE], [0x11-0x22], [0x27-0x2E], [0x30-0x33], [0x36]")
        request_packet = PMRegisterWritePacket(self._destination, CommonCommand.REGISTER_WRITE_REQ)
        request_packet.set_payload("size", size)
        request_packet.set_payload("data", addresses_values)
        response_packet = PMRegisterWritePacket(self._destination, CommonCommand.REGISTER_WRITE_RES)
        return self._send_packet(request_packet, response_packet)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes PM Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.delete_device_configuration_block()
        """
        request_packet = PMDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        response_packet = PMDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["dcb_data"])
            # []
        """
        request_packet = PMDCBCommandPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        response_packet = PMDCBPacket(self._destination, DCBCommand.READ_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def write_device_configuration_block(self, addresses_values: List[List[int]]) -> Dict:
        """
        Writes the device configuration block values of specified addresses.
        This function takes a list of addresses and values to write, and returns a response packet as
        dictionary containing addresses and values.

        :param addresses_values: List of addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.write_device_configuration_block([[0x2, 2], [0x1, 0x1]])
            print(x["payload"]["size"])
            # 2
        """
        request_packet = PMDCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        request_packet.set_payload("size", len(addresses_values))
        request_packet.set_payload("data", addresses_values)
        response_packet = PMDCBCommandPacket(self._destination, DCBCommand.WRITE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def write_device_configuration_block_from_file(self, filename: str) -> Dict:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.write_device_configuration_block_from_file("pm_dcb.dcfg")
        """
        result = self.device_configuration_file_to_list(filename)
        if result:
            return self.write_device_configuration_block(result)

    # noinspection PyTypeChecker
    def set_callback(self, callback_function: Callable, args: Tuple = (), stream: Stream = STREAM_BATTERY) -> None:
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
            application = sdk.get_pm_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2))
        """
        self._callback_function[stream] = callback_function
        self._args[stream] = args

    def _callback_data(self, packet, packet_id, callback_function=None, args=None, stream=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, BatteryInfoPacket(), self.STREAM_BATTERY)

    def _callback_data_helper(self, packet, response_packet, stream=None):
        """
        Process and returns the data back to user's callback function.
        """
        args = self._args.get(stream, ())
        callback_function = self._callback_function.get(stream, None)
        response_packet.decode_packet(packet)
        last_timestamp = self._last_timestamp.get(stream)
        first_timestamp = last_timestamp[0]
        result = response_packet.get_dict(last_timestamp)
        utils.update_timestamp(result, last_timestamp)
        csv_logger = self._csv_logger.get(stream, None)
        if csv_logger:
            csv_logger.add_row(result, first_timestamp)
        try:
            if callback_function:
                callback_function(result, *args)
        except Exception as e:
            logger.error(f"Can't send packet back to user callback function, reason :: {e}", exc_info=True)

        if not csv_logger and not callback_function:
            logger.warning(f"No callback function provided for {result['header']['source']}")

    def subscribe_stream(self, stream=STREAM_BATTERY):
        """
        Subscribe to the stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        request_packet = StreamPacket(self._destination, CommonCommand.SUBSCRIBE_STREAM_REQ)
        request_packet.set_payload("stream_address", stream)
        self._subscribe_stream_data(stream)
        response_packet = StreamPacket(self._destination, CommonCommand.SUBSCRIBE_STREAM_RES)
        self._update_timestamp(datetime.now(), stream)
        return self._send_packet(request_packet, response_packet)

    def _update_timestamp(self, date_time, stream=STREAM_BATTERY, generate_ts=False):
        if generate_ts:
            ts = (32000.0 * ((date_time.hour * 3600) + (date_time.minute * 60) + date_time.second))
        else:
            ts = -1
        self._last_timestamp[stream] = [date_time.timestamp(), ts]

    def unsubscribe_stream(self, stream=None):
        """
        Unsubscribe the stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        request_packet = StreamPacket(self._destination, CommonCommand.UNSUBSCRIBE_STREAM_REQ)
        request_packet.set_payload("stream_address", stream)
        response_packet = StreamPacket(self._destination, CommonCommand.UNSUBSCRIBE_STREAM_RES)
        response_packet = self._send_packet(request_packet, response_packet)
        self._unsubscribe_stream_data(stream)
        return response_packet

    def _subscribe_stream_data(self, stream=None, callback_function=None):
        callback_function = callback_function if callback_function else self._callback_data
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, stream)
        self._packet_manager.subscribe(data_packet_id, callback_function)

    def _unsubscribe_stream_data(self, stream=None, callback_function=None):
        callback_function = callback_function if callback_function else self._callback_data
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, stream)
        self._packet_manager.unsubscribe(data_packet_id, callback_function)

    def enable_csv_logging(self, filename, header=None) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.enable_csv_logging("adp.csv")
        """
        if header is None:
            header = ["Timestamp", "Battery status", "Battery level", "Battery mv"]
        self._csv_logger[Stream.BATTERY] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger.get(Stream.BATTERY):
            self._csv_logger[Stream.BATTERY].stop_logging()
        self._csv_logger[Stream.BATTERY] = None

    def read_uicr_customer_registers(self) -> Dict:
        """
        Read UICR customer Register.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            packet = application.read_uicr_customer_registers()

        """
        request_packet = UICRCustomerRegistersPacket(self._destination, PMCommand.READ_UICR_CUSTOMER_REG_REQ)
        response_packet = UICRCustomerRegistersPacket(self._destination, PMCommand.READ_UICR_CUSTOMER_REG_RES)
        return self._send_packet(request_packet, response_packet)

    def write_uicr_customer_registers(self, hw_revision=None, manufacture_date=None) -> Dict:
        """
        Writes to UICR customer Register.
        This API can only be used after NOR flash is erased, the following command can be used to do so:
        $nrfjprog --eraseall

        The following information is written to UICR. Hardcoded information:
            manufacturer_name "ADI",
            model_number "EVAL-HCRWATCH4Z
            hw_revision "4.3.00"
            serial_number 12 bytes BLE MAC address
            manufacture_date is current system date manufacture_date This is optional.

        :param manufacture_date: manufacture date size limit 12. default = current system date(YYYY-MM-DD).
        :param hw_revision: hw revision size limit 8. default = 4.3.00.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            packet = application.write_uicr_customer_registers("2022-02-15")

        """
        mac_address = self.get_system_info()["payload"]["mac_address"]
        now = datetime.now()
        date = str(now.year) + "-" + str('%02d' % now.month) + "-" + str('%02d' % now.day)
        if manufacture_date is None:
            manufacture_date = date
        if hw_revision is None:
            hw_revision = "4.3.00"
        request_packet = UICRCustomerRegistersPacket(self._destination, PMCommand.WRITE_UICR_CUSTOMER_REG_REQ)
        request_packet.set_payload("manufacturer_name", "ADI")
        request_packet.set_payload("model_number", "EVAL-HCRWATCH4Z")
        request_packet.set_payload("hw_revision", hw_revision)
        request_packet.set_payload("serial_number", mac_address.replace("-", ""))
        request_packet.set_payload("manufacture_date", manufacture_date)
        request_packet.set_payload("crc_8", 0)
        response_packet = UICRCustomerRegistersPacket(self._destination, PMCommand.WRITE_UICR_CUSTOMER_REG_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_sync_timer(self):
        """
        Enables Sync Timer

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.enable_sync_timer()
        """
        request_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_ENABLE_REQ)
        request_packet.set_payload("enabled", 1)
        response_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_ENABLE_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_sync_timer(self):
        """
        Disable Sync Timer

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.disable_sync_timer()
        """
        request_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_ENABLE_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_ENABLE_RES)
        return self._send_packet(request_packet, response_packet)

    def start_sync_timer(self):
        """
        Starts Sync Timer

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.start_sync_timer()
        """
        request_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_START_STOP_REQ)
        request_packet.set_payload("enabled", 1)
        response_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_START_STOP_RES)
        return self._send_packet(request_packet, response_packet)

    def stop_sync_timer(self):
        """
        Stops Sync Timer

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.enable_sync_timer()
        """
        request_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_START_STOP_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = SyncTimerPacket(self._destination, PMCommand.SYNC_TIMER_START_STOP_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_top_touch(self):
        """
        This API is used to enable top touch application(backlight control) in Fw.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.enable_top_touch()
        """
        request_packet = TopTouchControlPacket(self._destination, PMCommand.SET_TOP_TOUCH_CONTROL_REQ)
        request_packet.set_payload("enabled", 1)
        response_packet = TopTouchControlPacket(self._destination, PMCommand.SET_TOP_TOUCH_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def disable_top_touch(self):
        """
        This API is used to disable top touch application(backlight control) in Fw.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.disable_top_touch()
        """
        request_packet = TopTouchControlPacket(self._destination, PMCommand.SET_TOP_TOUCH_CONTROL_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = TopTouchControlPacket(self._destination, PMCommand.SET_TOP_TOUCH_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)

    def get_top_touch_status(self):
        """
        This API is used to get the status of top touch application(backlight control) in Fw,
         whether it is enabled or disabled

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.get_top_touch_status()
        """
        request_packet = TopTouchControlPacket(self._destination, PMCommand.GET_TOP_TOUCH_CONTROL_REQ)
        request_packet.set_payload("enabled", 0)
        response_packet = TopTouchControlPacket(self._destination, PMCommand.GET_TOP_TOUCH_CONTROL_RES)
        return self._send_packet(request_packet, response_packet)
