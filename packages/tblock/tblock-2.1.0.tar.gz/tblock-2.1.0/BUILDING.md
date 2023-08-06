# Notes for packagers

TBlock can be installed with the `make` utility, using two simple steps.
Here, we'll assume that we are building a package inside a directory called `pkg/`.

# Preparation

Before anything else, let's ensure we have the following packages installed:

- `make`
- `python3`
- `python3-setuptools`
- `sudo`
- `tar`
- `pandoc`
- `gzip`

After that, download the [latest source tarball](https://codeberg.org/tblock/tblock/releases), extract it and enter the directory.

Then, build TBlock and its man pages:

```sh
make
```

Finally, install everything under `pkg/`:

## With systemd

```sh
make install ROOT=pkg
```

The directory `pkg` should now have a structure similar to:

```
pkg
└── usr
    ├── bin
    │   ├── tblock
    │   ├── tblockc
    │   └── tblockd
    ├── lib
    │   ├── python3.10
    │   │   └── site-packages
    │   │       ├── tblock
    │   │       │   └── ...
    │   │       └── tblock-2.0.0b1-py3.10.egg-info
    │   │           ├── dependency_links.txt
    │   │           ├── entry_points.txt
    │   │           ├── PKG-INFO
    │   │           ├── requires.txt
    │   │           ├── SOURCES.txt
    │   │           └── top_level.txt
    │   └── systemd
    │       └── system
    │           └── tblockd.service
    └── share
        ├── doc
        │   └── tblock
        │       └── README.txt
        ├── licenses
        │   └── tblock
        │       └── LICENSE.txt
        └── man
            ├── man1
            │   ├── tblock.1.gz
            │   ├── tblockc.1.gz
            │   └── tblockd.1.gz
            └── man5
                └── tblock.conf.5.gz
```

## With OpenRC

To install an OpenRC service instead of a systemd unit file during the packaging process, simply use the following instead of `make install`:

```sh
make install-openrc ROOT=pkg
```

## Configuration file

Finally, install the configuration file under `pkg/etc/tblock.conf` by running:

```sh
make install-config ROOT=pkg
```

