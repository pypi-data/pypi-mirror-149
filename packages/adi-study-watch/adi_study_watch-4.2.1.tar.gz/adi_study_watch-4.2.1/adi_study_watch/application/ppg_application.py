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
from typing import Dict, List, Callable, Tuple

from ..core import utils
from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.packets.command_packet import CommandPacket
from ..core.packets.common_packets import VersionPacket
from ..core.enums.ppg_enums import PPGLcfgId, PPGCommand
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.stream_data_packets import PPGDataPacket, SYNCPPGDataPacket, AGCDataPacket, HRVDataPacket
from ..core.packets.ppg_packets import PPGDCBPacket, PPGLibraryConfigPacket, LibraryConfigDataPacket, \
    SetLibraryConfigPacket, PPGDCBCommandPacket

logger = logging.getLogger(__name__)


class PPGApplication(CommonStream):
    """
    PPG Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_ppg_application()

    """

    LCFG_ID_ADPD107 = PPGLcfgId.LCFG_ID_ADPD107
    LCFG_ID_ADPD185 = PPGLcfgId.LCFG_ID_ADPD185
    LCFG_ID_ADPD108 = PPGLcfgId.LCFG_ID_ADPD108
    LCFG_ID_ADPD188 = PPGLcfgId.LCFG_ID_ADPD188
    LCFG_ID_ADPD4000 = PPGLcfgId.LCFG_ID_ADPD4000

    STREAM_PPG = Stream.PPG
    STREAM_SYNC_PPG = Stream.SYNC_PPG
    STREAM_DYNAMIC_AGC = Stream.DYNAMIC_AGC_STREAM
    STREAM_HRV = Stream.HRV

    def __init__(self, packet_manager):
        super().__init__(Application.PPG, Stream.PPG, packet_manager)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        PPG Callback.
        """
        stream = Stream(packet[:2])
        response_packet = PPGDataPacket()
        if stream == self.STREAM_PPG:
            response_packet = PPGDataPacket()
        elif stream == self.STREAM_SYNC_PPG:
            response_packet = SYNCPPGDataPacket()
        elif stream == self.STREAM_DYNAMIC_AGC:
            response_packet = AGCDataPacket()
        elif stream == self.STREAM_HRV:
            response_packet = HRVDataPacket()
        self._callback_data_helper(packet, response_packet, stream)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes PPG Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            application.delete_device_configuration_block()
        """
        request_packet = PPGDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        response_packet = PPGDCBCommandPacket(self._destination, DCBCommand.ERASE_CONFIG_RES)
        return self._send_packet(request_packet, response_packet)

    def get_library_configuration(self) -> Dict:
        """
        Returns entire library configuration PPG.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_library_configuration()
            print(x["payload"]["data"])
            # [192, 0, 0, 0, 32, 0, 0, 0, 1, 0, ... , 0,0,0]

        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_LCFG_REQ)
        response_packet = LibraryConfigDataPacket(self._destination, CommonCommand.GET_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_lcfg_ids() -> List[PPGLcfgId]:
        """
        List all supported lcfg ID for PPG.

        :return: Array of lcfg ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_supported_lcfg_ids()
            print(x)
            # [<PPGLcfgId.LCFG_ID_ADPD107: ['0x6B']>, ... , <PPGLcfgId.LCFG_ID_ADPD4000: ['0x28']>]
        """
        return [PPGApplication.LCFG_ID_ADPD107, PPGApplication.LCFG_ID_ADPD185, PPGApplication.LCFG_ID_ADPD108,
                PPGApplication.LCFG_ID_ADPD188, PPGApplication.LCFG_ID_ADPD4000]

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["data"])
            # []

        """
        request_packet = PPGDCBCommandPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        response_packet = PPGDCBPacket(self._destination, DCBCommand.READ_CONFIG_RES)
        response_dict = self._send_packet(request_packet, response_packet)
        response_dict["payload"]["data"] = utils.add_index_to_array(response_dict["payload"]["data"], to_hex=True)
        return response_dict

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
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x0']]

        """
        data = [[field, 0] for field in fields]
        request_packet = PPGLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_REQ)
        request_packet.set_payload("size", len(data))
        request_packet.set_payload("data", data)
        response_packet = PPGLibraryConfigPacket(self._destination, CommonCommand.READ_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def set_library_configuration(self, lcfg_id: PPGLcfgId) -> Dict:
        """
        Set PPG to specified library configuration.

        :param lcfg_id: PPG lcfg_id to set, use get_supported_lcfg_ids() to list all supported lcfg IDs
        :type lcfg_id: PPGLcfgId
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.set_library_configuration(application.LCFG_ID_ADPD4000)
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        request_packet = SetLibraryConfigPacket(self._destination, CommonCommand.SET_LCFG_REQ)
        request_packet.set_payload("lcfg_id", lcfg_id)
        response_packet = CommandPacket(self._destination, CommonCommand.SET_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    def set_callback(self, callback_function: Callable, args: Tuple = (), stream: Stream = STREAM_PPG) -> None:
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
            application = sdk.get_ppg_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2), stream=application.PPG)
        """
        stream = self._ppg_stream_helper(stream)
        self._callback_function[stream] = callback_function
        self._args[stream] = args

    def subscribe_stream(self, stream=STREAM_PPG) -> Dict:
        """
        Subscribe to the PPG and SYNC PPG stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        stream = self._ppg_stream_helper(stream)
        return super().subscribe_stream(stream)

    def unsubscribe_stream(self, stream=STREAM_PPG) -> Dict:
        """
        Unsubscribe the PPG and SYNC PPG stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        stream = self._ppg_stream_helper(stream)
        return super().unsubscribe_stream(stream)

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
           * - 0x00
             - 0x38

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["size"])
            # 2
        """
        dcb_array = []
        for address_value in addresses_values:
            dcb_array.append(address_value[1])
        request_packet = PPGDCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        request_packet.set_payload("size", len(dcb_array))
        request_packet.set_payload("data", dcb_array)
        response_packet = PPGDCBCommandPacket(self._destination, DCBCommand.WRITE_CONFIG_RES)
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
           * - 0x00
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            application.write_device_configuration_block_from_file("ppg_dcb.lcfg")
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
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.write_library_configuration([[0x00, 0x1]])
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        request_packet = PPGLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        request_packet.set_payload("size", len(fields_values))
        request_packet.set_payload("data", fields_values)
        response_packet = PPGLibraryConfigPacket(self._destination, CommonCommand.WRITE_LCFG_RES)
        return self._send_packet(request_packet, response_packet)

    @staticmethod
    def get_supported_streams() -> List[Stream]:
        """
        List all supported streams for PPG.

        :return: Array of stream ID enums.
        :rtype: List[Stream]
        """
        return [PPGApplication.STREAM_PPG, PPGApplication.STREAM_SYNC_PPG, PPGApplication.STREAM_DYNAMIC_AGC,
                PPGApplication.STREAM_HRV]

    def _ppg_stream_helper(self, stream: Stream) -> Stream:
        """
        Confirms stream is from list of Enums.
        """
        if stream in self.get_supported_streams():
            return stream
        else:
            logger.warning(f"{stream} is not supported stream, choosing {self.get_supported_streams()[0]} "
                           f"as default stream. use get_supported_streams() to know all supported streams.")
            return self.get_supported_streams()[0]

    def get_version(self) -> Dict:
        """
        Returns PPG version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_version()
            print(x["payload"]["major_version"])
            # 3
            print(x["payload"]["minor_version"])
            # 4
            print(x["payload"]["patch_version"])
            # 3
            print(x["payload"]["version_string"])
            # ECG_App
            print(x["payload"]["build_version"])
            # TEST ECG_VERSION STRING
        """
        request_packet = CommandPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        response_packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_RES)
        return self._send_packet(request_packet, response_packet)

    def get_algo_version(self) -> Dict:
        """
        Returns PPG version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_algo_version()
            print(x["payload"]["major_version"])
            # 3
            print(x["payload"]["minor_version"])
            # 4
            print(x["payload"]["patch_version"])
            # 3
            print(x["payload"]["version_string"])
            # ECG_App
            print(x["payload"]["build_version"])
            # TEST ECG_VERSION STRING
        """
        request_packet = CommandPacket(self._destination, PPGCommand.GET_ALGO_VENDOR_VERSION_REQ)
        response_packet = VersionPacket(self._destination, PPGCommand.GET_ALGO_VENDOR_VERSION_RES)
        return self._send_packet(request_packet, response_packet)

    def enable_csv_logging(self, filename, header=None, stream: Stream = STREAM_PPG) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :param stream: PPG or SYNC_PPG stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.enable_csv_logging("ppg.csv", stream = application.PPG)
        """
        stream = self._ppg_stream_helper(stream)
        if header is None:
            if stream == self.STREAM_PPG:
                header = ["Timestamp", "HR", "Confidence", "HR Type"]
            elif stream == self.STREAM_SYNC_PPG:
                header = ["PPG Timestamp", "PPG", "ADXL Timestamp", "X", "Y", "Z"]
            elif stream == self.STREAM_DYNAMIC_AGC:
                header = ["Timestamp", ] + [f"MTS{i}" for i in range(0, 6)] + [f"Setting{i}" for i in range(0, 10)]
            elif stream == self.STREAM_HRV:
                header = ["Timestamp", "RR Interval", "Is Gap", "RMSSD"]
        self._csv_logger[stream] = CSVLogger(filename, header)

    def disable_csv_logging(self, stream: Stream = STREAM_PPG) -> None:
        """
        Stops logging stream data into CSV.

        :param stream: PPG or SYNC_PPG stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.disable_csv_logging(stream = application.PPG)
        """
        stream = self._ppg_stream_helper(stream)
        if self._csv_logger.get(stream):
            self._csv_logger[stream].stop_logging()
        self._csv_logger[stream] = None
