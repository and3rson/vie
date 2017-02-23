#!/usr/bin/env python2

from vie import VIE


def main():
    vie = VIE()

    # vie.force_device('FC:A8:9A:55:66:A8')
    vie.force_device('FC:A8:9A:80:9D:72')
    # vie.find_device()

    vie.connect()

    vie.set_led_color(VIE.LEDColor.RED)
    vie.set_eq([6, 0, -6])
    # vie.set_eq([-6, 0, 6], [VIE.EqBand1.FREQ_125_HZ, VIE.EqBand2.FREQ_250_HZ, VIE.EqBand3.FREQ_16_KHZ])


if __name__ == '__main__':
    main()
