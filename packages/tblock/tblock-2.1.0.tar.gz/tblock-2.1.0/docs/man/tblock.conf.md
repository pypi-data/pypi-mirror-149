%TBLOCK.CONF(1)

# NAME

tblock.conf - tblock configuration file format

# LOCATION

The configuration must be placed under _/etc/tblock.conf_ under UNIX-like systems, and under _%ALLUSERSPROFILE%\\TBlock\\conf.ini_ under Microsoft Windows.

# DESCRIPTION

**tblock.conf** is a configuration file that lets the user change how the TBlock ad-blocker works.

# OPTIONS

There are two sections. One is _[default]_, and controls the ad-blocker behavior in general. The other is _[daemon]_, and controls only the daemon.

## [default]

**default_ip** = _[IP]_
: Change the default IPv4 redirecting address for blocked domains. Default is `127.0.0.1`.

**default_ipv6** = _[IPv6]_
: Change the default IPv6 redirecting address for blocked domains. Default is `::1`.

**allow_ipv6** = _[true/false]_
: Allow IPv6 rules and IPv6-based blocking. Default is `false`.

**default_permissions** = _[PERMISSIONS]_
: Default filter permissions (A for Allow, B for Block, R for Redirect). Multiple options are supported. Default is `B`.

**prefer_onion** = _[true/false]_
: Prefer the filter list repository onion mirror (needs to redirect TBlock's traffic through the Tor network). This is recommended if you live in a country where other mirrors are censored, or if you are using TBlock behind a restrictive firewall. Default is `false`.

## [daemon]

**sync_repo** = _[true/false]_
: Sync the repository when updating filter lists. Default is `false`.

**frequency** = _[MINUTES]_
: Update filter lists every _x_ minutes. Default is `240`.

**force** = _[true/false]_
: Force-update filter lists. Default is `false`.

**anti_hijack** = _[true/false]_
: Detect and prevent hosts file hijack. Default is `true`.

# LINKS

- Homepage: _https://tblock.codeberg.page/_
- Documentation: _https://tblock.codeberg.page/docs/_
- Bug tracker: _https://codeberg.org/tblock/tblock/issues/_
- About the project: _https://tblock.codeberg.page/about.html_

# LICENSE

Copyright (C) 2021-2022

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <_https://www.gnu.org/licenses/_>.

# SEE ALSO

**tblock**(1), **tblockc**(1), **tblockd**(1), **hosts**(5), **dnsmasq**(8)

# AUTHORS

- Twann
