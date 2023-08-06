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
from typing import Dict, List

from ..core.enums.fs_enums import FSCommand
from ..core.enums.dcb_enums import DCBCommand
from .common_application import CommonApplication
from ..core.packets.command_packet import CommandPacket
from ..core.enums.low_touch_enum import LTCommand, CommandType
from ..core.enums.common_enums import Application, CommonCommand
from ..core.packets.low_touch_packets import ReadCH2CapPacket, CommandLogPacket, LTLibraryConfigPacket, LTDCBPacket, \
    LTDCBCommandPacket


class LowTouchApplication(CommonApplication):
    """
    FS Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_low_touch_application()
    """

    START_COMMAND = CommandType.START
    STOP_COMMAND = CommandType.STOP

    def __init__(self, packet_manager):
        super().__init__(Application.LT_APP, packet_manager)
        self._dcb_size = 57
        self._log_command = None

    def read_ch2_cap(self) -> Dict:
        """
        Read the AD7156 CH2 Capacitance in uF.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.read_ch2_cap()
            print(x["payload"]["cap_value"])
            # 0
        """
        request_packet = ReadCH2CapPacket(self._destination, LTCommand.READ_CH2_CAP_REQ)
        response_packet = ReadCH2CapPacket(self._destination, LTCommand.READ_CH2_CAP_RES)
        return self._send_packet(request_packet, response_packet)

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
             - 0x04

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.write_library_configuration([[0x00, 0x1]])
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        request_packet = LTLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        request_packet.set_payload("size", len(fields_values))
        request_packet.set_payload("data", fields_values)
        response_packet = LTLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

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
             - 0x04

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x0']]
        """
        data = [[field, 0] for field in fields]
        request_packet = LTLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_REQ)
        request_packet.set_payload("size", len(data))
        request_packet.set_payload("data", data)
        response_packet = LTLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def read_device_configuration_block(self, readable_format=False) -> [Dict]:
        """
        Returns entire device configuration block.

        :param readable_format: Converts binary result into readable commands.
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["data"])
        """
        request_packet = LTDCBCommandPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        response_packet = LTDCBPacket(self._destination, DCBCommand.READ_CONFIG_RES)
        result = self._send_packet_multi_response(request_packet, response_packet)

        if readable_format:
            raw_data = []
            total_size = 0
            for packet in result:
                total_size += packet["payload"]["size"]
                raw_data += packet["payload"]["data"][:packet["payload"]["size"] * 4]

            dcb_readable_format = []
            data_read = 0
            start_cmd_count = 0
            stop_cmd_count = 0
            if len(raw_data) > 0:
                raw_data[0:2], raw_data[2:4] = raw_data[2:4], raw_data[0:2]
                log_packet = CommandLogPacket()
                log_packet.decode_packet(raw_data)
                log_packet = log_packet.get_dict()
                raw_data = log_packet["payload"]["commands"]
                start_cmd_count = log_packet["payload"]["start_cmd_count"]
                stop_cmd_count = log_packet["payload"]["stop_cmd_count"]

                while data_read < len(raw_data):
                    pkt = raw_data[data_read:data_read + 8]
                    if not len(pkt) == 8:
                        break
                    length = (int(pkt[4]) << 8) + int(pkt[5])
                    pkt = raw_data[data_read:data_read + length]
                    pkt[0:2], pkt[2:4] = pkt[2:4], pkt[0:2]
                    packet = CommandPacket()
                    packet.decode_packet(pkt)
                    packet = packet.get_dict()
                    dcb_readable_format.append({
                        "application": packet["header"]["source"],
                        "command": packet["payload"]["command"]
                    })
                    data_read += length
            result = result[0]
            result["payload"]["size"] = total_size
            result["payload"]["data"] = dcb_readable_format
            result["payload"]["start_command_count"] = start_cmd_count
            result["payload"]["stop_command_count"] = stop_cmd_count
        return result

    def _write_device_configuration_block(self, commands) -> [Dict]:
        dcb_size = (self._dcb_size * 4)
        packets = math.ceil(len(commands) / dcb_size)
        if packets > 18:
            raise Exception("Can't write more than 18 packets. Size limit 4104 bytes.")
        result = []
        for packet in range(packets):
            temp_command = commands[packet * dcb_size:(packet + 1) * dcb_size]
            request_packet = LTDCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
            request_packet.set_payload("size", len(temp_command) // 4)
            request_packet.set_payload("packet_count", packets)
            request_packet.set_payload("data", temp_command)
            response_packet = LTDCBCommandPacket(self._destination, DCBCommand.WRITE_CONFIG_RES)
            result.append(self._send_packet(request_packet, response_packet))
        return result

    def write_device_configuration_block_from_file(self, filename: str) -> [Dict]:
        """
        Writes the device configuration block values from specified binary file.

        :param filename: binary filename
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.write_device_configuration_block_from_file("lt_dcb.dcb")
        """
        with open(filename, 'rb') as file:
            data = file.readlines()
            result = []
            for value in data:
                result += value
            return self._write_device_configuration_block(result)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes ADPD Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.delete_device_configuration_block()
        """
        request_packet = LTDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        response_packet = LTDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_command_logging(self, command_type: CommandType) -> None:
        """
        Starts recording SDK commands to a file.

        :param command_type: Start or Stop command recording.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.enable_command_logging(application.START)
        """
        if command_type == CommandType.START:
            self._log_command = CommandLogPacket(Application.FS, command=FSCommand.LOG_USER_CONFIG_DATA_REQ)
            self._packet_manager.subscribe_command_logger(self._log_command)
        self._packet_manager.enable_command_logging(command_type)

    def disable_command_logging(self, command_type: CommandType, filename="commands.LOG", word_align=False) -> None:
        """
        Stops recording SDK commands to a file.

        :param command_type: Start or Stop command recording.
        :param filename: Name of the file to store commands.
        :param word_align: Word align has to be true for generating LT app DCB, for User config file (FS) word align
        needs to be false.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.disable_command_logging(application.START)
        """
        self._packet_manager.disable_command_logging(command_type)
        if command_type == CommandType.STOP:
            self._packet_manager.unsubscribe_command_logger()
            self._generate_log_file(filename, word_align)

    def _generate_log_file(self, filename, word_align):
        self._log_command.set_header("source", self._packet_manager.source)

        with open(filename, 'wb') as file:
            commands = bytearray(self._log_command.to_list())
            if word_align:
                remaining = len(commands) % 4
                if remaining:
                    commands += b'\0' * (4 - remaining)
            file.write(commands)
