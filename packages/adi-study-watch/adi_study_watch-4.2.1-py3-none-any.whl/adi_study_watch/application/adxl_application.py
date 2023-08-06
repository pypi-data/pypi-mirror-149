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


import logging
from typing import List, Dict

from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.packets.command_packet import CommandPacket
from ..core.enums.adxl_enums import ADXLDevice, ADXLCommand
from ..core.packets.stream_data_packets import ADXLDataPacket
from ..core.packets.common_packets import DecimationFactorPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.adxl_packets import ADXLConfigPacket, ADXLRegisterWritePacket, ADXLRegisterReadPacket, \
    ADXLDCBPacket, ADXLDCFGPacket, ADXLDCBCommandPacket

logger = logging.getLogger(__name__)


class ADXLApplication(CommonStream):
    """
    ADXL Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_adxl_application()

    """
    DEVICE_362 = ADXLDevice.DEVICE_362

    def __init__(self, packet_manager):
        super().__init__(Application.ADXL, Stream.ADXL, packet_manager)
        self._dcb_size = 25

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes Adxl Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            application.delete_device_configuration_block()
        """
        request_packet = ADXLDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        response_packet = ADXLDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def get_decimation_factor(self) -> Dict:
        """
        Returns stream decimation factor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_decimation_factor()
            print(x["payload"]["decimation_factor"])
            # 1

        """
        request_packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_REQ)
        request_packet.set_payload("stream_address", self._stream)
        response_packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_RES)
        return self._send_packet(request_packet, response_packet)

    def get_device_configuration(self) -> Dict:
        """
        Returns device configuration data.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_device_configuration()
            print(x["payload"]["dcfg_data"])
            # [['0x9', '0x97'], ['0x7', '0x8FFF'], ['0xB', '0x2F6'], ... ]
        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_DCFG_REQ)
        response_packet = ADXLDCFGPacket(self._destination, CommonCommand.GET_DCFG_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_devices() -> List[ADXLDevice]:
        """
        List all supported device ID for adxl.

        :return: Array of device ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_supported_devices()
            print(x)
            # [<ADXLDevice.DEVICE_362: ['0x6A', '0x1']>]
        """
        return [ADXLApplication.DEVICE_362]

    def load_configuration(self, device_id: ADXLDevice) -> Dict:
        """
        Loads specified device id configuration.

        :param device_id: Device ID to load, use get_supported_devices() to list all supported devices.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5,8

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_supported_devices()
            print(x)
            # [<ADXLDevice.DEVICE_362: ['0x6A', '0x1']>]
            x = application.load_configuration(application.DEVICE_362)
            print(x["payload"]["device_id"])
            # <ADXLDevice.DEVICE_362: ['0x6A', '0x1']>

        """
        request_packet = ADXLConfigPacket(self._destination, ADXLCommand.LOAD_CONFIG_REQ)
        request_packet.set_payload("device_id", device_id)
        response_packet = ADXLConfigPacket(self._destination, ADXLCommand.LOAD_CONFIG_RES)
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
            application = sdk.get_adxl_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["data"])
            # []

        """
        request_packet = ADXLDCBCommandPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        response_packet = ADXLDCBPacket(self._destination, DCBCommand.READ_CONFIG_RES)
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
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.read_register([0x15, 0x20, 0x2E])
            print(x["payload"]["data"])
            # [['0x15', '0x0'], ['0x20', '0x0'], ['0x2E', '0x0']]
        """
        data = [[address, 0] for address in addresses]
        request_packet = ADXLRegisterReadPacket(self._destination, CommonCommand.REGISTER_READ_REQ)
        request_packet.set_payload("size", len(data))
        request_packet.set_payload("data", data)
        response_packet = ADXLRegisterReadPacket(self._destination, CommonCommand.REGISTER_READ_RES)
        return self._send_packet(request_packet, response_packet)

    def set_decimation_factor(self, decimation_factor: int) -> Dict:
        """
        Sets decimation factor for adxl stream.

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
            application = sdk.get_adxl_application()
            x = application.set_decimation_factor(2)
            print(x["payload"]["decimation_factor"])
            # 2

        """
        request_packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_REQ)
        request_packet.set_payload("stream_address", self._stream)
        request_packet.set_payload("decimation_factor", decimation_factor)
        response_packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_RES)
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

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x20
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["size"])
            # 2

        """
        request_packet = ADXLDCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        request_packet.set_payload("size", len(addresses_values))
        request_packet.set_payload("data", addresses_values)
        response_packet = ADXLDCBCommandPacket(self._destination, DCBCommand.WRITE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def write_device_configuration_block_from_file(self, filename: str) -> Dict:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x20
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            application.write_device_configuration_block_from_file("adxl_dcb.dcfg")

        """
        result = self.device_configuration_file_to_list(filename)
        if result:
            return self.write_device_configuration_block(result)

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
           * - 0x20
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
            print(x["payload"]["data"])
            # [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']]

        """
        request_packet = ADXLRegisterWritePacket(self._destination, CommonCommand.REGISTER_WRITE_REQ)
        request_packet.set_payload("size", len(addresses_values))
        request_packet.set_payload("data", addresses_values)
        response_packet = ADXLRegisterWritePacket(self._destination, CommonCommand.REGISTER_WRITE_RES)
        return self._send_packet(request_packet, response_packet)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, ADXLDataPacket())

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
            application = sdk.get_adxl_application()
            x = application.enable_csv_logging("adxl.csv")
        """
        if header is None:
            header = ["Timestamp", "X", "Y", "Z"]
        self._csv_logger[Stream.ADXL] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger.get(Stream.ADXL):
            self._csv_logger[Stream.ADXL].stop_logging()
        self._csv_logger[Stream.ADXL] = None
