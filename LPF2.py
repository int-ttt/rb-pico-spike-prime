from machine import UART, Pin
import math, utime
import ustruct as struct

CMD_MODES   = 0x51
CMD_SPEED   = 0x52
CMD_SELECT  = 0x43
CMD_WRITE   = 0x44
CMD_VERSION = 0x5f
CMD_Data    = 0xC0
CMD_TYPE    = 0x40
CMD_LLL_SHIFT = 3

INFO_NAME    = 0x00
INFO_RAW     = 0x01
INFO_PCT     = 0x02
INFO_SI      = 0x03
INFO_UNITS   = 0x04
INFO_MAPPING = 0x05
INFO_MODE_COMBOS = 0x06

length = {'Int8' : 1, 'uInt8' : 1, 'Int16' : 2, 'uInt16' : 2, 'Int32' : 4, 'uInt32' : 4, 'float' : 4}
format = {'Int8' : '<b', 'uInt8' : '<B', 'Int16' : '<h', 'uInt16' : '<H',
     'Int32' : '<l', 'uInt32' : '<L', 'float' : '<f'}

class LPF2:
    def __init__(self, modes, txPin = 1, rxPin = 0, baud=115200, type = 65):
        self.modes = modes
        self.type = type
        self.txPin = txPin
        self.rxPin = rxPin
        self.tx = Pin(txPin, Pin.OUT)
        self.rx = Pin(rxPin, Pin.IN)
        self.baud = baud
        self.ser = UART(1, baud, tx=self.tx, rx=self.rx)
        self.connected = False

    def sendData(self, type, data, mode):
        if isinstance(data, list):
            bit = math.floor(math.log2(length[type] * len(data)))
            bit = 4 if bit > 4 else bit  # max 16 bytes total (4 floats)
            array = data[:math.floor((2 ** bit) / length[type])]  # max array size is 16 bytes
            value = b''
            for element in array:
                value += struct.pack(format[type], element)
        else:
            bit = int(math.log2(length[type]))
            value = struct.pack(format[type], data)
        payload = bytearray([CMD_Data | (bit << CMD_LLL_SHIFT) | mode]) + value
        self.write(payload)

    def write(self, payload):
        self.ser.write(payload)

    def setupMode(self, mode, num):
        self.writeIt(self.padString(mode[0], num, NAME))  # write name
        self.writeIt(self.buildRange(mode[2], num, RAW))  # write RAW range
        self.writeIt(self.buildRange(mode[3], num, Pct))  # write Percent range
        self.writeIt(self.buildRange(mode[4], num, SI))  # write SI range
        self.writeIt(self.padString(mode[5], num, SYM))  # write symbol
        self.writeIt(self.buildFunctMap(mode[6], num, FCT))  # write Function Map
        self.writeIt(self.buildFormat(mode[1], num, FMT))  # write format

    def initialize(self):
        self.connected = False
        self.tx = Pin(self.txPin, Pin.OUT)
        self.rx = Pin(self.rxPin, Pin.IN)
        self.tx.value(0)
        utime.sleep_ms(500)
        self.tx.value(1)
        self.ser.init(self.baud)

        self.write(b'\x00')