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
import io
import re
import sqlite3

# Local modules
from .syntaxtools import detect_syntax, is_valid_rule, get_rule
from ..style import loading_icon, Icon, Font
from ..const import USER_RULE_PRIORITY, RulePolicy, TBlockSyntaxStatus, FilterSyntax, FilterPermissions, RULE_COMMENTS
from ..utils import contains_wildcards
from ..exceptions import FilterSyntaxError


ALL_SYNTAX = [FilterSyntax.ADBLOCKPLUS, FilterSyntax.DNSMASQ, FilterSyntax.HOSTS, FilterSyntax.LIST,
              FilterSyntax.TBLOCK]

ADBLOCKPLUS = FilterSyntax.ADBLOCKPLUS
DNSMASQ = FilterSyntax.DNSMASQ
HOSTS = FilterSyntax.HOSTS
LIST = FilterSyntax.LIST
TBLOCK = FilterSyntax.TBLOCK
UNKNOWN = FilterSyntax.UNKNOWN


class FilterParser:

    def __init__(self, local_file: str, syntax: str = None, quiet: bool = False) -> None:
        self.file = local_file
        self.quiet = quiet
        if syntax is None:
            try:
                with io.open(local_file, "rt") as f:
                    self.syntax = detect_syntax(f.readlines())
            except UnicodeDecodeError:
                raise FilterSyntaxError("unable to decode file: {0}".format(self.file))
            except PermissionError:
                raise FilterSyntaxError("unable to access file: {0}".format(self.file))
            except FileNotFoundError:
                raise FilterSyntaxError("file not found: {0}".format(self.file))
            except IsADirectoryError:
                raise FilterSyntaxError("is a directory: {0}".format(self.file))
        else:
            if syntax not in ALL_SYNTAX:
                raise FilterSyntaxError(
                    "invalid input syntax: {0}".format(syntax)
                )
            else:
                self.syntax = syntax

    def insert_rules_to_database(self, connection: sqlite3.Connection, filter_id: str,
                                 permissions: FilterPermissions) -> None:
        try:
            with io.open(self.file, "rt") as f:
                data = f.readlines()
        except UnicodeDecodeError:
            raise FilterSyntaxError("unable to decode file: {0}".format(self.file))
        except PermissionError:
            raise FilterSyntaxError("unable to access file: {0}".format(self.file))
        except FileNotFoundError:
            raise FilterSyntaxError("file not found: {0}".format(self.file))
        count = 0
        percent = 0
        all_rules_count = len(data)

        cursor = connection.cursor()

        wildcards = cursor.execute("SELECT domain FROM rules WHERE domain LIKE '%*%';").fetchall()

        # TBlock syntax support
        tblock_begin = False
        tblock_policy = None
        tblock_ip = None

        for line in data:

            count += 1
            percent = int(count * 100 / len(data))
            if not self.quiet:
                print(" {0} Inserting rules into database ({1}): {2}%".format(
                    loading_icon(count), all_rules_count, percent), end="\r")

            if is_valid_rule(line.split("\n")[0], self.syntax):
                if self.syntax == FilterSyntax.TBLOCK:
                    rule = get_rule(line.split("\n")[0], self.syntax, allow_comments=False, tblock_begin=tblock_begin,
                                    tblock_policy=tblock_policy, tblock_ip=tblock_ip, allow_allow=permissions.ALLOW,
                                    allow_block=permissions.BLOCK, allow_redirect=permissions.REDIRECT)
                else:
                    rule = get_rule(line.split("\n")[0], self.syntax, allow_comments=False,
                                    allow_allow=permissions.ALLOW, allow_block=permissions.BLOCK,
                                    allow_redirect=permissions.REDIRECT)

                if rule:
                    # Change the IP address if rule is a redirecting rule
                    if rule[1] == RulePolicy.REDIRECT:
                        ip = rule[2].compressed
                    else:
                        ip = None

                    # TBlock syntax support
                    if self.syntax == FilterSyntax.TBLOCK:
                        if rule[0] == TBlockSyntaxStatus.CURRENT_STATUS:
                            tblock_begin = rule[1]
                            continue
                        elif rule[0] == TBlockSyntaxStatus.CURRENT_POLICY:
                            tblock_policy = rule[1]
                            if tblock_policy == RulePolicy.REDIRECT:
                                tblock_ip = rule[2]
                            continue

                    domain = rule[0]
                    policy = rule[1]

                    # Check whether the rule already exists in the database
                    query = cursor.execute("SELECT domain, filter_id, policy FROM rules WHERE domain=?",
                                           (rule[0],)).fetchall()

                    # Check whether a wildcard rule already exists in the database

                    wildcards_exists = False
                    for rule in wildcards:
                        if re.match(re.compile(rule[0].replace(".", "\\.").replace("*", ".*")), domain):
                            wildcards_exists = True

                    if not wildcards_exists:
                        # Check if the rule exists and if the rule is not a user rule
                        if query and query[0][1] != USER_RULE_PRIORITY:
                            # Check if the local rule has a higher priority (block < redirect < allow)
                            if query[0][2] == policy == RulePolicy.BLOCK or \
                                    policy == RulePolicy.REDIRECT and policy != RulePolicy.ALLOW or \
                                    policy == RulePolicy.ALLOW:
                                cursor.execute(
                                    "UPDATE rules SET policy=?, filter_id=?, ip=? WHERE domain=?;",
                                    (policy, filter_id, ip, domain)
                                )
                        elif not query:
                            cursor.execute(
                                "INSERT INTO rules (domain, policy, filter_id, ip) VALUES (?, ?, ?, ?);",
                                (domain, policy, filter_id, ip)
                            )

        if not self.quiet:
            print(" {0} Inserting rules into database ({1}): {2}%".format(Icon.SUCCESS, all_rules_count, percent))
            print(" {0} Skipped {1} invalid rules or lines ({2}%)".format(
                Icon.INFORMATION, str(len(data) - connection.total_changes),
                str(round(((len(data) - connection.total_changes) * 100 / len(data)), 1))
            ))

    def convert(self, output_file: str, output_syntax: str, allow_comments: bool = False,
                redirect_to_zero: bool = False, dnsmasq_server: bool = False) -> None:
        try:
            with io.open(self.file, "rt") as f:
                data = f.readlines()
        except UnicodeDecodeError:
            raise FilterSyntaxError("unable to decode file: {0}".format(self.file))
        except PermissionError:
            raise FilterSyntaxError("unable to access file: {0}".format(self.file))
        except FileNotFoundError:
            raise FilterSyntaxError("file not found: {0}".format(self.file))

        if not self.quiet:
            print(" {0} Input syntax is: {1}".format(Icon.INFORMATION, self.syntax))

        # TBlock syntax support
        tblock_begin = False
        tblock_policy = None
        tblock_ip = None

        output_tblock_policy = None
        output_tblock_ip = None
        count = 0
        rules_count = len(data)

        with open(output_file, "wt") as w:
            if output_syntax == FilterSyntax.ADBLOCKPLUS:
                w.write("[Adblock Plus 2.0]\n\n")
            elif output_syntax == FilterSyntax.TBLOCK:
                w.write("@BEGIN_RULES\n\n")

            for line in data:

                if is_valid_rule(line.split("\n")[0], self.syntax):
                    if self.syntax == FilterSyntax.TBLOCK:
                        rule = get_rule(line.split("\n")[0], self.syntax, allow_comments=allow_comments,
                                        tblock_begin=tblock_begin, tblock_policy=tblock_policy, tblock_ip=tblock_ip)
                    else:
                        rule = get_rule(line.split("\n")[0], self.syntax, allow_comments=allow_comments)

                    if rule:
                        # Change the IP address if rule is a redirecting rule
                        if rule[1] == RulePolicy.REDIRECT:
                            ip = rule[2].compressed
                        else:
                            ip = None

                        # TBlock syntax support
                        if self.syntax == FilterSyntax.TBLOCK:
                            if rule[0] == TBlockSyntaxStatus.CURRENT_STATUS:
                                tblock_begin = rule[1]
                                continue
                            elif rule[0] == TBlockSyntaxStatus.CURRENT_POLICY:
                                tblock_policy = rule[1]
                                if tblock_policy == RulePolicy.REDIRECT:
                                    tblock_ip = rule[2]
                                continue

                        count += 1
                        percent = int(count * 100 / rules_count)
                        if not self.quiet:
                            print(" {0} Converting filter list ({1}): {2}%".format(
                                loading_icon(count), rules_count, percent), end="\r")

                        if output_syntax == FilterSyntax.ADBLOCKPLUS:
                            if rule[1] == RulePolicy.ALLOW:
                                w.write(f"@@||{rule[0]}^\n")
                            elif rule[1] == RulePolicy.BLOCK:
                                w.write(f"||{rule[0]}^\n")
                            elif rule[1] == RULE_COMMENTS and allow_comments:
                                w.write(f"!{rule[0]}\n")

                        elif output_syntax == FilterSyntax.HOSTS:
                            if rule[1] == RulePolicy.BLOCK and not contains_wildcards(rule[0]):
                                if redirect_to_zero:
                                    w.write(f"0.0.0.0\t\t{rule[0]}\n")
                                else:
                                    w.write(f"127.0.0.1\t\t{rule[0]}\n")
                            elif rule[1] == RulePolicy.REDIRECT and not contains_wildcards(rule[0]):
                                w.write(f"{ip}\t{rule[0]}\n")
                            elif rule[1] == RULE_COMMENTS and allow_comments:
                                w.write(f"#{rule[0]}\n")

                        elif output_syntax == FilterSyntax.LIST:
                            if rule[1] == RulePolicy.BLOCK and not contains_wildcards(rule[0]):
                                w.write(f"{rule[0]}\n")
                            elif rule[1] == RULE_COMMENTS and allow_comments:
                                w.write(f"#{rule[0]}\n")

                        elif output_syntax == FilterSyntax.DNSMASQ:
                            if rule[1] == RulePolicy.BLOCK and not contains_wildcards(rule[0]):
                                if dnsmasq_server:
                                    w.write(f"server=/{rule[0]}/\n")
                                elif redirect_to_zero:
                                    w.write(f"address=/{rule[0]}/0.0.0.0/\n")
                                else:
                                    w.write(f"address=/{rule[0]}/127.0.0.1/\n")
                            elif rule[1] == RulePolicy.REDIRECT and not contains_wildcards(rule[0]):
                                w.write(f"address=/{rule[0]}/{ip}/\n")
                            elif rule[1] == RULE_COMMENTS and allow_comments:
                                w.write(f"#{rule[0]}\n")

                        elif output_syntax == FilterSyntax.TBLOCK:
                            if not rule[1] == output_tblock_policy or not ip == output_tblock_ip:
                                if rule[1] == RulePolicy.ALLOW:
                                    w.write("\n!allow\n")
                                elif rule[1] == RulePolicy.BLOCK and not contains_wildcards(rule[0]):
                                    w.write("\n!block\n")
                                elif rule[1] == RulePolicy.REDIRECT and not contains_wildcards(rule[0]):
                                    w.write(f"\n!redirect {ip}\n")
                                if rule[1] != RULE_COMMENTS:
                                    output_tblock_policy = rule[1]
                                    output_tblock_ip = ip
                            if not rule[1] == RULE_COMMENTS:
                                w.write(f"{rule[0]}\n")
                            elif allow_comments:
                                w.write(f"#{rule[0]}\n")

                        else:
                            raise FilterSyntaxError(
                                "invalid output syntax: {0}".format(output_syntax)
                            )

            if output_syntax == FilterSyntax.TBLOCK:
                w.write("\n\n@END_RULES")

        if not self.quiet:
            print(" {0} Converting filter list ({1}): 100%".format(Icon.SUCCESS, rules_count))
            print(" {0} Skipped {1} rules ({2}%)".format(Icon.INFORMATION, rules_count - count,
                                                         round((rules_count - count) * 100 / rules_count, 1)))


def convert(input_file: str, output_file: str, output_syntax: str, input_syntax: str = None,
            allow_comments: bool = False, redirect_to_zero: bool = False, dnsmasq_server: bool = False,
            quiet: bool = False) -> None:
    if not quiet:
        print(f"{Font.BOLD}==> Converting filter list{Font.DEFAULT}")
    filter_parser = FilterParser(input_file, syntax=input_syntax, quiet=quiet)
    filter_parser.convert(output_file, output_syntax, allow_comments=allow_comments,
                          redirect_to_zero=redirect_to_zero, dnsmasq_server=dnsmasq_server)


def detect_filter_list_syntax(input_file: str) -> None:
    print(f"{Font.BOLD}==> Detecting filter list syntax{Font.DEFAULT}")
    filter_parser = FilterParser(input_file)
    print(f" {Icon.INFORMATION} Filter list syntax is: {filter_parser.syntax}")


def list_syntax() -> None:
    for s in ALL_SYNTAX:
        print(s)
