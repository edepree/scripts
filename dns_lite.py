#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author::     Eric DePree, James Espinosa
# Copyright::  Copyright (c) 2014
# License::    GPLv2

import sys
import signal
import struct
import logging
import argparse

from socket import *

class Server:
    def run_server(self, port):

        address = "localhost"

        # Create a communication socket
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind((address, port))

        logging.debug("Server bound to [{}] on port [{}]".format(address, port))

        while True:
            # Receive data from the client
            data, addr = s.recvfrom(4096)

            # Print client's message for debugging purposes
            logging.debug("Server received [{}]".format(data))

            # Decode request
            # unpackedDNS = struct.unpack('>HH' , data)
            # print unpackedDNS

            # Strcuture reply

            # Send the message back to the client
            # s.sendto(data, addr)

if __name__ == '__main__':
    # Command Line Arguments
    parser = argparse.ArgumentParser(description="DNS Server")

    parser.add_argument("-p", dest="port", type=int, default=53, help="Port Number [Default: 53]")
    parser.add_argument('-v', dest="verbosity", action='count', default=0, help="Increase verboseness of logging.")

    args = parser.parse_args()

    # Instantiate Logger
    logLevel = 40

    if args.verbosity == 1:
        logLevel = 30
    elif args.verbosity == 2:
        logLevel = 20
    elif args.verbosity == 3 or args.verbosity > 3:
        logLevel = 10

    logging.basicConfig(format="%(asctime)-19s %(levelname)-8s %(message)s", datefmt='%Y-%m-%d %H:%M:%S', level=logLevel)

    # Caputre SIGINT
    signal.signal(signal.SIGINT, lambda x,y: exit(-1))

    # Launch server
    logging.debug("Launching Server")
    server = Server()
    server.run_server(args.port)