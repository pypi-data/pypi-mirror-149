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
import tblock.exceptions
from tblock.config import create_dirs
from tblock.compat import init_db
import os
import unittest
import shutil
import subprocess
import sys
import requests
import time
from nose.tools import raises

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
REAL_REPO = tblock.REPO_MIRRORS
tblock.config.Var.REPO_MIRRORS = ["http://0.0.0.0:17213/index.json"]


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


def _start_server(port: int = None):
    # Start a basic HTTP server for syncing the filter list repository
    if not port:
        port = "17213"
    else:
        port = str(port)
    prc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "--bind", "0.0.0.0", "-d", os.path.join(os.path.dirname(__file__), "srv"),
         port],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait until the HTTP server is started
    while True:
        try:
            requests.get("http://0.0.0.0:" + port)
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
            continue
        else:
            break
    return prc


class TestFilters(unittest.TestCase):

    def test_sync_repo_local_server(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        _filter = tblock.Filter("tblock-base")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing),
            (True, True, False)
        )
        prc.kill()

    def test_sync_repo_local_server_custom_conflict(self):
        _create_env()
        tblock.subscribe_custom(["test-list", os.path.join(os.path.dirname(__file__), "srv", "test-list.txt")],
                                do_not_prompt=True, quiet=True)
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        _filter = tblock.Filter("test-list")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing),
            (True, False, True)
        )
        prc.kill()

    def test_sync_repo_local_server_custom_conflict_resync(self):
        _create_env()
        tblock.subscribe_custom(["test-list", os.path.join(os.path.dirname(__file__), "srv", "test-list.txt")],
                                do_not_prompt=True, quiet=True)
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.unsubscribe(["test-list"], do_not_prompt=True, quiet=True)
        tblock.sync_filter_list_repo(quiet=True)
        _filter = tblock.Filter("test-list")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing),
            (False, False, False)
        )
        prc.kill()

    def test_sync_repo_local_server_custom_conflict_resync_force(self):
        _create_env()
        tblock.subscribe_custom(["test-list", os.path.join(os.path.dirname(__file__), "srv", "test-list.txt")],
                                do_not_prompt=True, quiet=True)
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.unsubscribe(["test-list"], do_not_prompt=True, quiet=True)
        tblock.sync_filter_list_repo(quiet=True, force=True)
        _filter = tblock.Filter("test-list")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing),
            (True, True, False)
        )
        prc.kill()

    def test_subscribe_local_server(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list")
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id,
             tblock.Rule("tblock.codeberg.page").exists),
            (True, True, True, True, tblock.BLOCK, _filter.id, False)
        )
        prc.kill()

    @raises(tblock.exceptions.FilterError)
    def test_subscribe_unknown_id(self):
        _create_env()
        tblock.subscribe(["unknown-id"], do_not_prompt=True, quiet=True)

    def test_subscribe_mod_local_server(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True,
                         permissions=tblock.FilterPermissions(tblock.ALLOW + tblock.BLOCK))
        _filter = tblock.Filter("test-list")
        _rule = tblock.Rule("example.com")
        _rule_allow = tblock.Rule("tblock.codeberg.page")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id,
             _rule_allow.exists, _rule_allow.policy, _rule_allow.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id, True, tblock.ALLOW, _filter.id)
        )
        prc.kill()

    def test_unsubscribe_local_server(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        tblock.unsubscribe(["test-list"], quiet=True, do_not_prompt=True)
        _filter = tblock.Filter("test-list")
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists),
            (True, True, False, False)
        )
        prc.kill()

    def test_mod_local_server(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        tblock.change_permissions(["test-list"], tblock.FilterPermissions(tblock.ALLOW + tblock.BLOCK),
                                  quiet=True, do_not_prompt=True)
        _filter = tblock.Filter("test-list")
        _rule = tblock.Rule("example.com")
        _rule_allow = tblock.Rule("tblock.codeberg.page")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id,
             _rule_allow.exists, _rule_allow.policy, _rule_allow.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id, True, tblock.ALLOW, _filter.id)
        )
        prc.kill()

    def test_update_local_server(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        tblock.update(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list")
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id)
        )
        prc.kill()

    def test_update_local_server_cache(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        prc.kill()
        # Wait until the HTTP server is shut down
        while True:
            try:
                requests.get(tblock.config.Var.REPO_MIRRORS[0])
            except requests.exceptions.ConnectionError:
                break
            else:
                time.sleep(0.5)
                continue
        tblock.update(["test-list"], do_not_prompt=True, quiet=True)
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id)
        )

    def test_update_local_server_mirror_xz(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        prc.kill()
        # Wait until the HTTP server is shut down
        while True:
            try:
                requests.get(tblock.config.Var.REPO_MIRRORS[0])
            except requests.exceptions.ConnectionError:
                break
            else:
                time.sleep(0.5)
                continue
        # Remove cached filter list
        os.remove(os.path.join(tblock.Path.CACHE, "test-list"))
        prc = _start_server(17214)
        tblock.update(["test-list"], do_not_prompt=True, quiet=True)
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id)
        )
        prc.kill()

    def test_update_local_server_mirror_gzip(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        prc.kill()
        # Wait until the HTTP server is shut down
        while True:
            try:
                requests.get(tblock.config.Var.REPO_MIRRORS[0])
            except requests.exceptions.ConnectionError:
                break
            else:
                time.sleep(0.5)
                continue
        # Remove cached filter list
        os.remove(os.path.join(tblock.Path.CACHE, "test-list"))
        prc = _start_server(17215)
        tblock.update(["test-list"], do_not_prompt=True, quiet=True)
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id)
        )
        prc.kill()

    def test_update_local_server_mirror_no_compress(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        prc.kill()
        # Wait until the HTTP server is shut down
        while True:
            try:
                requests.get(tblock.config.Var.REPO_MIRRORS[0])
            except requests.exceptions.ConnectionError:
                break
            else:
                time.sleep(0.5)
                continue
        # Remove cached filter list
        os.remove(os.path.join(tblock.Path.CACHE, "test-list"))
        prc = _start_server(17216)
        tblock.update(["test-list"], do_not_prompt=True, quiet=True)
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id)
        )
        prc.kill()

    @raises(tblock.exceptions.FilterError)
    def test_update_local_server_no_cache(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        _filter.delete_cache()
        prc.kill()
        # Wait until the HTTP server is shut down
        while True:
            try:
                requests.get(tblock.config.Var.REPO_MIRRORS[0])
            except requests.exceptions.ConnectionError:
                break
            else:
                time.sleep(0.5)
                continue
        tblock.update(["test-list"], do_not_prompt=True, quiet=True)

    def test_update_all(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        tblock.update_all(quiet=True, do_not_prompt=True)
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id),
            (True, True, True, True, tblock.BLOCK, _filter.id)
        )
        prc.kill()

    def test_update_all_blacklist(self):
        _create_env()
        prc = _start_server()
        tblock.sync_filter_list_repo(quiet=True)
        tblock.subscribe(["test-list"], do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-list", quiet=True)
        _filter.delete_all_rules()
        tblock.update_all(quiet=True, do_not_prompt=True, blacklist=["test-list"])
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists),
            (True, True, True, False)
        )
        prc.kill()

    def test_add_custom(self):
        _create_env()
        tblock.subscribe_custom(["test-custom", os.path.join(os.path.dirname(__file__), "srv", "test-list.txt")],
                                do_not_prompt=True, quiet=True)
        _filter = tblock.Filter("test-custom")
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id,
             tblock.Rule("tblock.codeberg.page").exists),
            (True, False, True, True, tblock.BLOCK, _filter.id, False)
        )

    @raises(tblock.exceptions.FilterError)
    def test_add_custom_file_not_found(self):
        _create_env()
        tblock.subscribe_custom(["file-not-found", os.path.join(os.path.dirname(__file__), "srv", "file_not_found.txt")],
                                do_not_prompt=True, quiet=True)

    def test_add_mod_custom(self):
        _create_env()
        tblock.subscribe_custom(["test-custom", os.path.join(os.path.dirname(__file__), "srv", "test-list.txt")],
                                do_not_prompt=True, quiet=True,
                                permissions=tblock.FilterPermissions(tblock.ALLOW + tblock.BLOCK))
        _filter = tblock.Filter("test-custom")
        _rule = tblock.Rule("example.com")
        _rule_allow = tblock.Rule("tblock.codeberg.page")
        self.assertEqual(
            (_filter.exists, _filter.on_repo, _filter.subscribing, _rule.exists, _rule.policy, _rule.filter_id,
             _rule_allow.exists, _rule_allow.policy, _rule_allow.filter_id),
            (True, False, True, True, tblock.BLOCK, _filter.id, True, tblock.ALLOW, _filter.id)
        )

    def test_remove_custom(self):
        _create_env()
        tblock.subscribe_custom(["test-custom", os.path.join(os.path.dirname(__file__), "srv", "test-list.txt")],
                                do_not_prompt=True, quiet=True)
        tblock.unsubscribe(["test-custom"], quiet=True, do_not_prompt=True)
        _filter = tblock.Filter("test-custom")
        _rule = tblock.Rule("example.com")
        self.assertEqual(
            (_filter.exists, _rule.exists),
            (False, False)
        )

    @raises(tblock.exceptions.FilterError)
    def test_remove_custom_not_exists(self):
        _create_env()
        tblock.unsubscribe(["test-custom"], quiet=True, do_not_prompt=True)


if __name__ == "__main__":
    unittest.main()
