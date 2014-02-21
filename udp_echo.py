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
# Author::     Eric DePree
# Copyright::  Copyright (c) 2014
# License::    GPLv2

import sys
import signal
import logging
import argparse

from socket import *

class Server:
    def run_server(self, address, port, buffer):
        """Run the echo server till it's terminated"""

        # Create a communication socket
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind((address, port))

        logging.debug("Server bound to [{}] on port [{}]".format(address, port))

        while True:
            # Receive data from the client
            data, addr = s.recvfrom(buffer)

            # Print client's message for debugging purposes
            logging.debug("Server received [{}] from [{}]".format(data, addr))

            # Send the message back to the client
            s.sendto(data, addr)

class Client:
    def run_client(self, address, port, buffer):
        """Run the echo client till it's terminated"""

        logging.debug("Client connecting to [{}] on port [{}]".format(address, port))

        # Create a communication socket
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(("", 0))

        while True:
            # Read the users input from the terminal and strip any whitespace
            clientInput  = sys.stdin.readline()
            clientInput = clientInput.strip()

            if clientInput:
                # Send user input to the server
                s.sendto(clientInput, (address, port))

                # Retrieve server's response
                data, addr = s.recvfrom(buffer)
                data = data.strip()

                logging.debug("Client received [{}] from [{}]".format(data, addr))
                print(data)

if __name__ == '__main__':
    # Command Line Arguments
    parser = argparse.ArgumentParser(description="UDP Echo Client/Server")

    parser.add_argument("-a", dest="address", default="localhost", help="Address [Default: localhost]")
    parser.add_argument("-p", dest="port", type=int, default=5000, help="Port Number [Default: 5000]")
    parser.add_argument("-b", dest="buffer", type=int, default=4096, help="Buffer Size [Default: 4096]")
    parser.add_argument('-v', dest="verbosity", action='count', default=0, help="Increase verboseness of logging.")
    parser.add_argument("mode", help="Specify if this the the 'client' or 'server'")

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

    # Launch appropriate server or client
    if args.mode.lower() == "client":
        logging.debug("Launching Client")
        serverclient = Client()
        serverclient.run_client(args.address, args.port, args.buffer)
    elif args.mode.lower() == "server":
        logging.debug("Launching Server")
        server = Server()
        server.run_server(args.address, args.port, args.buffer)
    else:
        logging.error("The mode of [{}] is undefined".format(args.mode))