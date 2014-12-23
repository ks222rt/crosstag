# -*- coding: utf-8 -*-
import logging
import glob
import serial
import sys
from datetime import datetime
from optparse import OptionParser
import requests
import time


# TODO: 2014-11-29 lujo: Refactor this. All of it. Just get to it.
class CrosstagReader(object):
    def main(self, server, port):
        logging.basicConfig(filename='logs/reader.log', level=logging.DEBUG)
        logging.info("Attempting to set up the reader on: %s:%d" % (server, port))
        try:
            """
                ls /dev/serial/by-id/ to get all connected devices. Use that to determine this
                /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AD026CI5-if00-port0
            """
            usb_devices = glob.glob("/dev/serial/by-id/*")
            ser = serial.Serial(usb_devices[0], 9600, timeout=0)
            logging.info("Crosstag reader is up and running.")
            sys.stdout.flush()
        except:
            now = datetime.now()
            logging.error('%s reader ERROR unable to setup the RFID reade, is it plugged in?' % (now))
            sys.exit(-1)
        while True:
            if ser.inWaiting() > 0:
                data = ser.readline()
                if len(data) < 12:
                    continue
                now = datetime.datetime.now()
                ser.flushOutput()
                data = data.strip()
                tag_nbr = data[1:]
                if len(tag_nbr) != 12:
                    logging.error('%s reader ERROR [%s] is too long. len(tag_nbr): %d' % (now, tag_nbr, len(tag_nbr)))
                    # TODO, PiFace code to ask the person to tag again.
                    # audio signal and visual signal.
                    continue
                try:
                    print '%s reader tagging [%s]' % (now, tag_nbr)
                    res = requests.get("http://%s:%d/crosstag/v1.0/tagevent/%s" % (server, port, tag_nbr), timeout=3)
                    now = datetime.now()
                    logging.info("%s reader tagging result: [%s]" % (now, res.text))
                except:  # catch *all* exceptions
                    e = sys.exc_info()[0]
                    logging.error('%s reader failed (timeout?) to tag %s error: %s' % (now, tag_nbr, e))
            else:
                time.sleep(1)

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] arg \nTry this: python crosstag_reader.py", version="%prog 1.0")
    parser.add_option("-s", "--server",
                      action="store", type="string", dest="server", default="localhost", help="What is the URL to the crosstag server?")
    parser.add_option("-p", "--port",
                      action="store", type="int", dest="port", default=80, help="What is the port of the crosstag server?")
    (options, args) = parser.parse_args()
    r = CrosstagReader()
    r.main(options.server, options.port)
