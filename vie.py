import bluetooth
from gattlib import GATTRequester


class DeviceException(Exception):
    pass


class Device(object):
    """
    Abstract device.
    """
    def __init__(self):
        self.addr = None
        self.adapter = ''

    def find_device(self):
        self.addr = None

        for addr, name in bluetooth.discover_devices(lookup_names=True):
            if name == 'VIE SHAIR':
                self.addr = addr

        if self.addr is None:
            raise DeviceException('No matching devices found.')

    def force_device(self, addr):
        self.addr = addr

    def connect(self):
        self.req = GATTRequester(self.addr)

    def get_req(self):
        return self.req


class VIE(Device):
    """
    VIE SHAIR device.
    """
    HANDLE = 0x000E

    class LEDColor:
        """
        LED color values;
        """
        RED = '\x00'
        GREEN = '\x01'
        BLUE = '\x02'
        YELLOW = '\x03'
        WHITE = '\x04'

    class EqBand1:
        """
        Frequencies for the first equalizer band.
        """
        FREQ_60_HZ = '\x00'
        FREQ_95_HZ = '\x01'
        FREQ_125_HZ = '\x02'

    class EqBand2:
        """
        Frequencies for the second equalizer band.
        """
        FREQ_250_HZ = '\x03'
        FREQ_500_HZ = '\x04'
        FREQ_1_KHZ = '\x05'
        FREQ_2_KHZ = '\x06'

    class EqBand3:
        """
        Frequencies for the third equalizer band.
        """
        FREQ_3_KHZ = '\x07'
        FREQ_6_KHZ = '\x08'
        FREQ_16_KHZ = '\x09'

    def set_led_color(self, color):
        """
        Sets LED color. `color` values are specified in the LEDColor subclass.
        """
        self.get_req().write_by_handle(VIE.HANDLE, '\xE1\x01' + color)

    def set_eq(self, gains, freqs=[EqBand1.FREQ_60_HZ, EqBand2.FREQ_500_HZ, EqBand3.FREQ_6_KHZ]):
        """
        Sets equalizer values.
        `gains` is a list of 3 band values in range [-6, 6]
        `freqs` are equalizer bands. Allowed values are specified in the LEDColor subclass. They default to 60 Hz, 500 Hz and 6 KHz.
        """
        for i in xrange(0, 3):
            assert -6 <= gains[i] <= 6
        gains = map(lambda x: x + 6, gains)
        self.get_req().write_by_handle(VIE.HANDLE, '\xE2\x06' + str(
            bytearray(freqs) + bytearray(gains)
        ))
