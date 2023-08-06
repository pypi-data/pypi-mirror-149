from enum import Enum, unique

from .. import utils


@unique
class User0Command(Enum):
    """
    User0 Command Enum
    """
    LOWEST = [0x40]
    SET_STATE_REQ = [0x42]
    SET_STATE_RES = [0x43]
    GET_STATE_REQ = [0x44]
    GET_STATE_RES = [0x45]
    ID_OP_REQ = [0x46]
    ID_OP_RES = [0x47]
    CLEAR_PREV_ST_EVT_REQ = [0x48]
    CLEAR_PREV_ST_EVT_RES = [0x49]
    GET_PREV_ST_EVT_REQ = [0x4A]
    GET_PREV_ST_EVT_RES = [0x4B]
    BYPASS_USER0_TIMINGS_REQ = [0x4C]
    BYPASS_USER0_TIMINGS_RES = [0x4D]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class User0Status(Enum):
    """
    User0 status Enum
    """
    LOWEST = [0x40]
    OK = [0x41]
    ERR_ARGS = [0x42]
    ERR_NOT_CHKD = [0xFF]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class User0State(Enum):
    """
    User0 status Enum
    """
    ADMIT_STANDBY = [0x0]
    START_MONITORING = [0x1]
    SLEEP = [0x2]
    INTERMITTENT_MONITORING = [0x3]
    INTERMITTENT_MONITORING_START_LOG = [0x4]
    INTERMITTENT_MONITORING_STOP_LOG = [0x5]
    END_MONITORING = [0x6]
    CHARGING_BATTERY = [0x7]
    OUT_OF_BATTERY_STATE_BEFORE_START_MONITORING = [0x8]
    OUT_OF_BATTERY_STATE_DURING_INTERMITTENT_MONITORING = [0x9]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class User0Event(Enum):
    """
    User0 event Enum
    """
    INVALID = [0x0]
    NAV_BUTTON_RESET = [0x1]
    WATCH_ON_CRADLE_NAV_BUTTON_RESET = [0x2]
    BATTERY_DRAINED = [0x3]
    BLE_DISCONNECT_UNEXPECTED = [0x4]
    BLE_DISCONNECT_NW_TERMINATED = [0x5]
    RTC_TIMER_INTERRUPT = [0x6]
    BLE_ADV_TIMEOUT = [0x7]
    USB_DISCONNECT_UNEXPECTED = [0x8]
    BATTERY_FULL = [0x9]
    FINISH_LOG_TRANSFER = [0xA]
    SYS_RST_M2M2_COMMAND = [0xB]
    SYS_HW_RST_M2M2_COMMAND = [0xC]
    SET_USER0_STATE_M2M2_COMMAND = [0xD]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class User0ID(Enum):
    """
    User0 ID Enum
    """
    HW_ID = [0x0]
    EXP_ID = [0x1]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class User0OperationMode(Enum):
    """
    User0 operation Enum
    """
    READ = [0x0]
    WRITE = [0x1]
    DELETE = [0x2]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))
