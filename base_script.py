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
# Author::     AUTHOR
# Copyright::  Copyright (c) YEAR
# License::    GPLv2

# IMPORTS
import signal
import logging
import argparse

# GLOBAL VARIABLES
args = None


if __name__ == '__main__':
    # Command line arguments
    parser = argparse.ArgumentParser(description="Simple HTTP(S) server that accepts POST requests.")

    parser.add_argument("-v", dest="verbosity", action="store_true", help="Increase Verboseness of Logging.")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(format="%(asctime)-19s %(levelname)-8s %(message)s",
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=10 if args.verbosity else 20)

    # Capture SIGINT
    signal.signal(signal.SIGINT, lambda x, y: exit(-1))
