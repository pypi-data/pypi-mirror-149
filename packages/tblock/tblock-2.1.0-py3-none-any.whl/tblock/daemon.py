# -*- coding: utf-8 -*-
#   _____ ____  _            _
#  |_   _| __ )| | ___   ___| | __
#    | | |  _ \| |/ _ \ / __| |/ /
#    | | | |_) | | (_) | (__|   <
#    |_| |____/|_|\___/ \___|_|\_\
#
# An anti-capitalist ad-blocker that uses the hosts file
# Copyright (C) 2021-2022 Twann <tw4nn@disroot.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Standard modules
import os
import time
import signal
import configparser

# Local modules
from .filters import update_all
from .config import load_config, log_message, Path, hosts_are_safe, hosts_are_default
from .style import Font
from .utils import check_root_access, unlock_db, lock_db
from .hosts import update_hosts
from .exceptions import RepoError, FilterError, TBlockError, DatabaseLockedError


class SignalHandler:
    """
    Handler for SIGTERM and SIGINT
    """

    stopped = False
    signame = None

    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint)
        signal.signal(signal.SIGTERM, self.sigterm)

    def sigint(self, *args):
        self.stopped = True
        self.signame = "SIGINT"

    def sigterm(self, *args):
        self.stopped = True
        self.signame = "SIGTERM"


def start_daemon(config: str, no_pid: bool = False) -> None:
    """
    Start the daemon

    :param config: Path to the config file to use
    :param no_pid: Optional. Do not create a PID file (False by default)
    """
    # Check root access
    if not check_root_access():
        raise PermissionError("you need to run as root to perform this operation")
    if not os.path.isfile(config):
        raise FileNotFoundError("config file not found: {0}".format(config))
    try:
        daemon_config = load_config(config)
    except KeyError:
        raise TBlockError("invalid config file: {0}".format(config))
    if os.path.isfile(Path.DAEMON_PID) and not no_pid:
        with open(Path.DAEMON_PID, "rt") as f:
            if not int(f.read()) == os.getpid():
                log_message("[tblockd] ERROR: an instance of the daemon is already running")
                raise TBlockError(
                    "an instance of the daemon is already running. Try to run with the --no-pid option")
    else:
        if not no_pid:
            with open(Path.DAEMON_PID, "wt") as w:
                w.write(str(os.getpid()))
        try:
            frequency = daemon_config.getint("daemon", "frequency")
            # Prevent the frequency from being set to a value lower than one hour
            if frequency < 60:
                frequency = 60
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            frequency = 240
        try:
            sync_repo = daemon_config.getboolean("daemon", "sync_repo")
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            sync_repo = True
        try:
            anti_hijack = daemon_config.getboolean("daemon", "anti_hijack")
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            anti_hijack = True
        try:
            force = daemon_config.getboolean("daemon", "force")
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            force = False

        log_message("[tblockd] INFO:  config loaded; PID: {0}; launching updater now".format(os.getpid()))
        updater(sync_repo=sync_repo, frequency=frequency, do_not_remove_pid=no_pid, anti_hijack=anti_hijack,
                force=force)


def launch_anti_hijack():
    if not hosts_are_safe() and not hosts_are_default():
        print(f'{Font.BOLD}==> Hosts file hijack detected{Font.DEFAULT}')
        update_hosts(do_not_prompt=True)
        log_message("[tblockd] WARN:  hosts hijack was detected; hosts file was updated")


def updater(sync_repo: bool = False, frequency: int = 60, do_not_remove_pid: bool = False,
            anti_hijack: bool = True, force: bool = False) -> None:
    process = SignalHandler()
    while not process.stopped:
        try:
            # Lock the database
            lock_db()
        except DatabaseLockedError:
            # Wait one second before trying again and check for hosts hijack if enabled
            if process.stopped:
                break
            print(f'{Font.BOLD}==> Database locked, waiting for other instances to terminate{Font.DEFAULT}', end="\r")
            time.sleep(1)
            continue
        print(f'{Font.BOLD}==> Database locked, waiting for other instances to terminate{Font.DEFAULT}')
        log_message("[tblockd] INFO:  PID: {0}; updating filter lists now".format(os.getpid()))
        try:
            update_all(force=force, quiet=False, sync_repo=sync_repo, do_not_prompt=True, lock_database=False)
        except RepoError:
            try:
                update_all(force=force, quiet=False, sync_repo=False, do_not_prompt=True, lock_database=False)
            except FilterError:
                pass
        except FilterError:
            pass
        except FileNotFoundError as err:
            log_message("[tblockd] ERROR:  PID: {0}; caught FileNotFoundError: {1}".format(os.getpid(), err.__str__()))

        # Unlock the database
        unlock_db()

        log_message("[tblockd] INFO:  PID: {0}; operation was successful".format(os.getpid()))
        print(f'{Font.BOLD}==> Waiting {frequency} minute(s) until next update...{Font.DEFAULT}')
        x = 1
        while x <= frequency * 60:
            if process.stopped:
                break
            elif x % 60 and anti_hijack:
                launch_anti_hijack()
            time.sleep(1)
            x += 1
    else:
        if not do_not_remove_pid:
            os.remove(Path.DAEMON_PID)
        log_message("[tblockd] INFO:  caught {0}; PID: {1}; stopping now".format(process.signame, os.getpid()))
