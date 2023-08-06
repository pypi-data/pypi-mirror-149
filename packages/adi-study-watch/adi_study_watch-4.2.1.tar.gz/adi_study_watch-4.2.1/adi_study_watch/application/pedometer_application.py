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

from typing import Dict

from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.packets.command_packet import CommandPacket
from ..core.packets.common_packets import VersionPacket
from ..core.enums.pedometer_enums import PedometerCommand
from ..core.packets.stream_data_packets import PedometerDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand


class PedometerApplication(CommonStream):
    """
    Pedometer Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_pedometer_application()

    """

    def __init__(self, packet_manager):
        super().__init__(Application.PEDOMETER, Stream.PEDOMETER, packet_manager)

    def get_version(self) -> Dict:
        """
        Returns Pedometer version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pedometer_application()
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
        Returns Pedometer version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pedometer_application()
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
        request_packet = CommandPacket(self._destination, PedometerCommand.GET_ALGO_VENDOR_VERSION_REQ)
        response_packet = VersionPacket(self._destination, PedometerCommand.GET_ALGO_VENDOR_VERSION_RES)
        return self._send_packet(request_packet, response_packet)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, PedometerDataPacket())

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
            application = sdk.get_pedometer_application()
            x = application.enable_csv_logging("ped.csv")
        """
        if header is None:
            header = ["Timestamp", "Steps"]
        self._csv_logger[Stream.PEDOMETER] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pedometer_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger.get(Stream.PEDOMETER):
            self._csv_logger[Stream.PEDOMETER].stop_logging()
        self._csv_logger[Stream.PEDOMETER] = None
