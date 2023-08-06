from .command_packet import CommandPacket
from ..data_types.array import Array
from ..data_types.enums import Enums
from ..data_types.integer import Int
from ..enums.dcb_enums import DCBConfigBlockIndex


class TemperatureDCFGPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        [
            {
                'header': {
                    'source': <Application.TEMPERATURE: ['0xC3', '0x06']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 240,
                    'checksum': 0
                },
                'payload': {
                    'command': <CommonCommand.GET_DCFG_RES: ['0x26']>,
                    'status': <CommonStatus.OK: ['0x00']>,
                    'size': 57,
                    'packet_count': 2,
                    'data': [
                        [ 9, 151 ],
                        [ 11, 738 ],
                        ...
                        [ 421, 5 ],
                        [ 422, 0 ]
                    ]
                }
            },
            {
                'header': {
                    'source': <Application.TEMPERATURE: ['0xC3', '0x06']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 240,
                    'checksum': 0
                },
                'payload': {
                    'command': <CommonCommand.GET_DCFG_RES: ['0x26']>,
                    'status': <CommonStatus.OK: ['0x00']>,
                    'size': 10,
                    'packet_count': 2,
                    'data': [
                        [ 423, 288 ],
                        [ 424, 0 ],
                        ..
                        [ 431, 0 ],
                        [ 432, 4 ]
                    ]
                }
            }
        ]
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["packet_count"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=2, data_types=[Int(2), Int(2)], reverse_inner_array=True)


class TemperatureDCBPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        [
            {
                'header': {
                    'source': <Application.ADPD: ['0xC1', '0x10']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 242,
                    'checksum': 0
                },
                'payload': {
                    'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                    'status': <DCBStatus.OK: ['0x97']>,
                    'size': 57,
                    'packet_count': 2,
                    'data': [
                        [ '0x9', '0x97' ],
                        [ '0xB', '0x6E2' ],
                        ...
                        [ '0x1A5', '0x5' ],
                        [ '0x1A6', '0x0' ]
                    ]
                }
            },
            {
                'header': {
                    'source': <Application.ADPD: ['0xC1', '0x10']>,
                    'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                    'length': 242,
                    'checksum': 0
                },
                'payload': {
                    'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                    'status': <DCBStatus.OK: ['0x97']>,
                    'size': 10,
                    'packet_count': 2,
                    'data': [
                        [ '0x1A7', '0x120' ],
                        [ '0x1A8', '0x0' ],
                        ...
                        [ '0x1AF', '0x0' ],
                        [ '0x1B0', '0x4' ]
                    ]
                }
            }
        ]
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = Int(1)
        self._config["payload"]["packet_count"] = Int(2)
        self._config["payload"]["data"] = Array(-1, dimension=1, data_types=[Int(4, to_hex=True)])


class TemperatureDCBCommandPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.EDA: ['0xC3', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 20,
                'checksum': 0
            },
            'payload': {
                'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                'status': <DCBStatus.OK: ['0x97']>,
                'size': 1,
                'data': [
                    [ '0x0', '0x8' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["dcb_block_index"] = Enums(1, enum_class=DCBConfigBlockIndex,
                                                           default=DCBConfigBlockIndex.TEMPERATURE_BLOCK)


class TemperatureLibraryConfigPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PPG: ['0xC3', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': 16,
                'checksum': 0
            },
            'payload': {
                'command': <CommonCommand.READ_LCFG_RES: ['0x17']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'field': 1,
                'data': [
                    [ '0x0', '0xC0' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["field"] = Int(1)
        self._config["payload"]["data"] = Array(-1, dimension=1, data_types=[Int(4, to_hex=True)])
