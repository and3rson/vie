# vie

A Python library for controlling VIE SHAIR headphones.

# requirements

- `pybluez` - for device discovery
- `gattlib` - for ATT support

# example

```python
# Create VIE instance
vie = VIE()

# You can find the device automatically (may be slow):
vie.find_device()
# OR provide a MAC address manually (faster)
vie.force_device('FC:A8:9A:80:9D:72')

# Connect to the device
vie.connect()

# Set LED color
vie.set_led_color(VIE.LEDColor.RED)
vie.set_led_color(VIE.LEDColor.GREEN)
vie.set_led_color(VIE.LEDColor.BLUE)
vie.set_led_color(VIE.LEDColor.YELLOW)
vie.set_led_color(VIE.LEDColor.WHITE)

# Set equalizer values with default bands (60 Hz, 500 Hz & 6 KHz)
vie.set_eq([6, 0, -6])
# OR set equalizer values with custom bands (e. g. 125 Hz, 250 Hz & 16 KHz)
vie.set_eq([-6, 0, 6], [VIE.EqBand1.FREQ_125_HZ, VIE.EqBand2.FREQ_250_HZ, VIE.EqBand3.FREQ_16_KHZ])

```

# about

All values used here were reverse-engineered from
an Android app source code & Bluetooth snooping log.

Reversed & written by Andrew Dunai.

The license is MIT.

# contribution

I'm open to ideas, suggestions & contributions.
