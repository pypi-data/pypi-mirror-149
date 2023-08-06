# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5]
### Added
- Support for Ubuntu 'jammy'
### Changed
- APT keys in `./keys/*.gpg` install target changed for Ubuntu >= 'Jammy'
  "squashfs-root/etc/apt/trusted.gpg.d/." -> "squashfs-root/usr/share/keyrings/."
### Removed
- Deprecated support for Ubuntu 16.04
- Deprecating Python3.6 support

## [0.1.4]
### Fixed
- Locking pydoit to v0.34.2 before deprecating python3.6 support

## [0.1.3]
### Added
- Invalidate sudo credential cache
- `iso.yml` config option for qemu args
### Changed
- Optionalize image/casper/filesystem.size update for ubuntu-live-server

## [0.1.2]
### Changed
- Updated requirements in documentation

### Fixed
- 'xenial' open(pathlib.Path()) regression
- 'xenial' resolv.conf uptodate check

## [0.1.1]
### Fixed
- Updated documentation for PyPi

## [0.1.0]
### Added
- Project Initialized

[0.1.5]: https://git.sr.ht/~lucidone/ryo-iso/tree/0.1.5
[0.1.4]: https://git.sr.ht/~lucidone/ryo-iso/tree/0.1.4
[0.1.3]: https://git.sr.ht/~lucidone/ryo-iso/tree/0.1.3
[0.1.2]: https://git.sr.ht/~lucidone/ryo-iso/tree/0.1.2
[0.1.1]: https://git.sr.ht/~lucidone/ryo-iso/tree/0.1.1
[0.1.0]: https://git.sr.ht/~lucidone/ryo-iso/tree/0.1.0
[Unreleased]: https://git.sr.ht/~lucidone/ryo-iso/tree
