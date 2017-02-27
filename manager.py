#!/usr/bin/env python2

# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk
import gtk
import gobject
import sys
from vie import VIE
from threading import Thread, Lock

gobject.threads_init()

class App(gtk.Window):
    def __init__(self):
        super(App, self).__init__()
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.set_title('VIE SHAIR')
        self.connect('destroy', gtk.main_quit)

        self.vie = VIE()

        self._is_busy = False
        self._lock = Lock()

        self._init_gui()

    def _init_gui(self):
        self.layout = gtk.VBox()
        self.add(self.layout)

        self.bands_box = gtk.HBox()
        self.bands_box.set_size_request(-1, 128)
        self.layout.pack_start(self.bands_box, True, True)

        self.band1 = self._create_band_slider(self._on_band_change)
        self.bands_box.pack_start(self.band1)

        self.band2 = self._create_band_slider(self._on_band_change)
        self.bands_box.pack_start(self.band2)

        self.band3 = self._create_band_slider(self._on_band_change)
        self.bands_box.pack_start(self.band3)

        self.colors_box = gtk.HBox()
        self.layout.pack_start(self.colors_box, False, True)
        for color_name, color_code in (
            ('RED', '#FF5555'),
            ('GREEN', '#55FF55'),
            ('BLUE', '#5555FF'),
            ('YELLOW', '#FFFF55'),
            ('WHITE', '#FFFFFF')
        ):
            color_btn = gtk.Button(color_name[0])
            for state in (gtk.STATE_NORMAL, gtk.STATE_ACTIVE, gtk.STATE_PRELIGHT, gtk.STATE_SELECTED, gtk.STATE_INSENSITIVE):
                color_btn.modify_bg(state, gtk.gdk.color_parse(color_code))
                color_btn.modify_fg(state, gtk.gdk.color_parse('#000000'))
                color_btn.color_id = getattr(VIE.LEDColor, color_name)
            color_btn.connect('clicked', lambda btn: Thread(target=self._set_led_color, args=(btn.color_id,)).start())
            self.colors_box.pack_start(color_btn, True, True)

        self.status_box = gtk.HBox()
        self.layout.pack_start(self.status_box, False, True)

        self.status_label = gtk.Label('...')
        self.status_box.pack_start(self.status_label)

        self._update_gui()

    def _create_band_slider(self, on_change):
        band = gtk.VScale(gtk.Adjustment(0, -6, 7, 1, 1, 1))
        band.set_inverted(True)
        band.connect('value-changed', on_change)
        for i in xrange(-6, 7):
            band.add_mark(i, gtk.POS_RIGHT, None)
        return band


    def _on_band_change(self, band):
        v1, v2, v3 = map(int, (band.get_value() for band in (self.band1, self.band2, self.band3)))
        print [v1, v2, v3]
        Thread(target=self._set_eq, args=((v1, v2, v3),)).start()

    def _set_eq(self, freqs):
        self.lock_gui()
        print 'setting...'
        self.vie.set_eq(freqs)
        print 'set!'
        self.unlock_gui()

    def _set_led_color(self, color):
        self.lock_gui()
        print 'setting...'
        self.vie.set_led_color(color)
        print 'set!'
        self.unlock_gui()

    def start(self):
        self.vie.force_device(sys.argv[1])
        gobject.idle_add(self._connect_vie)

        self.show_all()
        gtk.main()

    def _connect_vie(self):
        def process():
            self.lock_gui()
            bands = self.vie.connect()
            self.band1.set_value(bands[0])
            self.band2.set_value(bands[1])
            self.band3.set_value(bands[2])
            print 'CONNECTED'
            self.unlock_gui()
#            self.vie.set_led_color(VIE.LEDColor.RED)
#            print 'SET'
#            print repr(self.vie.read())
            gobject.idle_add(self._update_gui)
        Thread(target=process).start()

    def _update_gui(self):
        if self._is_busy:
            self.status_label.set_text('In progress...')
            self.bands_box.set_sensitive(False)
            self.colors_box.set_sensitive(False)
        else:
            self.status_label.set_text('Ready')
            self.bands_box.set_sensitive(True)
            self.colors_box.set_sensitive(True)

    def lock_gui(self):
        self._lock.acquire()
        self._is_busy = True
        gobject.idle_add(self._update_gui)

    def unlock_gui(self):
        self._is_busy = False
        self._lock.release()
        gobject.idle_add(self._update_gui)

# vie = VIE()

def main():
    if len(sys.argv) != 2:
        print 'Usage: ./manager.py <MAC_ADDRESS>'
        sys.exit(1)
    app = App()
    app.start()


if __name__ == '__main__':
    main()
