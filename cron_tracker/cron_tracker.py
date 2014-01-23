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
from crontab import CronTab
from time import sleep

class CronListener:

    def __init__(self):
        # Parse Arguments
        parser = argparse.ArgumentParser(description="Crontab Tracking Tool")

        parser.add_argument("-f", metavar='FILE', dest="password_file", type=file, default="/etc/passwd",
            help="Password file to use.")

        parser.add_argument("-s", metavar='SLEEP TIME', dest="sleep_time", type=int, default=30,
            help="Time to sleep between checking cron tabs.")

        try:
            args = parser.parse_args()
        except IOError, e:
            print "There was a File IO error:\n{}".format(e)
            exit(0)

        # Process Tabs
        existing_tabs = {}

        while True:

            users = self.read_usernames(args.password_file)

            # Print and update system tabs
            current_system_tabs = self.retrieve_system_crontab()
            existing_system_tabs = set()

            self.print_changed_tabs('SYSTEM', current_system_tabs, existing_system_tabs)

            existing_tabs['SYSTEM'] = current_system_tabs

            # Print and update user tabs
            for user in users:
                current_user_tabs = self.retrieve_user_crontab(user)
                existing_user_tabs = set()

                if user in existing_tabs:
                    existing_user_tabs = existing_tabs[user]

                self.print_changed_tabs(user, existing_user_tabs, current_user_tabs)

                existing_tabs[user] = current_user_tabs

            print "-"*30
            sleep(args.sleep_time)

    def read_usernames(self, password_file):
        """Read a list of usernames from the passwd file in Linux."""
        usernames = set()

        # Add each user on the system to an array
        for line in password_file:
            usernames.add(line.split(":")[0])

        return usernames

    def retrieve_system_crontab(self):
        """Retrieve the jobs in the system crontab."""
        jobs = set()
        system_tab = CronTab()

        for job in system_tab:
            if not str(job).startswith("#"):
                jobs.add(str(job))

        return jobs

    def retrieve_user_crontab(self, username):
        """Retrieve the jobs in a users crontab."""
        jobs = set()
        user_tab = CronTab(username)

        for job in user_tab:
            if not str(job).startswith("#"):
                jobs.add(str(job))

        return jobs

    def print_changed_tabs(self, username, existing_tabs, current_tabs):
        """Print the cron jobs that have changed since previous execution."""
        change_tabs = current_tabs - existing_tabs

        if change_tabs:
            print "New tabs for {}".format(username)

            for tab in change_tabs:
                print tab


if __name__ == '__main__':
    CronListener()