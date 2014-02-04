#!/usr/bin/env python
#
# Copyright (C) 2014 Eric DePree
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

"""cron_tracker.py: Crontab Tracking Tool."""

# ---------- SYSTEM IMPORTS ----------
import argparse
import curses
import datetime
import logging
import signal

from subprocess import check_output, CalledProcessError, STDOUT
from time import sleep

class CronListener:

    parser = None
    command_line_arguments = None
    screen = None

    def __init__(self):
        self.command_line_arguments = self.parse_arguments()
        signal.signal(signal.SIGINT, self.exit_handler)

        logging.basicConfig(filename=self.command_line_arguments.log, level=logging.ERROR)
        self.parser = CronParser()

    def parse_arguments(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description="Crontab Tracking Tool. This program needs to be run " +
            "with with elevated permissions to access all the crontabs")

        parser.add_argument("-f", metavar="FILE", dest="password_file", type=file, default="/etc/passwd",
            help="Password file to use.")

        parser.add_argument("-s", metavar="SLEEP TIME", dest="sleep_time", type=int, default=30,
            help="Time to sleep between checking crontabs.")

        parser.add_argument("-l", metavar="LOG LOCATION", dest="log", default="/tmp/cron_tracker.log",
            help="Log location for application.")

        try:
            args = parser.parse_args()
            return args
        except IOError, e:
            print "There was a File IO error:\n{}".format(e)
            exit(0)

    def monitor_tabs(self, screen):
        """Main flow for the application."""
        existing_tabs = {}
        self.screen = screen

        self.screen.scrollok(True)

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.screen.addstr("Connection Tracker\n", curses.A_STANDOUT)

        while True:
            self.screen.addstr("\nRefreshed at {}\n".format(datetime.datetime.now()), curses.color_pair(2))

            users = self.read_usernames(self.command_line_arguments.password_file)

            # Print and update system tabs
            current_system_tabs = self.retrieve_crontab("SYSTEM")
            existing_system_tabs = set()

            self.print_changed_tabs("SYSTEM", current_system_tabs, existing_system_tabs)

            existing_tabs["SYSTEM"] = current_system_tabs

            # Print and update user tabs
            for user in users:
                current_user_tabs = self.retrieve_crontab(user)
                existing_user_tabs = set()

                if user in existing_tabs:
                    existing_user_tabs = existing_tabs[user]

                self.print_changed_tabs(user, existing_user_tabs, current_user_tabs)

                existing_tabs[user] = current_user_tabs

            screen.refresh()
            sleep(self.command_line_arguments.sleep_time)

    def read_usernames(self, password_file):
        """Read a list of usernames from the passwd file in Linux."""
        usernames = set()

        # Add each user on the system to an array
        for line in password_file:
            usernames.add(line.split(":")[0])

        logging.info(usernames)

        return usernames

    def retrieve_crontab(self, username):
        """Retrieve the jobs in a users crontab."""
        jobs = set()

        if username == "SYSTEM":
            tab = set()
        else:
            tab = self.parser.get_user_tab(username)

        if tab:
            for job in tab:
                if str(job).strip() and not str(job).startswith("#"):
                    jobs.add(str(job))

        return jobs

    def print_changed_tabs(self, username, existing_tabs, current_tabs):
        """Print the cron jobs that have changed since previous execution."""
        change_tabs = current_tabs - existing_tabs

        if change_tabs:
            self.screen.addstr("User: {}\n".format(username), curses.color_pair(1))

            for tab in change_tabs:
                self.screen.addstr("{}\n".format(tab))

    def exit_handler(self, signal, frame):
        """Override for keyboard interrupts to suppress stack track to terminal."""
        exit(-1)


class CronParser:
    """Parsere for reading crontabs."""
    def get_system_tab(self):
        """Read in the system crontab."""
        None

    def get_user_tab(self, username):
        """Read in a user's crontab using system commands."""
        try:
            cmnd_output = check_output(["crontab", "-l", "-u", username], stderr=STDOUT);
            return cmnd_output.split("\n")
        except CalledProcessError as exc:
            if not 'no crontab for' in exc.output:
                logging.critical(exc.output)


if __name__ == '__main__':
    listener = CronListener()
    curses.wrapper(listener.monitor_tabs)