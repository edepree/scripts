#!/usr/bin/env python
#
# Copyright (C) 2013 Eric DePree
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
# Copyright::  Copyright (c) 2013
# License::    GPLv2

"""connection_tracker.py: netstat monitoring tool."""

__author__ = "Eric DePree"
__copyright__ = "Copyright 2013, Eric DePree"
__version__ = "1.0"

# ---------- SYSTEM IMPORTS ----------
import argparse
import cPickle
import curses
import operator
import signal
from subprocess import check_output
from threading import Thread
from time import sleep
from Queue import Queue


class ConnectionTracker:
    """Class for user input and user display."""
    # Connections
    trackedConnections = {}

    # Command Line Arguments
    args = None

    # Drawing Variables
    startingLine = 5
    endingLine = startingLine
    selectedLine = None
    selectedLineConnection = None

    def __init__(self):
        """Set up program and run in infinite loop"""
        self.args = self.read_arguments()

        __ignoredConnections = []
        __connectionsToIgnore = []

        # Set up screen/curses arguments
        __screen = curses.initscr()
        __screen.keypad(True)
        __screen.nodelay(True)
        __screen.scrollok(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.curs_set(0)

        __thread = NetstatParser(self.args.frequency)
        __thread.daemon = True
        __thread.start()

        while True:
            # Where there is an update from the thread capture it and reset variables
            if not NetstatParser.trackedConnections.empty():
                self.trackedConnections = NetstatParser.trackedConnections.get_nowait()
                __ignoredConnections = NetstatParser.connectionsToIgnore.get_nowait()
                self.selectedLine = self.startingLine
                __connectionsToIgnore = []
                self.display_data(self.args.frequency,  __screen, self.trackedConnections, __ignoredConnections,
                                  __connectionsToIgnore, self.startingLine, self.selectedLine)

            # Capture user data
            userInput = __screen.getch()
            if userInput == curses.KEY_UP and self.selectedLine > self.startingLine:
                self.selectedLine -= 1
                self.display_data(self.args.frequency,  __screen, self.trackedConnections, __ignoredConnections,
                                  __connectionsToIgnore, self.startingLine, self.selectedLine)
            elif userInput == curses.KEY_DOWN and self.selectedLine < self.endingLine - 1:
                self.selectedLine += 1
                self.display_data(self.args.frequency,  __screen, self.trackedConnections, __ignoredConnections,
                                  __connectionsToIgnore, self.startingLine, self.selectedLine)
            elif userInput == curses.KEY_RIGHT:
                __connectionsToIgnore.append(self.selectedLineConnection)
                NetstatParser.trackedConnectionsIgnored.put(self.selectedLineConnection)
                self.display_data(self.args.frequency,  __screen, self.trackedConnections, __ignoredConnections,
                                  __connectionsToIgnore, self.startingLine, self.selectedLine)
            elif userInput == curses.KEY_RESIZE:
                self.display_data(self.args.frequency,  __screen, self.trackedConnections, __ignoredConnections,
                                  __connectionsToIgnore, self.startingLine, self.selectedLine)

            sleep(0.01)

    def saving_handler(self, signal, frame):
        """Dump data to disk."""
        cPickle.dump(self.trackedConnections, self.args.outfile)
        exit(0)

    def read_arguments(self):
        """Load arguments from the command line and perform assorted tasks related to the optional switches."""
        parser = argparse.ArgumentParser(description="A netstat monitoring tool. KEYPAD_UP/DOWN: Move between rows.\n" +
                                                     "KEYPAD_RIGHT: Mark a connection to be ignored on update.\n")
        parser.add_argument("-u", dest="frequency", type=int, default=15,
                            help="How often to query netstat, in seconds (default: 15)")
        parser.add_argument("-s", metavar='FILE', dest="outfile", type=argparse.FileType('w'),
                            help="Save data to a file on SIGINT")
        parser.add_argument("-l", metavar='FILE', dest="infile", type=file,
                            help="Load a previous file save")

        try:
            args = parser.parse_args()
        except IOError, e:
            print "There was a File IO error:\n{}".format(e)
            exit(0)

        # ---------- OPTIONAL ARUMENTS ----------
        if(args.outfile is not None):
            signal.signal(signal.SIGINT, self.saving_handler)

        if(args.infile is not None):
            NetstatParser.trackedConnections.put(cPickle.load(args.infile))

        return args

    def display_data(self, frequency, screen, trackedConnections, ignoredConnections,
                     connectionsToIgnore, startingLine, selectedLine):
        """Output the data to the terminal"""

        screen.clear()
        screen.addstr("Connection Tracker\n", curses.A_STANDOUT)
        screen.addstr("Update Interval: {} seconds\n\n".format(frequency))
        screen.addstr("{:<8} {:>21} {:>21} {:>12} {:>9}\n".format(
                      "PROTOCOL", "LOCAL ADDRESS", "FOREGIN ADDRESS", "STATE", "TIME"), curses.A_BOLD)

        # Display tracked connections
        location = startingLine
        for connection, count in sorted(trackedConnections.iteritems(), key=operator.itemgetter(1)):

            if(location == selectedLine):
                self.selectedLineConnection = connection

            splitConnection = connection.split("|")
            connectionTime = (count-1) * frequency

            if location == selectedLine:
                (self.output_formatted_tracked_connection(splitConnection[0], splitConnection[1],
                 splitConnection[2], splitConnection[3], screen, connectionTime, curses.A_UNDERLINE))
            elif connection in connectionsToIgnore:
                (self.output_formatted_tracked_connection(splitConnection[0], splitConnection[1],
                 splitConnection[2], splitConnection[3], screen, connectionTime, curses.A_STANDOUT))
            elif connectionTime > 60:
                (self.output_formatted_tracked_connection(splitConnection[0], splitConnection[1],
                 splitConnection[2], splitConnection[3], screen, connectionTime, curses.color_pair(1)))
            else:
                (self.output_tracked_connection(splitConnection[0], splitConnection[1],
                 splitConnection[2], splitConnection[3], screen, connectionTime))

            location += 1

        self.endingLine = location

        screen.addstr("\nIGNORED CONNECTIONS\n\n", curses.A_BOLD)

        # Display ignored connections
        for ignoredConnection in ignoredConnections:
            splitIgnoredConnection = ignoredConnection.split("|")

            self.output_ignored_connection(splitIgnoredConnection[0], splitIgnoredConnection[1],
                                           splitIgnoredConnection[2], splitIgnoredConnection[3], screen)

        screen.refresh()

    def output_tracked_connection(self, protocol, localIp, foreginIp, state, screen, time):
        """Output a connection to the screen."""
        screen.addstr("{:<8} {:>21} {:>21} {:>12} {:>5} sec\n".format(protocol, localIp, foreginIp, state, time))

    def output_formatted_tracked_connection(self, protocol, localIp, foreginIp, state, screen, time, option):
        """Output a formatted connection to the screen."""
        screen.addstr("{:<8} {:>21} {:>21} {:>12} {:>5} sec\n".format(protocol, localIp, foreginIp, state, time), option)

    def output_ignored_connection(self, protocol, localIp, foreginIp, state, screen):
        """Output a connection to the screen without seconds tracking."""
        screen.addstr("{:<8} {:>21} {:>21} {:>12}\n".format(protocol, localIp, foreginIp, state))

    def revert_screen(self):
        """Revert the changes curses made to the screen."""
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __del__(self):
        """Revert curses changes on delete."""
        self.revert_screen()


class NetstatParser(Thread):
    """Worker thread class for processing netstat updates."""
    trackedConnections = Queue()
    trackedConnectionsIgnored = Queue()
    connectionsToIgnore = Queue()

    connections = {}
    connectionKeys = None
    updateFrequency = None
    ignoredConnections = []

    def __init__(self, updateFrequency):
        """Retrieve any initial netstat data."""
        super(NetstatParser, self).__init__()

        if not self.trackedConnections.empty():
            self.connections = self.trackedConnections.get_nowait()

        self.connectionKeys = self.connections.keys()
        self.updateFrequency = updateFrequency

    def run(self):
        """The thread will run until killed by parent"""
        while True:
            while not self.trackedConnectionsIgnored.empty():
                self.ignoredConnections.append(self.trackedConnectionsIgnored.get_nowait())

            self.trackedConnections.put(self.update_netstat_data())
            self.connectionsToIgnore.put(self.ignoredConnections)
            sleep(self.updateFrequency)

    def update_netstat_data(self):
        """Build a dictionary of the connection returned by netstat."""
        lineCounter = 2
        updatedConnections = {}

        # Get data from system
        netstatOutput = check_output(["netstat", "-tuan"]).split("\n")

        # Update/Build list of open connections
        while lineCounter < len(netstatOutput) - 1:

            splitLine = netstatOutput[lineCounter].split()
            lineCounter += 1

            connection = "{}|{}|{}|".format(splitLine[0], splitLine[3], splitLine[4])

            # Add the state of the connection if it's TCP; otherwise nothing for UDP
            if len(splitLine) > 5:
                connection += splitLine[5]
            else:
                connection += ""

            # Increment the life of the connection or add a new one
            if(connection in self.ignoredConnections):
                pass
            elif(connection in self.connectionKeys):
                count = self.connections[connection]
                updatedConnections[connection] = count + 1
            else:
                updatedConnections[connection] = 1

        self.connectionKeys = updatedConnections.keys()
        self.connections = updatedConnections

        return updatedConnections

if __name__ == '__main__':
    """Main Method"""
    ConnectionTracker()
