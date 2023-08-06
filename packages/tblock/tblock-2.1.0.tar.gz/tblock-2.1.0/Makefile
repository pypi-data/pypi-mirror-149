#!/usr/bin/env make -j2

# TBlock default Makefile
# Run 'make help' to show help message

# Define variables
PYTHON ?= /usr/bin/env python3
ROOT ?= /
DESTDIR ?= $(ROOT)/usr

all: build build-files

.PHONY: all clean build-wheel build-sdist build-pypi man test test-pytest test-bandit test-flake8 install install-openrc uninstall uninstall-openrc install-config uninstall-config

# ----- CLEAN -----

clean:
	rm -rf build dist README.txt *.1.gz *.5.gz *.1 *.5 *.egg-info tblock/__pycache__ tblock/*/__pycache__ test/__pycache__ test/fake_root *.bin

# ----- BUILD -----

build:
	$(PYTHON) ./setup.py build

build-pypi: build-wheel build-sdist

build-wheel:
	$(PYTHON) ./setup.py bdist_wheel

build-sdist:
	$(PYTHON) ./setup.py sdist


build-files: man README.txt

man: tblock.1.gz tblockc.1.gz tblockd.1.gz tblock.conf.5.gz

tblock.bin:
	mkdir -p zip
	for d in tblock tblock/converter tblock/argumentor; do mkdir -p zip/$$d ; cp -pPR $$d/*.py zip/$$d/ ; done
	touch -t 200001010101 zip/tblock/*.py zip/tblock/*/*.py
	echo 'from tblock.cli import run\n\nrun()' > zip/__main__.py
	cd zip ; zip -q ../tblock tblock/*.py tblock/*/*.py __main__.py
	rm -rf zip
	echo '#!/usr/bin/env python3' > tblock.bin
	cat tblock.zip >> tblock.bin
	rm tblock.zip
	chmod a+x tblock.bin

tblockc.bin:
	mkdir -p zip
	for d in tblock tblock/converter tblock/argumentor; do mkdir -p zip/$$d ; cp -pPR $$d/*.py zip/$$d/ ; done
	touch -t 200001010101 zip/tblock/*.py zip/tblock/*/*.py
	echo 'from tblock.cli import run_converter\n\nrun_converter()' > zip/__main__.py
	cd zip ; zip -q ../tblock tblock/*.py tblock/*/*.py __main__.py
	rm -rf zip
	echo '#!/usr/bin/env python3' > tblockc.bin
	cat tblock.zip >> tblockc.bin
	rm tblock.zip
	chmod a+x tblockc.bin

tblockd.bin:
	mkdir -p zip
	for d in tblock tblock/converter tblock/argumentor; do mkdir -p zip/$$d ; cp -pPR $$d/*.py zip/$$d/ ; done
	touch -t 200001010101 zip/tblock/*.py zip/tblock/*/*.py
	echo 'from tblock.cli import run_daemon\n\nrun_daemon()' > zip/__main__.py
	cd zip ; zip -q ../tblock tblock/*.py tblock/*/*.py __main__.py
	rm -rf zip
	echo '#!/usr/bin/env python3' > tblockd.bin
	cat tblock.zip >> tblockd.bin
	rm tblock.zip
	chmod a+x tblockd.bin

bin: tblock.bin tblockc.bin tblockd.bin

tblock.1.gz:
	pandoc -s -f markdown ./docs/man/tblock.md -t man -o tblock.1
	gzip -9 tblock.1

tblockc.1.gz:
	pandoc -s -f markdown ./docs/man/tblockc.md -t man -o tblockc.1
	gzip -9 tblockc.1

tblockd.1.gz:
	pandoc -s -f markdown ./docs/man/tblockd.md -t man -o tblockd.1
	gzip -9 tblockd.1

tblock.conf.5.gz:
	pandoc -s -f markdown ./docs/man/tblock.conf.md -t man -o tblock.conf.5
	gzip -9 tblock.conf.5

README.txt:
	pandoc -s -f markdown -t plain README.md -o README.txt

# ----- TEST -----

test:
	$(PYTHON) -V
	+make test-nose test-bandit test-flake8

test-nose:
	$(PYTHON) -m nose test -v

test-bandit:
	$(PYTHON) -m bandit -r tblock -c .bandit.yml

test-flake8:
	$(PYTHON) -m flake8 tblock

# ----- INSTALL -----

install: all install-files install-service-systemd install-python-module

install-openrc: all install-files install-service-openrc install-python-module

install-files: build-files
	install -Dm644 tblock.1.gz $(DESTDIR)/share/man/man1/tblock.1.gz
	install -Dm644 tblockc.1.gz $(DESTDIR)/share/man/man1/tblockc.1.gz
	install -Dm644 tblockd.1.gz $(DESTDIR)/share/man/man1/tblockd.1.gz
	install -Dm644 tblock.conf.5.gz $(DESTDIR)/share/man/man5/tblock.conf.5.gz
	install -Dm644 README.txt $(DESTDIR)/share/doc/tblock/README.txt
	install -Dm644 LICENSE $(DESTDIR)/share/licenses/tblock/LICENSE.txt

install-service-openrc:
	install -Dm755 assets/services/openrc/tblockd.initd $(ROOT)/etc/init.d/tblockd

install-service-systemd:
	install -Dm644 assets/services/systemd/tblockd.service $(DESTDIR)/lib/systemd/system/tblockd.service

install-python-module:
	$(PYTHON) ./setup.py install --root=$(ROOT) --skip-build --optimize=1

install-config:
	install -Dm644 assets/config/tblock.conf $(ROOT)/etc/tblock.conf

install-bin:
	install -Dm755 tblock.bin $(DESTDIR)/bin/tblock
	install -Dm755 tblockc.bin $(DESTDIR)/bin/tblockc
	install -Dm755 tblockd.bin $(DESTDIR)/bin/tblockd

# ----- UNINSTALL -----
uninstall:
	rm -f $(DESTDIR)/bin/tblock
	rm -f $(DESTDIR)/bin/tblockc
	rm -f $(DESTDIR)/bin/tblockd
	rm -rf $(DESTDIR)/lib/python3.*/site-packages/tblock*
	rm -f $(DESTDIR)/share/man/man1/tblock.1.gz
	rm -f $(DESTDIR)/share/man/man1/tblockc.1.gz
	rm -f $(DESTDIR)/share/man/man1/tblockd.1.gz
	rm -f $(DESTDIR)/share/man/man5/tblock.conf.5.gz
	rm -f $(DESTDIR)/share/doc/tblock/README.txt
	rm -f $(DESTDIR)/share/licenses/tblock/LICENSE.txt
	rm -f $(DESTDIR)/lib/systemd/system/tblockd.service

uninstall-openrc:
	rm -f $(DESTDIR)/bin/tblock
	rm -f $(DESTDIR)/bin/tblockc
	rm -f $(DESTDIR)/bin/tblockd
	rm -rf $(DESTDIR)/lib/python3.*/site-packages/tblock*
	rm -f $(DESTDIR)/share/man/man1/tblock.1.gz
	rm -f $(DESTDIR)/share/man/man1/tblockc.1.gz
	rm -f $(DESTDIR)/share/man/man1/tblockd.1.gz
	rm -f $(DESTDIR)/share/man/man5/tblock.conf.5.gz
	rm -f $(DESTDIR)/share/doc/tblock/README.txt
	rm -f $(DESTDIR)/share/licenses/tblock/LICENSE.txt
	rm -f $(ROOT)/etc/init.d/tblockd

uninstall-config:
	rm -f $(ROOT)/etc/tblock.conf

# ----- HELP -----
help:
	@echo "TBlock default Makefile help page"
	@echo
	@echo "usage: make <option> [VARIABLE=VALUE]"
	@echo
	@echo "OPTIONS:"
	@echo "---[help]---"
	@echo "  help					Show this help page"
	@echo "---[clean]---"
	@echo "  clean					Clean build files"
	@echo "---[build]---"
	@echo "  all					Build Python package, man pages and README.txt (default)"
	@echo "  build					Build the Python package"
	@echo "  build-pypi				Build the Python wheel and standard distribution"
	@echo "  build-wheel				Build the Python wheel"
	@echo "  build-sdist				Build the Python standard distribution (tar archive)"
	@echo "  build-files				Build man pages and README.txt"
	@echo "  man					Build man pages"
	@echo "  build					Build binaries"
	@echo "  tblock.bin				Build the tblock binary"
	@echo "  tblockc.bin				Build the tblockc binary"
	@echo "  tblockd.bin				Build the tblockd binary"
	@echo "  tblock.1.gz				Build the man page for tblock"
	@echo "  tblockc.1.gz				Build the man page for tblockc"
	@echo "  tblockd.1.gz				Build the man page for tblockd"
	@echo "  tblock.conf.5.gz			Build the man page for tblock.conf"
	@echo "  README.txt				Build the README.txt file"
	@echo "---[test]---"
	@echo "  test					Run all tests"
	@echo "  test-bise				Run nose tests"
	@echo "  test-bandit				Test for vulnerability within the code"
	@echo "  test-flake8				Test for syntax error within the code"
	@echo "---[install]---"
	@echo "  install				Install TBlock (with systemd service) and its build files"
	@echo "  install-openrc			Install TBlock (with OpenRC service) and its build files"
	@echo "  install-files				Install man pages, license and README.txt"
	@echo "  install-service-systemd		Install systemd service"
	@echo "  install-service-openrc		Install openrc service"
	@echo "  install-python-module			Install TBlock's python module (default with install)"
	@echo "  install-bin				Install TBlock binaries"
	@echo "  install-config			Install TBlock's configuration file on the machine"
	@echo "---[uninstall]---"
	@echo "  uninstall				Uninstall TBlock from the machine (with systemd service)"
	@echo "  uninstall-openrc			Uninstall TBlock from the machine (with OpenRC service)"
	@echo "  uninstall-config			Uninstall TBlock's configuration file from the machine"
	@echo ""
	@echo "VARIABLES:"
	@echo "  PYTHON	Specify the Python interpreter to use (default: /usr/bin/env python3)"
	@echo "  ROOT		Specify the root filesystem for installation (default: /)"
	@echo "  DESTDIR	Specify the directory where to install TBlock (default: ROOT/usr)"
	@echo ""
	@echo "You can visit https://tblock.codeberg.page/docs//installation-build-manually.html for more information"
