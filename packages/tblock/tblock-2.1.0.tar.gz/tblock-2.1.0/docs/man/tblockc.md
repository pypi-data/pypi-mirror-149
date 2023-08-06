%TBLOCKC(1)

# NAME

tblockc - tblock’s built-in filter list converter

# SYNOPSIS

**tblockc** \[operation\] \[option(s)\] \[arg(s)\]

# DESCRIPTION

**tblockc** is one of the various utilities provided by the free and open-source ad-blocker called TBlock. This command can be used to convert local filter lists into another filter list format.

# OPERATIONS

**-h, -\-help**
: Show this help page

**-v, -\-version**
: Show version and license information

**-g, -\-get-syntax**
: Detect the filter list format of a file

**-l, -\-list-syntax**
: List supported filter formats

**-C, -\-convert** _FILEPATH_
: Convert a filter list into another filter list format

# OPTIONS

**-s, -\-syntax** _FORMAT_
: Specify the syntax to use for output

**-o, -\-output** _FILEPATH_
: Specify the output file

**-c, -\-comments**
: Also convert comments

**-i, -\-input-syntax** _FORMAT_
: Specify the input filter list format

**-0, -\-zero**
: Redirect domains to `0.0.0.0` instead of `127.0.0.1` (**hosts**/**dnsmasq**)

**-e, -\-server**
: Block domains using "server" (**dnsmasq**)

# FILTER LIST FORMATS SUPPORTED

**adblockplus**
: Adblock Plus / uBlock Origin syntax

**dnsmasq**
: dnsmasq configuration file

**hosts**
: Hosts file format

**list**
: Plain text blocklist

**tblock**
: Highly-compatible TBlock filter list syntax

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

**tblock**(1), **tblockd**(1), **tblock.conf**(5), **hosts**(5), **dnsmasq**(8)

# AUTHORS

- Twann
