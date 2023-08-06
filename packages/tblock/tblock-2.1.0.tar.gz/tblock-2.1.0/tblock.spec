Name:           tblock
Version:        2.1.0
Release:        1%{?dist}
Summary:        An anti-capitalist ad-blocker that uses the hosts file

License:        GPLv3
URL:            https://tblock.codeberg.page
Source0:        https://codeberg.org/tblock/tblock/archive/%{version}.tar.gz

BuildRequires:  make
BuildRequires:  pandoc
BuildRequires:  gzip
BuildRequires:  python
BuildRequires:  python-setuptools
BuildRequires:  python-colorama
BuildRequires:  python-requests
BuildRequires:  python-urllib3
BuildRequires:  python-defusedxml
Requires:       python
Requires:       python-colorama
Requires:       python-requests
Requires:       python-urllib3
Requires:       python-defusedxml

%description
TBlock is a system-wide, platform independent ad-blocker written in Python and released under GPLv3.

%global debug_package %{nil}

%prep
%autosetup

%build
make 

%install
rm -rf %{buildroot}
make install ROOT=%{buildroot}
make install-config ROOT=%{buildroot}

%files
%license LICENSE.txt
%doc README.txt
%config(noreplace) /etc/tblock.conf
/usr/bin/tblock
/usr/bin/tblockc
/usr/bin/tblockd
/usr/lib/python3.*/site-packages/tblock/
/usr/lib/python3.*/site-packages/tblock-*-py3.*.egg-info/
/usr/lib/systemd/system/tblockd.service
/usr/share/man/man1/tblock.1.gz
/usr/share/man/man1/tblockc.1.gz
/usr/share/man/man1/tblockd.1.gz
/usr/share/man/man5/tblock.conf.5.gz

%changelog
* Sun Mar 13 09:56:30 CEST 2022 Twann <tw4nn@disroot.org>
- Release v2.0.0. Consult the changelog here: https://codeberg.org/tblock/tblock/src/branch/main/CHANGELOG

