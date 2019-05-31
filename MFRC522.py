import spidev
from gpiozero import DigitalOutputDevice

# MFRC522 library for RC522 type boards using SPI interface
# Designed for Raspberry Pi, but should work with another SPI interface on other systems (because why the fuck not)
# something else idk


class MFRC522:
    spi = spidev.SpiDev()  # SPI object which will be used to talk to the MFRC522
    rst = DigitalOutputDevice()

    def __init__(self, bus, device):
        self.spi.open(bus,device)
        self.spi.max_speed_hz = 500000  # 500kHz for safety but I believe the MFRC522 can do much better
        self.spi.mode = 0b00  # data valid on rising edge, I think clock idles low
        self.spi.lsbfirst = 0  # MSB transmitted first

    def mfrc_read(self, address): # provide only a single address
        tosend = (address << 1) | 0x80  # MSB = 1 for reads, address shifted by one to the left
        received = self.spi.xfer2([tosend, 0x00])
        return received[1] # the data will appear on byte 2

    def mfrc_write(self, address, data):  # DO NOT (DO NOT!) use a list of addresses
        if (type(data) != list) || (type(data) != tuple):
            data = [data]
            self.spi.xfer2([address] + data)  # not much to do here, nothing to read back

    def start(self, reset_pin):
        self.rst = DigitalOutputDevice(reset_pin)
        self.rst.on()

        # TODO: look up relevant registers in the datasheet