import csv
import math
import logging
import time
from datetime import datetime

from ..core.enums.common_enums import Stream

logger = logging.getLogger(__name__)


class CSVLogger:
    def __init__(self, filename, header, write_header=True):
        self.ch1 = []
        self.ch2 = []
        self.file = None
        self.ch1_dark = []
        self.ch2_dark = []
        self.ch1_time = []
        self.ch2_time = []
        self.writer = None
        self.header = header
        self.filename = filename
        self.logging_started = None
        self.write_header = write_header

    def write_row(self, row):
        if self.writer:
            self.writer.writerow(row)

    def start_logging(self, last_timestamp):
        try:
            self.file = open(self.filename, 'w', newline="")
            self.writer = csv.writer(self.file, quoting=csv.QUOTE_NONE)
            dt_object = datetime.fromtimestamp(last_timestamp)
            is_dst = time.daylight and time.localtime().tm_isdst > 0
            utc_offset = - (time.altzone if is_dst else time.timezone)
            self.write_row(["Local: ", dt_object, "tz_sec ", utc_offset])
            self.write_row(["Linux Epoch (ms):", last_timestamp * 1000])
            if self.write_header:
                self.write_row(self.header)
        except Exception as e:
            logger.error(f"Error while opening the {self.filename} file, reason :: {e}.", exc_info=True)

    def stop_logging(self):
        data_len = max(len(self.ch1_time), len(self.ch2_time))
        if len(self.ch1_time) > 0 and len(self.ch2_time) > 0:
            if not len(self.ch1_time) == len(self.ch2_time):
                data_len = min(len(self.ch1_time), len(self.ch2_time))
                logger.warning(f"Issue with ADPD CSV logging. Recommended sequence unsubscribe_stream "
                               f"then disable_csv_logging.")
        for i in range(data_len):
            if len(self.ch2) == 0:
                self.adpd_add_row([self.ch1_time[i], self.ch1_dark[i], self.ch1[i]], 1)
            elif len(self.ch1) == 0:
                self.adpd_add_row([self.ch2_time[i], self.ch2_dark[i], self.ch2[i]], 2)
            else:
                self.adpd_add_row(
                    [self.ch1_time[i], self.ch1_dark[i], self.ch1[i], self.ch2_dark[i], self.ch2[i]], 0)

        if self.file:
            self.file.close()

    def add_row(self, result, last_timestamp):
        stream = result["header"]["source"]
        if self.logging_started is None:
            self.logging_started = True
            self.start_logging(last_timestamp)
        if stream == Stream.ADXL:
            self._adxl_callback(result)
        elif stream in [Stream.ADPD1, Stream.ADPD2, Stream.ADPD3, Stream.ADPD4, Stream.ADPD5, Stream.ADPD6,
                        Stream.ADPD7, Stream.ADPD8, Stream.ADPD9, Stream.ADPD10, Stream.ADPD11, Stream.ADPD12]:
            self._adpd_callback(result)
        elif stream == Stream.PPG:
            self._ppg_callback(result)
        elif stream == Stream.SYNC_PPG:
            self._syncppg_callback(result)
        elif stream == Stream.ECG:
            self._ecg_callback(result)
        elif stream == Stream.EDA:
            self._eda_callback(result)
        elif stream in [Stream.TEMPERATURE1, Stream.TEMPERATURE2, Stream.TEMPERATURE3,
                        Stream.TEMPERATURE4, Stream.TEMPERATURE5, Stream.TEMPERATURE6, Stream.TEMPERATURE7,
                        Stream.TEMPERATURE8, Stream.TEMPERATURE9, Stream.TEMPERATURE10,
                        Stream.TEMPERATURE11, Stream.TEMPERATURE12]:
            self._temp_callback(result)
        elif stream == Stream.PEDOMETER:
            self._ped_callback(result)
        elif stream == Stream.BIA:
            self._bia_callback(result)
        elif stream == Stream.SQI:
            self._sqi_callback(result)
        elif stream == Stream.BATTERY:
            self._battery_callback(result)
        elif stream in [Stream.STATIC_AGC_STREAM, Stream.DYNAMIC_AGC_STREAM]:
            self._agc_callback(result)
        elif stream == Stream.HRV:
            self._hrv_callback(result)
        elif stream == Stream.AD7156:
            self._ad7156_callback(result)

    def adpd_add_row(self, row, header_format):
        if not self.write_header:
            self.write_header = True
            self.write_row([" ", self.header[0], "", "", "", ""])
            row2 = []
            if header_format == 0:
                row2 = [" ", "CH1", "", "", "CH2", ""]
            elif header_format == 1:
                row2 = [" ", "CH1", "", ""]
            elif header_format == 2:
                row2 = [" ", "CH2", "", ""]
            self.write_row(row2)
            row3 = []
            if header_format == 0:
                row3 = [" ", "Timestamp", "D1", "S1", "D2", "S2"]
            elif header_format == 1:
                row3 = [" ", "Timestamp", "D1", "S1"]
            elif header_format == 2:
                row3 = [" ", "Timestamp", "D2", "S2"]
            self.write_row(row3)
        self.write_row([" "] + row)

    def _adxl_callback(self, data):
        for value in data["payload"]["stream_data"]:
            self.write_row([value["timestamp"], value["x"], value["y"], value["z"]])

    def _adpd_callback(self, data):
        if len(self.ch1_time) > 200 or len(self.ch2_time) > 200:
            adpd_data_length = len(data["payload"]["signal_data"])
            for i in range(adpd_data_length):
                if len(self.ch2) == 0:
                    self.adpd_add_row([self.ch1_time[i], self.ch1_dark[i], self.ch1[i]], 1)
                elif len(self.ch1) == 0:
                    self.adpd_add_row([self.ch2_time[i], self.ch2_dark[i], self.ch2[i]], 2)
                else:
                    self.adpd_add_row(
                        [self.ch1_time[i], self.ch1_dark[i], self.ch1[i], self.ch2_dark[i], self.ch2[i]], 0)

            del self.ch1[:adpd_data_length]
            del self.ch2[:adpd_data_length]
            del self.ch1_dark[:adpd_data_length]
            del self.ch2_dark[:adpd_data_length]
            del self.ch1_time[:adpd_data_length]
            del self.ch2_time[:adpd_data_length]

        if data["payload"]["channel_num"] == 1:
            for signal_data in data["payload"]["signal_data"]:
                self.ch1_time.append(data["payload"]["timestamp"])
                self.ch1.append(signal_data)
            for dark_data in data["payload"]["dark_data"]:
                self.ch1_dark.append(dark_data)

        elif data["payload"]["channel_num"] == 2:
            for adpd_data in data["payload"]["signal_data"]:
                self.ch2_time.append(data["payload"]["timestamp"])
                self.ch2.append(adpd_data)
            for dark_data in data["payload"]["dark_data"]:
                self.ch2_dark.append(dark_data)

    def _ecg_callback(self, data):
        for value in data["payload"]["stream_data"]:
            self.write_row([value["timestamp"], data["payload"]["sequence_number"], value["ecg_data"]])

    def _ppg_callback(self, data):
        hr = float(data["payload"]["hr"]) / float(16)
        confidence = (float(100) * (data["payload"]["confidence"] / float(1024)))
        self.write_row([data["payload"]["timestamp"], hr, confidence, data["payload"]["hr_type"]])

    def _syncppg_callback(self, data):
        for value in data["payload"]["stream_data"]:
            self.write_row(
                [value["ppg_timestamp"], value["ppg_data"], value["adxl_timestamp"], value["adxl_x"],
                 value["adxl_y"], value["adxl_z"]])

    def _eda_callback(self, data):
        for value in data["payload"]["stream_data"]:
            eda_real = value["real"]
            eda_imaginary = value["imaginary"]
            if eda_real == 0:
                eda_real = 1
            impedance_img = eda_imaginary * 1000
            impedance_real = eda_real * 1000
            real_and_img = float(impedance_real * impedance_real + impedance_img * impedance_img)
            impedance_module = math.sqrt(real_and_img)
            impedance_phase = math.atan2(impedance_img, impedance_real)
            admittance_real = float(impedance_real /
                                    float(impedance_real * impedance_real + impedance_img * impedance_img))
            admittance_img = -float(impedance_img /
                                    float(impedance_real * impedance_real + impedance_img * impedance_img))
            admittance_module = 1 / impedance_module
            admittance_phase = math.atan2(admittance_img, admittance_real)

            self.write_row([
                value["timestamp"], impedance_real, impedance_img, impedance_module, impedance_phase, admittance_real,
                admittance_img, admittance_module, admittance_phase, data["payload"]["sequence_number"]
            ])

    def _temp_callback(self, data):
        self.write_row([data["payload"]["timestamp"], data["payload"]["skin_temperature"],
                        data["payload"]["impedance"], data["payload"]["compensated_temperature"]])

    def _ped_callback(self, data):
        self.write_row([data["payload"]["timestamp"], data["payload"]["steps"]])

    def _bia_callback(self, data):
        for value in data["payload"]["stream_data"]:
            bcm_real = value["real"]
            bcm_imaginary = value["imaginary"]
            if bcm_real == 0:
                bcm_real = 1
            if bcm_imaginary == 0:
                bcm_imaginary = 1
            impedance_img = bcm_imaginary / 1000
            impedance_real = bcm_real / 1000
            real_and_img = float(impedance_real * impedance_real + impedance_img * impedance_img)
            impedance_module = math.sqrt(real_and_img)
            impedance_phase = math.atan2(impedance_img, impedance_real)
            admittance_real = float(impedance_real /
                                    float(impedance_real * impedance_real + impedance_img * impedance_img))
            admittance_img = -float(impedance_img /
                                    float(impedance_real * impedance_real + impedance_img * impedance_img))
            admittance_module = 1 / impedance_module
            admittance_phase = math.atan2(admittance_img, admittance_real)
            self.write_row([
                value["timestamp"], impedance_real, impedance_img, impedance_module, impedance_phase,
                admittance_real, admittance_img, admittance_module, admittance_phase,
                data["payload"]["sequence_number"], value["frequency_index"]
            ])

    def _sqi_callback(self, data):
        self.write_row([data["payload"]["timestamp"], data["payload"]["sqi"]])

    def _battery_callback(self, data):
        self.write_row([data["payload"]["timestamp"], data["payload"]["battery_status"],
                        data["payload"]["battery_level"], data["payload"]["battery_mv"]])

    def _agc_callback(self, data):
        self.write_row([data["payload"]["timestamp"], *data["payload"]["mts"], *data["payload"]["setting"]])

    def _hrv_callback(self, data):
        for value in data["payload"]["stream_data"]:
            self.write_row([value["timestamp"], value["rr_interval"], value["is_gap"], value["rmssd"]])

    def _ad7156_callback(self, data):
        self.write_row([data["payload"]["timestamp"], data["payload"]["ch1_cap"], data["payload"]["ch2_cap"]])
