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
import re
import math
import logging
from typing import List, Dict, Callable, Tuple

from ..core import utils
from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.packets.command_packet import CommandPacket
from ..core.packets.common_packets import StreamStatusPacket
from ..core.packets.stream_data_packets import TemperatureDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.temperature_packets import TemperatureDCFGPacket, TemperatureDCBPacket, \
    TemperatureLibraryConfigPacket, TemperatureDCBCommandPacket

logger = logging.getLogger(__name__)


class TemperatureApplication(CommonStream):
    """
    Temperature Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_temperature_application()

    """

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

    def __init__(self, packet_manager):
        super().__init__(Application.TEMPERATURE, Stream.TEMPERATURE4, packet_manager)
        self._slope = 1
        self._correction_factor = 0
        self._dcb_size = 57

    def get_device_configuration(self) -> List[Dict]:
        """
        Returns device configuration data.

        :return: A response packet as dictionary.
        :rtype: List[Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.get_device_configuration()
            print(x[0]["payload"]["data"])
            # [['0x9', '0x97'], ['0x7', '0x8FFF'], ['0xB', '0x2F6'], ... ]
        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_DCFG_REQ)
        response_packet = TemperatureDCFGPacket(self._destination, CommonCommand.GET_DCFG_RES)
        return self._send_packet_multi_response(request_packet, response_packet)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        stream = Stream(packet[:2])
        self._callback_data_helper(packet, TemperatureDataPacket(), stream=stream)

    def _update_stream_data(self, result):
        compensated_temperature = (result["payload"]["skin_temperature"] * self._slope) + self._correction_factor
        result["payload"]["compensated_temperature"] = compensated_temperature

    def set_callback(self, callback_function: Callable, args: Tuple = (), stream: Stream = STREAM_TEMPERATURE4) -> None:
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
            application = sdk.get_temperature_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2), stream=application.PPG)
        """
        stream = self._temperature_stream_helper(stream)
        self._callback_function[stream] = callback_function
        self._args[stream] = args

    @staticmethod
    def get_supported_streams() -> List[Stream]:
        """
        List all supported streams for Temperature.

        :return: Array of stream ID enums.
        :rtype: List[Stream]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.TEMPERATURE1: ['0xC8', '0x16']>, ... , <Stream.TEMPERATURE12: ['0xC8', '0x21']>]
        """
        return [TemperatureApplication.STREAM_TEMPERATURE1, TemperatureApplication.STREAM_TEMPERATURE2,
                TemperatureApplication.STREAM_TEMPERATURE3, TemperatureApplication.STREAM_TEMPERATURE4,
                TemperatureApplication.STREAM_TEMPERATURE5, TemperatureApplication.STREAM_TEMPERATURE6,
                TemperatureApplication.STREAM_TEMPERATURE7, TemperatureApplication.STREAM_TEMPERATURE8,
                TemperatureApplication.STREAM_TEMPERATURE9, TemperatureApplication.STREAM_TEMPERATURE10,
                TemperatureApplication.STREAM_TEMPERATURE11, TemperatureApplication.STREAM_TEMPERATURE12]

    def _temperature_stream_helper(self, stream: Stream) -> Stream:
        """
        Confirms stream is from list of Enums.
        """
        if stream in self.get_supported_streams():
            return stream
        else:
            logger.warning(f"{stream} is not supported stream, choosing {self.get_supported_streams()[0]} "
                           f"as default stream. use get_supported_streams() to know all supported streams.")
            return self.get_supported_streams()[0]

    def get_sensor_status(self, stream=STREAM_TEMPERATURE1) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.get_sensor_status(application.STREAM_TEMPERATURE1)
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0
        """
        stream = self._temperature_stream_helper(stream)
        request_packet = StreamStatusPacket(self._destination, CommonCommand.GET_SENSOR_STATUS_REQ)
        request_packet.set_payload("stream_address", stream)
        response_packet = StreamStatusPacket(self._destination, CommonCommand.GET_SENSOR_STATUS_RES)
        return self._send_packet(request_packet, response_packet)

    def write_dcb_to_lcfg(self) -> Dict:
        """
        Writes Device configuration block data to library configuration.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.write_dcb_to_lcfg()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = CommandPacket(self._destination, CommonCommand.SET_LCFG_REQ)
        response_packet = CommandPacket(self._destination, CommonCommand.SET_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes PPG Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            application.delete_device_configuration_block()
        """
        request_packet = TemperatureDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        response_packet = TemperatureDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_RES)
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
            application = sdk.get_temperature_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["data"])
            # []

        """
        request_packet = TemperatureDCBCommandPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        response_packet = TemperatureDCBPacket(self._destination, DCBCommand.READ_CONFIG_RES)
        response_dict = self._send_packet_multi_response(request_packet, response_packet)
        for packet in response_dict:
            packet["payload"]["data"] = utils.add_index_to_array(packet["payload"]["data"], to_hex=True)
        return response_dict

    def read_library_configuration(self, field: int) -> Dict:
        """
        Reads library configuration from specified field values.

        :param field: field values to read.
        :type field: int
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Fields Lower Limit
             - Fields Upper Limit
           * - 0x00
             - 0x14

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.read_library_configuration(0)
            print(x["payload"]["data"])
            # [['0x0', '0x0']]

        """
        request_packet = TemperatureLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_REQ)
        request_packet.set_payload("field", field)
        response_packet = TemperatureLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_RES)
        response_dict = self._send_packet(request_packet, response_packet)
        if field in [0, 1]:
            response_dict["payload"]["data"] = response_dict["payload"]["data"][:1]
        return response_dict

    def write_device_configuration_block(self, addresses_values: List[List[int]]) -> List:
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
            application = sdk.get_temperature_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["size"])
            # 2

        """
        dcb_array = []
        for address_value in addresses_values:
            dcb_array.append(address_value[1])
        result = []
        packets = math.ceil(len(dcb_array) / self._dcb_size)
        for packet in range(packets):
            addresses_value = dcb_array[packet * self._dcb_size: (packet + 1) * self._dcb_size]
            request_packet = TemperatureDCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
            request_packet.set_payload("size", len(addresses_value))
            request_packet.set_payload("packet_count", packets)
            request_packet.set_payload("data", addresses_value)
            response_packet = TemperatureDCBCommandPacket(self._destination, DCBCommand.WRITE_CONFIG_RES)
            result.append(self._send_packet(request_packet, response_packet))
        return result

    def write_device_configuration_block_from_file(self, filename: str) -> List:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            application.write_device_configuration_block_from_file("temperature_dcb.lcfg")

        """
        file = open(filename, 'r')
        regex = r"^<.*?>(?:.|\n)+?<\/.*?>"
        test_str = "".join(file.readlines())
        file.close()
        matches = re.findall(regex, test_str, re.MULTILINE)
        dcb = {}
        for x in matches:
            lines = x.split("\n")
            first_line = lines[0].strip()
            dcb[first_line] = lines[1:-1]

        if dcb.get("<TEMP_DCB>", None) is None:
            raise Exception("Invalid file format.")

        result = []
        selected_dcb = 0
        for line in dcb["<TEMP_DCB>"]:
            dcb_value = self._parse_single_dcb_line(line)
            result.append([int(dcb_value[0], 16), int(dcb_value[1], 16)])
            if int(dcb_value[0], 16) == 1:
                selected_dcb = format(int(dcb_value[1], 16), 'b').zfill(16)
        selected_dcb = list(reversed(selected_dcb))

        required_dcb = []
        for i, value in enumerate(selected_dcb):
            slot = (i + 65) * int(value)
            if slot and chr(slot) in ['C', 'D', 'J', 'K', 'L']:
                dcb_slot = f"<TEMP_SLOT{chr(slot)}_DCB>"
                required_dcb.append(dcb_slot)
                if dcb.get(dcb_slot, None) is None:
                    raise Exception(f"{dcb_slot} not present.")

        for dcb_slot in required_dcb:
            dcb_lines = dcb[dcb_slot]
            for line in dcb_lines:
                if line[0] != '#' and line[0] != '\n' and line[0] != ' ' and line[0] != '\t':
                    dcb_value = self._parse_single_dcb_line(line)
                    result.append([int(dcb_value[0], 16), int(dcb_value[1], 16)])
        if result:
            return self.write_device_configuration_block(result)

    def write_library_configuration(self, field: int, value) -> Dict:
        """
        Writes library configuration from List of fields and values.

        :param field: field index to write.
        :type field: int
        :param value: value needs to be int if field is 0,1 else it is a file address (str).
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Fields Lower Limit
             - Fields Upper Limit
           * - 0x00
             - 0x14

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.write_library_configuration(2, "temp.lcfg")
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        if field in [0, 1]:
            if not type(value) is int:
                raise Exception("Value needs to be int for fields 0 and 1.")
            data = [value]
        else:
            if not type(value) is str:
                raise Exception("Value needs to be file address (str) for fields other than 0 and 1.")
            addresses_values = self.device_configuration_file_to_list(value)
            data = []
            for address_value in addresses_values:
                data.append(address_value[1])

        request_packet = TemperatureLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        request_packet.set_payload("field", field)
        request_packet.set_payload("data", data)
        response_packet = TemperatureLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_RES)
        response_dict = self._send_packet(request_packet, response_packet)
        if field in [0, 1]:
            response_dict["payload"]["data"] = response_dict["payload"]["data"][:1]
        return response_dict

    def enable_csv_logging(self, filename, header=None, stream=STREAM_TEMPERATURE4) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :return: A response packet as dictionary.
        :param stream:
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.enable_csv_logging("temp.csv")
        """
        stream = self._temperature_stream_helper(stream)
        if header is None:
            header = ["Timestamp", "Skin Temperature", "Impedance", "Compensated Temperature"]
        self._csv_logger[stream] = CSVLogger(filename, header)

    def disable_csv_logging(self, stream=STREAM_TEMPERATURE4) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            x = application.disable_csv_logging()
        """
        stream = self._temperature_stream_helper(stream)
        if self._csv_logger.get(stream):
            self._csv_logger[stream].stop_logging()
        self._csv_logger[stream] = None

    def set_correction_factor(self, correction_factor: float):
        """
        Set correction factor.

        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            application.set_correction_factor(2.5)

        """
        self._correction_factor = correction_factor

    def set_slope(self, slope: float):
        """
        Set slope.

        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_temperature_application()
            application.set_slope(1.5)
        """
        self._slope = slope

    def subscribe_stream(self, stream: Stream = STREAM_TEMPERATURE4) -> Dict:
        """
        Subscribe to the specified TEMPERATURE stream.

        :param stream: Stream to subscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        stream = self._temperature_stream_helper(stream)
        return super().subscribe_stream(stream)

    def unsubscribe_stream(self, stream: Stream = STREAM_TEMPERATURE4) -> Dict:
        """
        Unsubscribe the specified TEMPERATURE stream.

        :param stream: Stream to unsubscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        stream = self._temperature_stream_helper(stream)
        return super().unsubscribe_stream(stream)
