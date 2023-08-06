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

import tblock.converter
import unittest
import os

ADBLOCKPLUS_FILE = os.path.join(os.path.dirname(__file__), "templates", "adblockplus.txt")
HOSTS_FILE = os.path.join(os.path.dirname(__file__), "templates", "hosts.txt")
DNSMASQ_FILE = os.path.join(os.path.dirname(__file__), "templates", "dnsmasq.conf")
LIST_FILE = os.path.join(os.path.dirname(__file__), "templates", "list.txt")
TBLOCK_FILE = os.path.join(os.path.dirname(__file__), "templates", "tblock.txt")


class TestDetectSyntax(unittest.TestCase):

    def test_detect_adblockplus(self):
        with open(ADBLOCKPLUS_FILE, "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.ADBLOCKPLUS
            )

    def test_detect_hosts(self):
        with open(HOSTS_FILE, "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.HOSTS
            )

    def test_detect_dnsmasq(self):
        with open(DNSMASQ_FILE, "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.DNSMASQ
            )

    def test_detect_list(self):
        with open(LIST_FILE, "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.LIST
            )

    def test_detect_tblock(self):
        with open(TBLOCK_FILE, "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.TBLOCK
            )


class TestFilterListConvert(unittest.TestCase):

    def test_convert_adblockplus_adblockplus(self):
        tblock.converter.convert(ADBLOCKPLUS_FILE, ADBLOCKPLUS_FILE + ".out", tblock.converter.ADBLOCKPLUS, quiet=True)
        with open(ADBLOCKPLUS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.ADBLOCKPLUS
            )
        os.remove(ADBLOCKPLUS_FILE + ".out")

    def test_convert_adblockplus_hosts(self):
        tblock.converter.convert(ADBLOCKPLUS_FILE, ADBLOCKPLUS_FILE + ".out", tblock.converter.HOSTS, quiet=True)
        with open(ADBLOCKPLUS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.HOSTS
            )
        os.remove(ADBLOCKPLUS_FILE + ".out")

    def test_convert_adblockplus_dnsmasq(self):
        tblock.converter.convert(ADBLOCKPLUS_FILE, ADBLOCKPLUS_FILE + ".out", tblock.converter.DNSMASQ, quiet=True)
        with open(ADBLOCKPLUS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.DNSMASQ
            )
        os.remove(ADBLOCKPLUS_FILE + ".out")

    def test_convert_adblockplus_list(self):
        tblock.converter.convert(ADBLOCKPLUS_FILE, ADBLOCKPLUS_FILE + ".out", tblock.converter.LIST, quiet=True)
        with open(ADBLOCKPLUS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.LIST
            )
        os.remove(ADBLOCKPLUS_FILE + ".out")

    def test_convert_adblockplus_tblock(self):
        tblock.converter.convert(ADBLOCKPLUS_FILE, ADBLOCKPLUS_FILE + ".out", tblock.converter.TBLOCK, quiet=True)
        with open(ADBLOCKPLUS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.TBLOCK
            )
        os.remove(ADBLOCKPLUS_FILE + ".out")

    def test_convert_hosts_adblockplus(self):
        tblock.converter.convert(HOSTS_FILE, HOSTS_FILE + ".out", tblock.converter.ADBLOCKPLUS, quiet=True)
        with open(HOSTS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.ADBLOCKPLUS
            )
        os.remove(HOSTS_FILE + ".out")

    def test_convert_hosts_hosts(self):
        tblock.converter.convert(HOSTS_FILE, HOSTS_FILE + ".out", tblock.converter.HOSTS, quiet=True)
        with open(HOSTS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.HOSTS
            )
        os.remove(HOSTS_FILE + ".out")

    def test_convert_hosts_dnsmasq(self):
        tblock.converter.convert(HOSTS_FILE, HOSTS_FILE + ".out", tblock.converter.DNSMASQ, quiet=True)
        with open(HOSTS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.DNSMASQ
            )
        os.remove(HOSTS_FILE + ".out")

    def test_convert_hosts_list(self):
        tblock.converter.convert(HOSTS_FILE, HOSTS_FILE + ".out", tblock.converter.LIST, quiet=True)
        with open(HOSTS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.LIST
            )
        os.remove(HOSTS_FILE + ".out")

    def test_convert_hosts_tblock(self):
        tblock.converter.convert(HOSTS_FILE, HOSTS_FILE + ".out", tblock.converter.TBLOCK, quiet=True)
        with open(HOSTS_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.TBLOCK
            )
        os.remove(HOSTS_FILE + ".out")

    def test_convert_dnsmasq_adblockplus(self):
        tblock.converter.convert(DNSMASQ_FILE, DNSMASQ_FILE + ".out", tblock.converter.ADBLOCKPLUS, quiet=True)
        with open(DNSMASQ_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.ADBLOCKPLUS
            )
        os.remove(DNSMASQ_FILE + ".out")

    def test_convert_dnsmasq_hosts(self):
        tblock.converter.convert(DNSMASQ_FILE, DNSMASQ_FILE + ".out", tblock.converter.HOSTS, quiet=True)
        with open(DNSMASQ_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.HOSTS
            )
        os.remove(DNSMASQ_FILE + ".out")

    def test_convert_dnsmasq_dnsmasq(self):
        tblock.converter.convert(DNSMASQ_FILE, DNSMASQ_FILE + ".out", tblock.converter.DNSMASQ, quiet=True)
        with open(DNSMASQ_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.DNSMASQ
            )
        os.remove(DNSMASQ_FILE + ".out")

    def test_convert_dnsmasq_list(self):
        tblock.converter.convert(DNSMASQ_FILE, DNSMASQ_FILE + ".out", tblock.converter.LIST, quiet=True)
        with open(DNSMASQ_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.LIST
            )
        os.remove(DNSMASQ_FILE + ".out")

    def test_convert_dnsmasq_tblock(self):
        tblock.converter.convert(DNSMASQ_FILE, DNSMASQ_FILE + ".out", tblock.converter.TBLOCK, quiet=True)
        with open(DNSMASQ_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.TBLOCK
            )
        os.remove(DNSMASQ_FILE + ".out")

    def test_convert_list_adblockplus(self):
        tblock.converter.convert(LIST_FILE, LIST_FILE + ".out", tblock.converter.ADBLOCKPLUS, quiet=True)
        with open(LIST_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.ADBLOCKPLUS
            )
        os.remove(LIST_FILE + ".out")

    def test_convert_list_hosts(self):
        tblock.converter.convert(LIST_FILE, LIST_FILE + ".out", tblock.converter.HOSTS, quiet=True)
        with open(LIST_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.HOSTS
            )
        os.remove(LIST_FILE + ".out")

    def test_convert_list_dnsmasq(self):
        tblock.converter.convert(LIST_FILE, LIST_FILE + ".out", tblock.converter.DNSMASQ, quiet=True)
        with open(LIST_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.DNSMASQ
            )
        os.remove(LIST_FILE + ".out")

    def test_convert_list_list(self):
        tblock.converter.convert(LIST_FILE, LIST_FILE + ".out", tblock.converter.LIST, quiet=True)
        with open(LIST_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.LIST
            )
        os.remove(LIST_FILE + ".out")

    def test_convert_list_tblock(self):
        tblock.converter.convert(LIST_FILE, LIST_FILE + ".out", tblock.converter.TBLOCK, quiet=True)
        with open(LIST_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.TBLOCK
            )
        os.remove(LIST_FILE + ".out")

    def test_convert_tblock_adblockplus(self):
        tblock.converter.convert(TBLOCK_FILE, TBLOCK_FILE + ".out", tblock.converter.ADBLOCKPLUS, quiet=True)
        with open(TBLOCK_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.ADBLOCKPLUS
            )
        os.remove(TBLOCK_FILE + ".out")

    def test_convert_tblock_hosts(self):
        tblock.converter.convert(TBLOCK_FILE, TBLOCK_FILE + ".out", tblock.converter.HOSTS, quiet=True)
        with open(TBLOCK_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.HOSTS
            )
        os.remove(TBLOCK_FILE + ".out")

    def test_convert_tblock_dnsmasq(self):
        tblock.converter.convert(TBLOCK_FILE, TBLOCK_FILE + ".out", tblock.converter.DNSMASQ, quiet=True)
        with open(TBLOCK_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.DNSMASQ
            )
        os.remove(TBLOCK_FILE + ".out")

    def test_convert_tblock_list(self):
        tblock.converter.convert(TBLOCK_FILE, TBLOCK_FILE + ".out", tblock.converter.LIST, quiet=True)
        with open(TBLOCK_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.LIST
            )
        os.remove(TBLOCK_FILE + ".out")

    def test_convert_tblock_tblock(self):
        tblock.converter.convert(TBLOCK_FILE, TBLOCK_FILE + ".out", tblock.converter.TBLOCK, quiet=True)
        with open(TBLOCK_FILE + ".out", "rt") as r:
            self.assertEqual(
                tblock.converter.detect_syntax(r.readlines()),
                tblock.converter.TBLOCK
            )
        os.remove(TBLOCK_FILE + ".out")


if __name__ == "__main__":
    unittest.main()
