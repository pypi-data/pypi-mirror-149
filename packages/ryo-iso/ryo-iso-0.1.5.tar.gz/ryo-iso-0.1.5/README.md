# ryo-iso
[![](https://img.shields.io/pypi/v/ryo_iso.svg?style=flat)](https://pypi.org/project/ryo-iso/)
[![](https://builds.sr.ht/~lucidone/ryo-iso.svg)](https://builds.sr.ht/~lucidone/ryo-iso)
[![](https://readthedocs.org/projects/ryo-iso/badge/?version=latest)](https://ryo-iso.readthedocs.io/en/latest/?badge=latest)

-----

**Table of Contents**

* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

## Overview

ryo-iso is distributed on [PyPI](https://pypi.org/project/ryo-iso/) and is available for
Python 3.8+ on Linux.

```bash
$ python3 -m pip install -U --user git+https://git.sr.ht/~lucidone/ryo-iso
```

### Documentation
Documentation is available at https://ryo-iso.readthedocs.io/

### Deprecated
  - Ubuntu 16.04 (Xenial)
  - Python 3.6

### Currently supported targets
  - Ubuntu 18.04 (Bionic)
  - Ubuntu 20.04 (Focal)
  - Ubuntu 22.04 (Focal)

## Usage

### TL;DR
```bash
$ sudo apt install curl gpgv2 squashfs-tools xorriso apt-utils apt-cacher-ng qemu-system-x86 isolinux
$ if [ $(lsb_release -cs) = "jammy" ]; then sudo apt install jq fdisk; fi
$ python3 -m pip install -U --user git+https://git.sr.ht/~lucidone/ryo-iso
$ mkdir ~/iso_test
$ cd ~/iso_test
$ ryo-iso init
$ ryo-iso build
$ ryo-iso start
```

## Requirements
`$ sudo apt install curl gpgv2 squashfs-tools xorriso apt-utils apt-cacher-ng qemu-system-x86 isolinux`
Working with `jammy` also requires
`$ sudo apt install jq fdisk`

## Other commands
### Create a new project
`$ ryo-iso init`

This command will initialize a project with a default `iso.yml` configuration
file in the current directory.

If this is the first time being run it will create the `ryo-iso` application
config file in `~/.config/ryo-iso/config.yml` and provides a set of
reasonable defaults in `~/.config/ryo-iso/iso_base.yml` that can be overridden
on a per-project basis.

### Build an ISO
`$ ryo-iso build`

Builds an iso in `build/image.iso`

### VM Install
`$ ryo-iso install`

Generated images can be tested by installing them into a QEMU VM

### VM Start
`$ ryo-iso start`

This command can provide a means of booting the image as a LiveCD or restarting
a previously installed disk image.

### Cleanup
`$ ryo-iso clean`

This command will remove all build artifacts to prepare the project to be
checked into version control.

NOTE: Using this command is preferable to running `rm -rf` as builds that are
aborted with <key>Ctrl-C</key> may leave chrooted filesystems mounted.

### Additional
`$ ryo-iso list -p`

This will list all intermediate processes that may be useful for debugging.

### GPG Keys
All of the keys found in `./keys` will be install into the squashfs-root
On `jammy` and later they should be referenced via
`deb [arch=amd64 signed-by=/usr/share/keyrings/repo-keyring.gpg] http://repo.example.org/ ubuntu jammy main`

## License

ryo-iso is distributed under the terms of both

- [MIT License](https://choosealicense.com/licenses/mit)
- [Apache License, Version 2.0](https://choosealicense.com/licenses/apache-2.0)

at your option.
