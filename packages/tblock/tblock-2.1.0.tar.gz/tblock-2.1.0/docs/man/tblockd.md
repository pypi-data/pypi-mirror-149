%TBLOCKD(1)

# NAME

tblockd - tblock’s built-in daemon

# SYNOPSIS

**tblockd** \[operation\] \[option(s)\] \[arg(s)\]

# DESCRIPTION

**tblockc** is one of the various utilities provided by the free and open-source ad-blocker called TBlock. This command can be used to run a daemon process that prevents hosts file hijack and that updates filter lists at a regular time interval.

# OPERATIONS

**-h, -\-help**
: Show this help page

**-v, -\-version**
: Show version and license information

**-d, -\-daemon**
: Start the daemon

# OPTIONS

**-c, -\-config** _FILEPATH_
: Path to the config file to use

**-n, -\-no-pid**
: Do not create a PID file

# LINKS

- Homepage: _https://tblock.codeberg.page/_
- Documentation: _https://tblock.codeberg.page/docs/_
- Bug tracker: _https://codeberg.org/tblock/tblock/issues/_
- About the project: _https://tblock.codeberg.page/about.html_

# LICENSE

Copyright (C) 2021-2022 Twann

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

**tblock**(1), **tblockc**(1), **tblock.conf**(5), **hosts**(5), **dnsmasq**(8)

# AUTHORS

- Twann
