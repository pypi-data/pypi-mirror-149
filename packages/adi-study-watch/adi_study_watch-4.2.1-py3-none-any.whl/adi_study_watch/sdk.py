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
import os
import time
import logging
from typing import List
from datetime import datetime

import serial
from tqdm import tqdm
import serial.tools.list_ports

from .core import utils
from .core.ble_manager import BLEManager
from .core.enums.board_enums import Board
from .core.enums.fs_enums import FSCommand
from .core.enums.pm_enums import PMCommand
from .core.enums.sqi_enum import SQICommand
from .core.enums.ppg_enums import PPGCommand
from .core.enums.ecg_enums import ECGCommand
from .core.packet_manager import PacketManager
from .application.pm_application import PMApplication
from .core.packets.adpd_packets import ADPDDCFGPacket
from .application.fs_application import FSApplication
from .core.packets.adxl_packets import ADXLDCFGPacket
from .application.eda_application import EDAApplication
from .application.sqi_application import SQIApplication
from .application.ecg_application import ECGApplication
from .application.bia_application import BIAApplication
from .application.ppg_application import PPGApplication
from .core.enums.pedometer_enums import PedometerCommand
from .application.adxl_application import ADXLApplication
from .application.adpd_application import ADPDApplication
from .application.test_application import TestApplication
from .application.user0_application import User0Application
from .core.packets.ecg_packets import ECGLibraryConfigPacket
from .core.packets.ppg_packets import LibraryConfigDataPacket
from .application.ad7156_application import AD7156Application
from .core.packets.fs_packets import KeyValuePairResponsePacket
from .application.vsm_mb_sb.pm_application import VSMPMApplication
from .application.low_touch_application import LowTouchApplication
from .core.packets.common_packets import VersionPacket, AlarmPacket
from .application.pedometer_application import PedometerApplication
from .core.packets.pm_packets import DateTimePacket, SystemInfoPacket
from .application.temperature_application import TemperatureApplication
from .core.enums.common_enums import Application, CommonCommand, CommonStatus

logger = logging.getLogger(__name__)


class SDK:
    """
    SDK class
    """

    READING_LOG = 0
    JOINING_CSV = 1

    STUDY_WATCH = Board.STUDY_WATCH
    VSM_MB_SB = Board.VSM_MB_SB
    __version__ = "4.2.1"

    def __init__(self, serial_port_address: str, mac_address: str = None, baud_rate: int = 921600,
                 board=Board.STUDY_WATCH, logging_filename: str = None, debug: bool = False,
                 sync_date_time=True, check_version=True, ble_vendor_id: int = 0x0456, ble_product_id: int = 0x2CFE,
                 ble_serial_number: str = None, ble_timeout: int = 10, **kwargs):
        """
        Creates a SDK object

        :param serial_port_address: serial port of the device connected.
        :param mac_address: MAC address of the device.
        :param baud_rate: baud rate.
        :param board: board to connect (STUDY_WATCH, VSM_MB_SB).
        :param logging_filename: log file name.
        :param debug: control for debug mode.
        :param sync_date_time: Sync current system date and time with firmware (Default=True).
        :param check_version: Check for SDK and firmware compatibility (Default=True).
        :param ble_vendor_id: BLE Vendor ID for ADI dongle (Default=0x0456).
        :param ble_product_id: BLE Product ID for ADI dongle (Default=0x2CFE).
        :param ble_serial_number: BLE Serial Number ID for ADI dongle, if none then it will choose first device
         with given vendor and product ID (Default=None).
        :param ble_timeout: BLE connection timeout (Default=10).
        """
        self._board = None
        self._mac_address = None
        self._ble_manager = None
        self._alarms_args = None
        self._serial_object = None
        self._packet_manager = None
        self._alarms_callback_function = None
        self.reconnect(serial_port_address, mac_address, baud_rate, board, logging_filename, debug,
                       sync_date_time, check_version, ble_vendor_id, ble_product_id, ble_serial_number, ble_timeout,
                       **kwargs)

    def reconnect(self, serial_port_address: str, mac_address: str = None, baud_rate: int = 921600,
                  board=Board.STUDY_WATCH, logging_filename: str = None, debug: bool = False,
                  sync_date_time=False, check_version=False, ble_vendor_id: int = 0x0456, ble_product_id: int = 0x2CFE,
                  ble_serial_number: str = None, ble_timeout: int = 10, **kwargs):
        """
        reconnect method allows you to reconnect to SDK; you must call disconnect before using connect.

        :param serial_port_address: serial port of the device connected.
        :param mac_address: MAC address of the device.
        :param baud_rate: baud rate.
        :param board: board to connect (STUDY_WATCH, VSM_MB_SB).
        :param logging_filename: log file name.
        :param debug: control for debug mode.
        :param sync_date_time: Sync current system date and time with firmware (Default=False).
        :param check_version: Check for SDK and firmware compatibility (Default=False).
        :param ble_vendor_id: BLE Vendor ID for ADI dongle (Default=0x0456).
        :param ble_product_id: BLE Product ID for ADI dongle (Default=0x2CFE).
        :param ble_serial_number: BLE Serial Number ID for ADI dongle, if none then it will choose first device
         with given vendor and product ID (Default=None).
        :param ble_timeout: BLE connection timeout (Default=10).
        """

        log_format = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        if logging_filename:
            logging.basicConfig(filename=logging_filename, filemode='a', format=log_format, datefmt=date_format,
                                level=logging.DEBUG)
        else:
            if debug:
                logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)
            else:
                logging.basicConfig(format=log_format, datefmt=date_format)
        logger.debug("----- Study Watch SDK Started -----")
        self._mac_address = mac_address
        self._board = board
        version = None
        for _ in range(3):
            if self._mac_address:
                self._ble_manager = BLEManager(ble_vendor_id, ble_product_id, ble_timeout, ble_serial_number)
                self._ble_manager.disconnect()
                self._ble_manager.connect(self._mac_address)
            self._serial_object = serial.Serial(serial_port_address, baud_rate, **kwargs)
            self._packet_manager = PacketManager(self._serial_object)
            self._subscribe_alarms()
            if self._mac_address:
                self._packet_manager.set_ble_source()
            else:
                self._packet_manager.set_usb_source()

            self._packet_manager.start_receive_and_process_threads()
            pm_app = self.get_pm_application()
            if sync_date_time:
                pm_app.set_datetime(datetime.now())
            version = pm_app.get_version()
            if not version["payload"]["status"] == CommonStatus.NO_RESPONSE:
                break
            self.disconnect()

        if check_version:
            self._check_version(version)

    @staticmethod
    def _check_version(version):
        if version["payload"]["status"] == CommonStatus.NO_RESPONSE:
            raise Exception("Can't establish connection to the study watch.")

        supported_version = f"{version['payload']['major_version']}.{version['payload']['minor_version']}." \
                            f"{version['payload']['patch_version']}"
        if not supported_version == "5.8.0":
            logger.warning(f"Current firmware is not fully compatible with this SDK Version.\n"
                           f"Supported Firmware Version :: 5.8.0\n"
                           f"Current Firmware Version :: {supported_version}\n"
                           f"SDK Version :: {SDK.__version__}\n"
                           f"Latest firmware: https://github.com/analogdevicesinc/study-watch-sdk/tree/main/firmware")

    def _subscribe_alarms(self):
        for app in [Application.PM, Application.FS, Application.LT_APP]:
            packet_id = self._get_packet_id(CommonCommand.ALARM_NOTIFICATION, app)
            self._packet_manager.subscribe(packet_id, self._alarms_callback)

    # noinspection PyUnusedLocal
    def _alarms_callback(self, data, packet_id):
        response_packet = AlarmPacket()
        response_packet.decode_packet(data)
        response_packet = response_packet.get_dict()
        if self._alarms_callback_function:
            self._alarms_callback_function(response_packet)
        else:
            logger.warning(f"ALARM - {response_packet['header']['source']} - {response_packet['payload']['status']}")

    def set_alarms_callback(self, callback_function, args=()):
        self._alarms_args = args
        self._alarms_callback_function = callback_function

    def get_adpd_application(self):
        """
        Creates an adpd application object

        :returns: an Adpd Application
        :rtype: ADPDApplication
        """
        return ADPDApplication(self._packet_manager)

    def get_adxl_application(self):
        """
        Creates an adxl application object

        :returns: an Adxl Application
        :rtype: ADXLApplication
        """
        return ADXLApplication(self._packet_manager)

    def get_ecg_application(self):
        """
        Creates an ecg application object

        :returns: an ecg Application
        :rtype: ECGApplication
        """
        return ECGApplication(self._packet_manager)

    def get_eda_application(self):
        """
        Creates an eda application object

        :returns: an eda Application
        :rtype: EDAApplication
        """
        return EDAApplication(self._packet_manager)

    def get_fs_application(self):
        """
        Creates an fs application object

        :returns: an fs Application
        :rtype: FSApplication
        """
        return FSApplication(self._packet_manager)

    def get_pedometer_application(self):
        """
        Creates an pedometer application object

        :returns: an pedometer Application
        :rtype: PedometerApplication
        """
        return PedometerApplication(self._packet_manager)

    def get_pm_application(self):
        """
        Creates an pm application object

        :returns: an pm Application
        :rtype: VSMPMApplication
        """
        if self._board == Board.VSM_MB_SB:
            return VSMPMApplication(self._packet_manager)
        else:
            return PMApplication(self._packet_manager)

    def get_ppg_application(self):
        """
        Creates an ppg application object

        :returns: an Ppg Application
        :rtype: PPGApplication
        """
        return PPGApplication(self._packet_manager)

    def get_temperature_application(self):
        """
        Creates a temperature application object

        :returns: a Temperature Application
        :rtype: TemperatureApplication
        """
        return TemperatureApplication(self._packet_manager)

    def get_sqi_application(self):
        """
        Creates a sqi application object

        :returns: a SQI Application
        :rtype: SQIApplication
        """
        return SQIApplication(self._packet_manager)

    def get_bia_application(self):
        """
        Creates a bia application object

        :returns: a BIA Application
        :rtype: BIAApplication
        """
        return BIAApplication(self._packet_manager)

    def get_ad7156_application(self):
        """
        Creates a ad7156 application object

        :returns: a AD7156 Application
        :rtype: AD7156Application
        """
        return AD7156Application(self._packet_manager)

    def get_low_touch_application(self):
        """
        Creates a low touch application object

        :returns: a LowTouch Application
        :rtype: LowTouchApplication
        """
        return LowTouchApplication(self._packet_manager)

    def get_test_application(self, key_test_callback=None, cap_sense_callback=None):
        """
        Creates a test application object, used for internal firmware testing.

        :returns: a Test Application
        :rtype: TestApplication
        """
        return TestApplication(key_test_callback, cap_sense_callback, self._packet_manager)

    def get_user0_application(self):
        """
        Creates a User0 application object

        :returns: a User Application
        :rtype: User0Application
        """
        return User0Application(self._packet_manager)

    def unsubscribe_all_streams(self):
        """
        Unsubscribe from all application streams
        """
        result = [self.get_adxl_application().unsubscribe_stream(), self.get_sqi_application().unsubscribe_stream(),
                  self.get_ppg_application().unsubscribe_stream(), self.get_bia_application().unsubscribe_stream(),
                  self.get_ecg_application().unsubscribe_stream(), self.get_eda_application().unsubscribe_stream(),
                  self.get_temperature_application().unsubscribe_stream(),
                  self.get_pedometer_application().unsubscribe_stream()]
        adpd_app = self.get_adpd_application()
        fs_app = self.get_fs_application()
        for stream in adpd_app.get_supported_streams():
            result.append(adpd_app.unsubscribe_stream(stream))
        for stream in fs_app.get_supported_streams():
            result.append(fs_app.unsubscribe_stream(stream))
        return result

    @staticmethod
    def _get_packet_id(response_command, destination):
        return utils.join_multi_length_packets(destination.value + response_command.value)

    @staticmethod
    def get_supported_boards():
        return [SDK.STUDY_WATCH, SDK.VSM_MB_SB]

    @staticmethod
    def get_available_ports() -> List:
        """
        returns the list of tuple (port, description, hardware_id) of available ports.
        """
        ports = serial.tools.list_ports.comports()
        result = []
        for port, desc, hardware_id in sorted(ports):
            result.append((port, desc, hardware_id))
        return result

    @staticmethod
    def join_csv(*args, output_filename="combined.csv", display_progress=True, progress_callback=None):
        """
        Joins multiple data stream csv file into single csv file.
        """
        file_size = os.path.getsize(args[0])
        current_size = 0
        progress_bar = None
        if display_progress:
            progress_bar = tqdm(total=file_size)
            progress_bar.set_description("ADPD csv join")
        space = {}
        header = []
        all_csv = {}
        first_iter = {}
        result_file = open(output_filename, 'w')

        for file in args:
            csv_file = open(file, 'r')
            header = [csv_file.readline(), csv_file.readline()]
            all_csv[file] = csv_file
            first_iter[file] = True
            space[file] = 0

        # write header
        result_file.write(header[0])
        result_file.write(header[1])

        while True:
            result_line = ""
            empty_file_count = 0
            for file in args:
                line = all_csv[file].readline().strip()
                # checking for empty file condition
                if len(line) == 0:
                    empty_file_count += 1
                    result_line += "," * space[file]
                    continue
                # saving number of elements in a row
                if first_iter[file]:
                    space[file] = len(line.split(","))
                    first_iter[file] = False
                # concat row
                result_line += line + ","
                # progress bar
                if file == args[0]:
                    line_size = len(line.encode('utf-8'))
                    current_size += line_size
                    if display_progress:
                        progress_bar.update(line_size)
                    if progress_callback:
                        progress_callback(SDK.JOINING_CSV, file_size, current_size)
            # break condition
            if empty_file_count == len(args):
                break
            result_file.write(result_line + "\n")

        # cleanup
        result_file.close()
        if display_progress:
            progress_bar.update(file_size - current_size)
            progress_bar.close()
        if progress_callback:
            progress_callback(SDK.JOINING_CSV, file_size, file_size)
        for file in args:
            all_csv[file].close()

    @staticmethod
    def _csv_write_config(file, config, header):
        file.write(f"Address, Value, {header}\n")
        if not type(config) == list:
            config = [config]
        for data in config:
            for value in data["payload"]["data"]:
                if header == "#PPG_LCFG":
                    file.write(f"{value}\n")
                else:
                    file.write(f"{value[0]}, {value[1]}\n")
        file.write(f"\n")

    @staticmethod
    def _csv_write_version(file, config, header):
        file.write(f"Module, {header}\n")
        file.write(f"Major version, {config['payload']['major_version']}\n")
        file.write(f"Minor version, {config['payload']['minor_version']}\n")
        file.write(f"Patch version, {config['payload']['patch_version']}\n")
        file.write(f"Version string, {config['payload']['version_string']}\n")
        file.write(f"Build version, {config['payload']['build_version']}\n")
        file.write(f"\n")

    @staticmethod
    def _packet_loss(file, msg, packet_count):
        if packet_count:
            file.write(f"{msg}, {packet_count}\n")
        else:
            file.write(f"{msg}, 0\n")

    # noinspection PyProtectedMember,PyTypeChecker,PyUnresolvedReferences
    @staticmethod
    def convert_log_to_csv(filename, display_progress=True, progress_callback=None):
        """
        Converts M2M2 log file into csv.
        """
        if not os.path.exists(filename):
            raise Exception("File not Found.")

        info_result = {
            "key_value_pair": None, "datetime": None, "system_info": None, "version": None, "ppg_algo_version": None,
            "ped_algo_version": None, "ecg_algo_version": None, "sqi_algo_version": None, "adpd_dcfg": None,
            "adxl_dcfg": None, "ppg_lcfg": None, "ecg_lcfg": None,
        }
        folder_name = filename.split(".")[0]
        try:
            os.mkdir(folder_name)
        except Exception as e:
            logger.debug(e)

        # creating all applications
        packet_manager = PacketManager(None, filename=filename)
        packet_manager.set_usb_source()
        ad7156_app = AD7156Application(packet_manager)
        adpd_app = ADPDApplication(packet_manager)
        adxl_app = ADXLApplication(packet_manager)
        ecg_app = ECGApplication(packet_manager)
        eda_app = EDAApplication(packet_manager)
        ped_app = PedometerApplication(packet_manager)
        ppg_app = PPGApplication(packet_manager)
        temp_app = TemperatureApplication(packet_manager)
        sqi_app = SQIApplication(packet_manager)
        bia_app = BIAApplication(packet_manager)
        pm_app = PMApplication(packet_manager)

        # enabling csv logging
        adxl_app.enable_csv_logging(f"{folder_name}/adxl.csv")
        for i, stream in enumerate(adpd_app.get_supported_streams()):
            if stream == adpd_app.STREAM_STATIC_AGC:
                adpd_app.enable_csv_logging(f"{folder_name}/static_agc.csv", stream=adpd_app.STREAM_STATIC_AGC)
            else:
                adpd_app.enable_csv_logging(f"{folder_name}/adpd{i + 1}.csv", stream=stream)
        ecg_app.enable_csv_logging(f"{folder_name}/ecg.csv")
        eda_app.enable_csv_logging(f"{folder_name}/eda.csv")
        ped_app.enable_csv_logging(f"{folder_name}/ped.csv")
        ppg_app.enable_csv_logging(f"{folder_name}/ppg.csv", stream=ppg_app.STREAM_PPG)
        ppg_app.enable_csv_logging(f"{folder_name}/sync_ppg.csv", stream=ppg_app.STREAM_SYNC_PPG)
        ppg_app.enable_csv_logging(f"{folder_name}/dynamic_agc.csv", stream=ppg_app.STREAM_DYNAMIC_AGC)
        ppg_app.enable_csv_logging(f"{folder_name}/hrv.csv", stream=ppg_app.STREAM_HRV)
        for i, stream in enumerate(temp_app.get_supported_streams()):
            temp_app.enable_csv_logging(f"{folder_name}/temperature{i + 1}.csv", stream=stream)
        sqi_app.enable_csv_logging(f"{folder_name}/sqi.csv")
        bia_app.enable_csv_logging(f"{folder_name}/bia.csv")
        pm_app.enable_csv_logging(f"{folder_name}/adp.csv")
        ad7156_app.enable_csv_logging(f"{folder_name}/ad7156.csv")

        # subscribing
        apps = [adxl_app, ecg_app, eda_app, ped_app, sqi_app, bia_app, ad7156_app]
        for app in apps:
            app._subscribe_stream_data()
        ppg_app._subscribe_stream_data(ppg_app.STREAM_PPG)
        ppg_app._subscribe_stream_data(ppg_app.STREAM_SYNC_PPG)
        ppg_app._subscribe_stream_data(ppg_app.STREAM_DYNAMIC_AGC)
        ppg_app._subscribe_stream_data(ppg_app.STREAM_HRV)
        pm_app._subscribe_stream_data(pm_app.STREAM_BATTERY)
        for stream in adpd_app.get_supported_streams():
            adpd_app._subscribe_stream_data(stream)
        for stream in temp_app.get_supported_streams():
            temp_app._subscribe_stream_data(stream)

        def update_info_dict(packet, response_byte, key):
            packet.decode_packet(response_byte)
            if info_result.get(key) is None:
                info_result[key] = packet.get_dict()
            else:
                if type(info_result[key]) == list:
                    info_result[key] = info_result[key] + [packet.get_dict()]
                else:
                    info_result[key] = [info_result[key], packet.get_dict()]

        # noinspection PyShadowingNames,PyProtectedMember
        def callback(response_byte, packet_id):
            if SDK._get_packet_id(FSCommand.SET_KEY_VALUE_PAIR_RES, Application.FS) == packet_id:
                packet = KeyValuePairResponsePacket()
                update_info_dict(packet, response_byte, "key_value_pair")
            elif SDK._get_packet_id(PMCommand.GET_DATE_TIME_RES, Application.PM) == packet_id:
                packet = DateTimePacket()
                update_info_dict(packet, response_byte, "datetime")
                response_packet = info_result["datetime"]
                dt = datetime(response_packet['payload']['year'], response_packet['payload']['month'],
                              response_packet['payload']['day'], response_packet['payload']['hour'],
                              response_packet['payload']['minute'], response_packet['payload']['second'])
                for _stream in adpd_app.get_supported_streams():
                    adpd_app._update_timestamp(dt, _stream, generate_ts=True)
                for _stream in temp_app.get_supported_streams():
                    temp_app._update_timestamp(dt, _stream, generate_ts=True)
                for _app in apps:
                    _app._update_timestamp(dt, generate_ts=True)
                ppg_app._update_timestamp(dt, ppg_app.STREAM_PPG, generate_ts=True)
                ppg_app._update_timestamp(dt, ppg_app.STREAM_SYNC_PPG, generate_ts=True)
                ppg_app._update_timestamp(dt, ppg_app.STREAM_DYNAMIC_AGC, generate_ts=True)
                ppg_app._update_timestamp(dt, ppg_app.STREAM_HRV, generate_ts=True)
                pm_app._update_timestamp(dt, pm_app.STREAM_BATTERY, generate_ts=True)

            elif SDK._get_packet_id(PMCommand.SYS_INFO_RES, Application.PM) == packet_id:
                packet = SystemInfoPacket()
                update_info_dict(packet, response_byte, "system_info")
            elif SDK._get_packet_id(CommonCommand.GET_VERSION_RES, Application.PM) == packet_id:
                packet = VersionPacket()
                update_info_dict(packet, response_byte, "version")
            elif SDK._get_packet_id(PPGCommand.GET_ALGO_VENDOR_VERSION_RES, Application.PPG) == packet_id:
                packet = VersionPacket()
                update_info_dict(packet, response_byte, "ppg_algo_version")
            elif SDK._get_packet_id(PedometerCommand.GET_ALGO_VENDOR_VERSION_RES, Application.PEDOMETER) == packet_id:
                packet = VersionPacket()
                update_info_dict(packet, response_byte, "ped_algo_version")
            elif SDK._get_packet_id(ECGCommand.GET_ALGO_VENDOR_VERSION_RES, Application.ECG) == packet_id:
                packet = VersionPacket()
                update_info_dict(packet, response_byte, "ecg_algo_version")
            elif SDK._get_packet_id(SQICommand.GET_ALGO_VENDOR_VERSION_RES, Application.SQI) == packet_id:
                packet = VersionPacket()
                update_info_dict(packet, response_byte, "sqi_algo_version")
            elif SDK._get_packet_id(CommonCommand.GET_DCFG_RES, Application.ADXL) == packet_id:
                packet = ADXLDCFGPacket()
                update_info_dict(packet, response_byte, "adxl_dcfg")
            elif SDK._get_packet_id(CommonCommand.GET_DCFG_RES, Application.ADPD) == packet_id:
                packet = ADPDDCFGPacket()
                update_info_dict(packet, response_byte, "adpd_dcfg")
            elif SDK._get_packet_id(CommonCommand.GET_LCFG_RES, Application.PPG) == packet_id:
                packet = LibraryConfigDataPacket()
                update_info_dict(packet, response_byte, "ppg_lcfg")
            elif SDK._get_packet_id(CommonCommand.READ_LCFG_RES, Application.ECG) == packet_id:
                packet = ECGLibraryConfigPacket()
                update_info_dict(packet, response_byte, "ecg_lcfg")

        initial_packets = [
            [FSCommand.SET_KEY_VALUE_PAIR_RES, Application.FS],
            [PMCommand.GET_DATE_TIME_RES, Application.PM],
            [PMCommand.SYS_INFO_RES, Application.PM],
            [CommonCommand.GET_VERSION_RES, Application.PM],
            [PPGCommand.GET_ALGO_VENDOR_VERSION_RES, Application.PPG],
            [PedometerCommand.GET_ALGO_VENDOR_VERSION_RES, Application.PEDOMETER],
            [ECGCommand.GET_ALGO_VENDOR_VERSION_RES, Application.ECG],
            [SQICommand.GET_ALGO_VENDOR_VERSION_RES, Application.SQI],
            [CommonCommand.GET_DCFG_RES, Application.ADXL],
            [CommonCommand.GET_DCFG_RES, Application.ADPD],
            [CommonCommand.GET_LCFG_RES, Application.PPG],
            [CommonCommand.READ_LCFG_RES, Application.ECG]
        ]
        for initial_packet in initial_packets:
            packet_id = SDK._get_packet_id(initial_packet[0], initial_packet[1])
            packet_manager.subscribe(packet_id, callback)

        # process file
        packet_manager.process_file(display_progress, progress_callback)

        # disabling csv logging.
        for stream in adpd_app.get_supported_streams():
            adpd_app.disable_csv_logging(stream=stream)
        for stream in temp_app.get_supported_streams():
            temp_app.disable_csv_logging(stream=stream)
        for app in apps:
            app.disable_csv_logging()
        ppg_app.disable_csv_logging(stream=ppg_app.STREAM_PPG)
        ppg_app.disable_csv_logging(stream=ppg_app.STREAM_SYNC_PPG)
        ppg_app.disable_csv_logging(stream=ppg_app.STREAM_DYNAMIC_AGC)
        ppg_app.disable_csv_logging(stream=ppg_app.STREAM_HRV)
        pm_app.disable_csv_logging()

        # unsubscribing
        for app in apps:
            app._unsubscribe_stream_data()
        ppg_app._unsubscribe_stream_data(ppg_app.STREAM_PPG)
        ppg_app._unsubscribe_stream_data(ppg_app.STREAM_SYNC_PPG)
        ppg_app._unsubscribe_stream_data(ppg_app.STREAM_DYNAMIC_AGC)
        ppg_app._unsubscribe_stream_data(ppg_app.STREAM_HRV)
        pm_app._unsubscribe_stream_data(pm_app.STREAM_BATTERY)
        for stream in adpd_app.get_supported_streams():
            adpd_app._unsubscribe_stream_data(stream)
        for stream in temp_app.get_supported_streams():
            temp_app._unsubscribe_stream_data(stream)

        with open(f"{folder_name}/Summary.csv", 'w') as f:
            if info_result['key_value_pair']:
                f.write(f"Participant Information, {info_result['key_value_pair']['payload']['value_id']}" + "\n")
                # packet loss check
                SDK._packet_loss(f, "ADXL Packet loss", adxl_app.get_packet_lost_count())
                for i, stream in enumerate(adpd_app.get_supported_streams()):
                    if stream == adpd_app.STREAM_STATIC_AGC:
                        SDK._packet_loss(f, "STATIC AGC Packet loss", adpd_app.get_packet_lost_count(stream))
                    else:
                        adpd_lost_packets = adpd_app.get_packet_lost_count(stream)
                        if adpd_lost_packets:
                            SDK._packet_loss(f, f"ADPD{i + 1} CH1 Packet loss", adpd_lost_packets[0])
                            SDK._packet_loss(f, f"ADPD{i + 1} CH2 Packet loss", adpd_lost_packets[1])
                        else:
                            SDK._packet_loss(f, f"ADPD{i + 1} CH1 Packet loss", 0)
                            SDK._packet_loss(f, f"ADPD{i + 1} CH2 Packet loss", 0)
                for i, stream in enumerate(temp_app.get_supported_streams()):
                    SDK._packet_loss(f, f"Temperature{i + 1} Packet loss", temp_app.get_packet_lost_count(stream))

                SDK._packet_loss(f, "AD7156 Packet loss", ad7156_app.get_packet_lost_count())
                SDK._packet_loss(f, "ECG Packet loss", ecg_app.get_packet_lost_count())
                SDK._packet_loss(f, "EDA Packet loss", eda_app.get_packet_lost_count())
                SDK._packet_loss(f, "Pedometer Packet loss", ped_app.get_packet_lost_count())
                SDK._packet_loss(f, "PPG Packet loss", ppg_app.get_packet_lost_count(ppg_app.STREAM_PPG))
                SDK._packet_loss(f, "SYNC PPG Packet loss", ppg_app.get_packet_lost_count(ppg_app.STREAM_SYNC_PPG))
                SDK._packet_loss(f, "DYNAMIC AGC Packet loss",
                                 ppg_app.get_packet_lost_count(ppg_app.STREAM_DYNAMIC_AGC))
                SDK._packet_loss(f, "HRV Packet loss", ppg_app.get_packet_lost_count(ppg_app.STREAM_HRV))
                SDK._packet_loss(f, "SQI Packet loss", sqi_app.get_packet_lost_count())
                SDK._packet_loss(f, "BIA Packet loss", bia_app.get_packet_lost_count())

        with open(f"{folder_name}/Configuration.csv", 'w') as f:
            if info_result["adpd_dcfg"]:
                SDK._csv_write_config(f, info_result["adpd_dcfg"], "#ADPD_DCFG")
            if info_result["adxl_dcfg"]:
                SDK._csv_write_config(f, info_result["adxl_dcfg"], "#ADXL_DCFG")
            if info_result["ppg_lcfg"]:
                SDK._csv_write_config(f, info_result["ppg_lcfg"], "#PPG_LCFG")
            if info_result["ecg_lcfg"]:
                SDK._csv_write_config(f, info_result["ecg_lcfg"], "#ECG_LCFG")

        with open(f"{folder_name}/FirmwareVersion.csv", 'w') as f:
            if info_result["version"]:
                SDK._csv_write_version(f, info_result["version"], "PM Firmware Version")
            if info_result["ppg_algo_version"]:
                SDK._csv_write_version(f, info_result["ppg_algo_version"], "PPG Firmware Version")
            if info_result["ped_algo_version"]:
                SDK._csv_write_version(f, info_result["ped_algo_version"], "PED Firmware Version")
            if info_result["ecg_algo_version"]:
                SDK._csv_write_version(f, info_result["ecg_algo_version"], "ECG Firmware Version")
            if info_result["sqi_algo_version"]:
                SDK._csv_write_version(f, info_result["sqi_algo_version"], "SQI Firmware Version")

        with open(f"{folder_name}/PSBoardInfo.csv", 'w') as f:
            if info_result["system_info"]:
                config = info_result["system_info"]
                f.write(f"Module, PS Board Info\n")
                f.write(f"Version, {config['payload']['version']}\n")
                f.write(f"MAC address, {config['payload']['mac_address']}\n")
                f.write(f"Device ID, {config['payload']['device_id']}\n")
                f.write(f"Model number, {config['payload']['model_number']}\n")
                f.write(f"Hardware ID, {config['payload']['hw_id']}\n")
                f.write(f"BOM ID, {config['payload']['bom_id']}\n")
                f.write(f"Batch ID, {config['payload']['batch_id']}\n")
                f.write(f"Board Type, {config['payload']['board_type']}\n")

        # combining adpd csv
        adpd_csv_files = []
        for i in range(1, 13):
            adpd_file = f"{folder_name}/adpd{i}.csv"
            if os.path.exists(adpd_file):
                adpd_csv_files.append(adpd_file)
        if len(adpd_csv_files):
            SDK.join_csv(*adpd_csv_files, output_filename=f"{folder_name}/adpd_streams.csv",
                         display_progress=display_progress, progress_callback=progress_callback)

        # cleanup
        del adpd_app
        del temp_app
        for _ in apps:
            del _
        del ppg_app
        del pm_app
        del packet_manager

    def disconnect(self):
        """disconnect SDK"""
        logger.debug("----- Study Watch SDK Stopped -----")
        if self._mac_address:
            self._ble_manager.disconnect()
        self._packet_manager.close()
        time.sleep(1)
