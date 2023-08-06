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
from ..core.packets.sqi_packets import SQISlotPacket
from ..core.enums.sqi_enum import SQISlot, SQICommand
from ..core.packets.common_packets import VersionPacket
from ..core.packets.command_packet import CommandPacket
from ..core.packets.stream_data_packets import SQIDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand

logger = logging.getLogger(__name__)


class SQIApplication(CommonStream):
    """
    SQI Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_sqi_application()

    """

    SLOT_F = SQISlot.SLOT_F
    SLOT_G = SQISlot.SLOT_G
    SLOT_H = SQISlot.SLOT_H
    SLOT_I = SQISlot.SLOT_I

    def __init__(self, packet_manager):
        super().__init__(Application.SQI, Stream.SQI, packet_manager)

    @staticmethod
    def get_supported_slots() -> List[SQISlot]:
        """
        List all supported slots for SQI.

        :return: Array of slot ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.get_supported_slots()
            print(x)
            # [<SQISlot.SLOT_F: ['0x6', '0x0']>, ... , <SQISlot.SLOT_I: ['0x9', '0x0']>]

        """
        return [SQIApplication.SLOT_F, SQIApplication.SLOT_G, SQIApplication.SLOT_H, SQIApplication.SLOT_I]

    def set_slot(self, slot_id: SQISlot) -> Dict:
        """
        Set specified Slot ID for SQI.

        :param slot_id: slot_num to set, use get_supported_slots() to list all supported slot ID.
        :type slot_id: SQISlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.get_supported_slots()
            print(x)
            # [<SQISlot.SLOT_F: ['0x6', '0x0']>, ... , <SQISlot.SLOT_I: ['0x9', '0x0']>]
            x = application.set_slot(application.SLOT_F)
            print(x["payload"]["sqi_slot"])
            # SQISlot.SLOT_F
        """
        request_packet = SQISlotPacket(self._destination, SQICommand.SET_SLOT_REQ)
        request_packet.set_payload("slot", slot_id)
        response_packet = SQISlotPacket(self._destination, SQICommand.SET_SLOT_RES)
        return self._send_packet(request_packet, response_packet)

    def get_version(self) -> Dict:
        """
        Returns SQI version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
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
        Returns SQI version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
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
        request_packet = CommandPacket(self._destination, SQICommand.GET_ALGO_VENDOR_VERSION_REQ)
        response_packet = VersionPacket(self._destination, SQICommand.GET_ALGO_VENDOR_VERSION_RES)
        return self._send_packet(request_packet, response_packet)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, SQIDataPacket())

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
            application = sdk.get_sqi_application()
            x = application.enable_csv_logging("sqi.csv")
        """
        if header is None:
            header = ["Timestamp", "SQI"]
        self._csv_logger[Stream.SQI] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger.get(Stream.SQI):
            self._csv_logger[Stream.SQI].stop_logging()
        self._csv_logger[Stream.SQI] = None
