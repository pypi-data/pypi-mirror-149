%TBLOCK(1)

# NAME

tblock - an anti-capitalist ad-blocker that uses the hosts file

# SYNOPSIS

**tblock** \[operation\] \[option(s)\] \[arg(s)\]

# DESCRIPTION

**tblock** is one of the various utilities provided by the free and open-source ad-blocker called TBlock. This command can be used to manage the domains to block, as well as the online sources to use in order to have an efficient protection against advertising and tracking.

# OPERATIONS

## GENERAL

**-h, -\-help**
: Show this help page

**-s, -\-status**
: Show status information

**-v, -\-version**
: Show version and license information

## RULES

**-a, -\-allow** _DOMAIN [DOMAIN(S)...]_
: Allow specified domain(s)

**-b, -\-block** _DOMAIN [DOMAIN(S)...]_
: Block specified domain(s)

**-r, -\-redirect** _DOMAIN [DOMAIN(S)...]_ \[**[-i, -\-ip]** _[IP]_\]
: Redirect specified domain(s)

**-d, -\-delete-rule** _DOMAIN [DOMAIN(S)...]_
: Delete rule(s) for specified domain(s)

## FILTER LISTS

**-Y, -\-sync**
: Sync the filter list repository

**-S, -\-subscribe** _ID [ID(S)...]_
: Subscribe to specified filter list(s)

**-C, -\-add-custom** _ID SOURCE [ID(s) SOURCE(s)...]_
: Subscribe to specified custom filter list(s)

**-N, -\-rename** _ID NEWID [ID(S) NEWID(S)...]_
: Rename specified custom filter list(s)

**-R, -\-remove** _ID [ID(S)...]_
: Unsubscribe from specified filter list(s)

**-U, -\-update**
: Update all filter lists

**-M, -\-mod** _ID [ID(S)...]_ \[**[-p, -\-permissions]** _[PERMISSIONS]_\]
: Change permissions of specified filter list(s)

**-I, -\-info** _ID [ID(S)...]_
: Get information about specified filter list(s)

**-P, -\-purge-cache**
: Remove cached filter lists

## HOSTS

**-D, -\-restore**
: Restore default hosts file

**-H, -\-update-hosts**
: Update hosts file

**-G, -\-gen-hosts**
: Generate hosts file template

## SEARCH

**-l, -\-list-rules**
: List rules

**-L, -\-list**
: List filter lists

**-Q, -\-search**
: Perform a search inside filter lists database

# OPTIONS

## GENERAL

**-n, -\-no-prompt**
: Do not prompt for anything

## RULES

**-i, -\-ip** _IP_
: Specify the redirection IP address (with **-\-redirect**)

## FILTER LISTS

**-p, -\-permissions** _PERMISSIONS_
: Specify the permissions to give to filter lists

**-y, -\-with-sync**
: Also sync filter list repository

**-u, -\-with-update**
: Also update all filter lists

**-x, -\-custom-syntax** _FORMAT_
: Specify the syntax of a custom filter list

**-f, -\-force**
: Force to update filter lists or repository

## SEARCH

**-e, -\-user**
: List user rules only

**-t, -\-standard**
: List standard (filter lists) rules only

**-m, -\-from-filters** _ID [ID(S)...]_
: List rules coming from specific filter lists only

**-c, -\-custom**
: List custom filter lists only

**-w, -\-on-repo**
: List filter lists available on the filter list repository only

**-k, -\-subscribing**
: List subscribed filter lists only

**-z, -\-not-subscribing**
: List unsubscribed filter lists only

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

**tblockc**(1), **tblockd**(1), **tblock.conf**(5), **hosts**(5), **dnsmasq**(8)

# AUTHORS

- Twann
