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

import tblock
from tblock.config import create_dirs
from tblock.compat import init_db
import os
import unittest
import shutil

# Change PATH variables
__root__ = os.path.join(os.path.dirname(__file__), "fake_root")
__prefix__ = os.path.join(__root__, "usr", "lib")
tblock.config.Path.PREFIX = __prefix__
tblock.config.Path.CACHE = os.path.join(__root__, "var", "cache")
tblock.config.Path.CONFIG = os.path.join(__root__, "etc", "tblock.conf")
tblock.config.Path.DAEMON_PID = os.path.join(__root__, "run", "tblock.pid")
tblock.config.Path.DATABASE = os.path.join(__prefix__, "storage.sqlite")
tblock.config.Path.DB_LOCK = os.path.join(__prefix__, ".db_lock")
tblock.config.Path.HOSTS = os.path.join(__root__, "etc", "hosts")
tblock.config.Path.HOSTS_BACKUP = os.path.join(__prefix__, "hosts.bak")
tblock.config.Path.LOGS = os.path.join(__root__, "var", "log", "tblock.log")
tblock.config.Path.TMP_DIR = os.path.join(__root__, "tmp", "tblock")


def _create_env():
    # Remove data from previous tests
    if os.path.isdir(__root__):
        shutil.rmtree(__root__)
    # Setup new test environment
    os.mkdir(__root__)
    create_dirs()
    os.mkdir(os.path.join(__root__, "etc"))
    init_db(True)
    with open(tblock.Path.HOSTS, "wt") as h:
        h.close()


class TestRules(unittest.TestCase):

    def test_add_allow(self):
        _create_env()
        tblock.allow_domains(["example.com"], do_not_prompt=True, quiet=True, also_update_hosts=False)
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_rule.exists, _rule.policy),
            (True, tblock.ALLOW)
        )

    def test_add_block(self):
        _create_env()
        tblock.block_domains(["example.org"], do_not_prompt=True, quiet=True, also_update_hosts=False)
        _rule = tblock.Rule("example.org")
        self.assertEqual(
            (_rule.exists, _rule.policy),
            (True, tblock.BLOCK)
        )

    def test_add_redirect(self):
        _create_env()
        tblock.redirect_domains(["redirect.example.com"], ip="0.0.0.1",
                                do_not_prompt=True, quiet=True, also_update_hosts=False)
        _rule = tblock.Rule("redirect.example.com")
        self.assertEqual(
            (_rule.exists, _rule.policy, _rule.ip),
            (True, tblock.REDIRECT, "0.0.0.1")
        )

    def test_remove_existing(self):
        _create_env()
        tblock.block_domains(["block.example.org"], do_not_prompt=True, quiet=True, also_update_hosts=False)
        tblock.delete_rules(["block.example.org"], do_not_prompt=True, quiet=True, also_update_hosts=False)
        _rule = tblock.Rule("block.example.com")
        self.assertEqual(
            (_rule.exists,),
            (False,)
        )

    def test_remove_not_existing(self):
        _create_env()
        tblock.delete_rules(["not.example.org"], do_not_prompt=True, quiet=True, also_update_hosts=False)
        _rule = tblock.Rule("not.example.com")
        self.assertEqual(
            (_rule.exists,),
            (False,)
        )


if __name__ == "__main__":
    unittest.main()
