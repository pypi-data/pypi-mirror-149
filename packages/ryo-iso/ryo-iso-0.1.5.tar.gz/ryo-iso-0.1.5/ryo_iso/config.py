import appdirs as _appdirs
from pathlib import Path as _Path
# NOTE: importlib backport for Python 3.5
import importlib_resources as _resources
import shutil as _shutil
import time as _time
import yaml as _yaml
import sys as _sys
import os as _os
import re as _re
from loguru import logger as _logger
import requests as _requests
import delegator as _delegator

_ctx = None

class Config:
    """
    Configuration State

    This class stores configuration information and provides
    methods for validation and network updates

    Methods
    -------
    __init__(config='~/.config/ryo-iso/config.yml')
        Loads ``config`` file and perform initialization
    *distro*_init()
        Performs distribution specific initialization
    """

    # Config File Setup
    _cfg_dir = (_os.environ.get('RYO_USER_CONFIG_DIR')
                or _appdirs.user_config_dir('ryo-iso', 'HxR'))
    _iso_cfg = _os.environ.get('RYO_ISO_CONF')
    data = {
        'app':  _Path(_cfg_dir) / 'config.yml',
        'base': _Path(_cfg_dir) / 'iso_base.yml',
        'iso':  _Path(_iso_cfg) if _iso_cfg else (_Path.cwd() / 'iso.yml'),
    }
    build_dir = _Path(_os.environ.get('RYO_BUILD_DIR') or _Path.cwd())

    @classmethod
    def install(cls,force=False):
        """
        Install user config files.

        This function installs the application and project config files.

        Parameters
        ----------
        force : bool
            Overwrite existing config files
        """

        cls.data['app'].parent.mkdir(parents=True, exist_ok=True)
        if (not cls.data['app'].exists() or force):
            # Install application config from package resources
            # into $XDG_CONFIG_HOME/ryo-iso/config.yml
            with _resources.path("ryo_iso.data", 'config.yml') as default_config:
                _logger.debug("Install %s to %s"%(default_config, cls.data['app']))
                # NOTE: Python 3.5 shutil.copy does not accept pathlib.Path
                _shutil.copy(str(default_config), str(cls.data['app']))

        cls.data['base'].parent.mkdir(parents=True, exist_ok=True)
        if (not cls.data['base'].exists() or force):
            # Install base config from package resources
            # into $XDG_CONFIG_HOME/ryo-iso/iso_base.yml
            with _resources.path("ryo_iso.data", 'iso_base.yml') as default_config:
                _logger.debug("Install %s to %s"%(default_config, cls.data['base']))
                # NOTE: Python 3.5 shutil.copy does not accept pathlib.Path
                _shutil.copy(str(default_config), str(cls.data['base']))


        if (not cls.data['iso'].exists() or force):
            # Install Project config from package resources
            with _resources.path("ryo_iso.data", 'iso.yml') as default_config:
                _logger.debug("Install %s to %s"%(default_config, cls.data['iso']))
                # NOTE: Python 3.5 shutil.copy does not accept pathlib.Path
                _shutil.copy(str(default_config), str(cls.data['iso']))

    @staticmethod
    def deep_merge(overlay, base):
        """
        Deep merge dictionaries

        This method recursivly merges dictionaries, where ``base`` provides
        defaults for the dictionary ``overlay``. Sub-lists and dictionaries
        inside lists are replaced and not merged.

        Parameters
        ----------
        overlay : dict
            This dictionary is modified in place to contain the merged results.
        base : dict
            Provides default values not found in the overlay.
        """
        for k in base.keys():
            if isinstance(base[k],dict):
                overlay[k] = overlay.get(k) or {}
                Config.deep_merge(overlay[k],base[k])
            else:
                overlay[k] = overlay.get(k) or base[k]

    def __repr__(self):
        #report = {}
        #report['data'] = self.data
        #report['base_image'] = self.base_image
        #report['file'] = self.file
        #report['cache'] = self.cache
        #report['url'] = self.url
        return _yaml.dump(self.iso_cfg)

    def __init__(self,config=data['iso']):
        """
        Initialize Config Class

        This class loads a config file and provides functions for
        updating the configurational state from online resources

        Parameters
        ----------
        config : str
            iso project config file
        """

        # hashes are cached before they are validated
        self.app_cache_dir = _Path(_appdirs.user_cache_dir('ryo-iso', 'HxR'))
        self.app_cache_dir.mkdir(parents=True, exist_ok=True)

        with self.data['app'].open('r') as f:
            self.app_cfg = _yaml.safe_load(f)

        with self.data['base'].open('r') as f:
            self.base_cfg = _yaml.safe_load(f)

        with config.open('r') as f:
            self.iso_cfg = _yaml.safe_load(f)

        # Setup `iso.yml` defaults via `$XDG_CONFIG_HOME/ryo-iso/iso_base.yml`
        self.deep_merge(self.iso_cfg,self.base_cfg)

        self.base_image={}

        # supported distros
        distros = ['ubuntu']

        # Parse ``image: {{ distro }}/{{version}}`` from config
        # See builds.sr.ht config file for aesthetics
        (self.base_image['distro'],self.base_image['version']) = self.iso_cfg['image'].split('/')
        if self.base_image['distro'] not in distros:
            _logger.error("Unsupported Distro")
            _sys.exit(_os.EX_CONFIG)

        # Distro plug-in system
        # Remap Config.{{distro}}_{{command}}() to Config.distro_{{command}}()
        # TODO: This probably needs to be refactored into a submodule
        cmds = ['init', 'update',
                'hash_cache', 'hash_check', 'hash_version',
                'base_image_check',
        ]
        for cmd in cmds:
            setattr(self,"distro_"+cmd, getattr(self, self.base_image['distro']+"_"+cmd))

        # Initialize {{ distro }}
        self.distro_init(self.base_image['version'])

    def ubuntu_init(self,version):
        """
        Ubuntu - distro specific initialization

        This function normalizes versions and codenames to compose
        the URLs for the distribution and associated hash file

        Parameters
        ----------
        version : str
            Version of the distribution
        """
        codenames = ['xenial', 'bionic', 'cosmic', 'focal', 'impish', 'jammy']
        codevers = {'16.04': 'xenial', '18.04': 'bionic', '18.10': 'cosmic', '20.04': 'focal', '21.10': 'impish', '22.04': 'jammy'}

        if version in codenames:
            self.base_image['codename'] = version

        match = _re.match(r'^(\d+\.\d+)$',version)
        if match:
            self.base_image['codename'] = codevers[match.group(0)]

        match = _re.match(r'^(\d+\.\d+\.\d+)$',version)
        if match:
            for ver in codevers:
                if version.startswith(ver):
                    self.base_image['codename'] = codevers[ver]

        self.base_image['release_url'] = ('http://releases.ubuntu.com/'
                                  + self.base_image['codename'] + '/')

        # NOTE: The ISO image download directory should have sufficient disk space
        self.base_image['dir'] = ( _Path(
            self.app_cfg['distro_image_dir']).expanduser()
            / self.base_image['distro']
            / self.base_image['codename']
        )
        self.base_image['dir'].mkdir(parents=True, exist_ok=True)

        self.file = {}
        self.file['hash'] = 'SHA256SUMS'
        self.file['sign'] = 'SHA256SUMS.gpg'

        self.cache = {}
        for k in self.file.keys():
            self.cache[k] = self.app_cache_dir / self.file[k]

    def ubuntu_hash_cache(self):
        """
        Ubuntu - SHA256 checksum download

        This function downloads the hashes and the associated gpg signature file.
        ``['SHA256SUMS', 'SHA256SUMS.gpg']``
        """
        _logger.debug("ubuntu_hash_cache")
        self.url = {}
        for k in self.file.keys():
            self.url[k] = self.base_image['release_url'] + self.file[k]

        for k in self.cache.keys():
            with open(str(self.cache[k]),'w') as f:
                _logger.debug("Downloading %s to %s"%(self.url[k],self.cache[k]))
                r = _requests.get(self.url[k])
                f.write(r.text)

    def ubuntu_hash_check(self):
        """
        Ubuntu - Verify GPG signature of SHA256 checksum download

        This function verifies the GPG signature of ``SHA256SUMS`` from the
        local keyring.
        """
        _logger.debug("ubuntu_hash_check")
        keyring = [ "/usr/share/keyrings/ubuntu-archive-keyring.gpg",
                    "/usr/share/keyrings/ubuntu-archive-removed-keys.gpg"
                  ]
        keyargs = map(lambda i: "--keyring "+i, keyring)
        cmd = ("gpgv2 "+ " ".join(keyargs)
               + " " + str(self.cache['sign'])
               + " " + str(self.cache['hash'])
        )
        _logger.debug(cmd)
        r = _delegator.run(cmd)
        return_msg = "OK" if r.return_code == 0 else "ERROR"
        _logger.debug("Verify: " + return_msg)

        if r.return_code == 0:
            for k in self.cache.keys():
                # NOTE: Python 3.5 shutil.copy does not accept pathlib.Path
                _shutil.copy(str(self.cache[k]), str(self.base_image['dir']))
                self.base_image[k] = self.base_image['dir'] / self.file[k]
        else:
            _logger.error("Can not verify " + self.file['hash'])
            _sys.exit(_os.EX_DATAERR)

    def ubuntu_hash_version(self):
        """
        Ubuntu - Parse and extract version information from hash file

        Parses version information from configuration and extracts the full
        version ``yy.mm.patch`` from ``SHA256SUMS`` from the local keyring.

        The function can extend the configured version from ``yy.mm`` into
        ``yy.mm.patch`` for easier upstream tracking. It can also convert
        from codenames (ex. ``xenial``) to ``yy.mm.patch`` (ex. ``16.04.6``).

        Finally this function constructs the url of the Ubuntu release from
        the version and variant configuration.
        """
        _logger.debug("ubuntu_hash_version")
        target = {}

        # If version in ``image: {{ distro }}/{{version}}`` from config
        # is in the format `yy.mm.patch` (ex. 16.04.6)
        match = _re.match(r'^(\d+)\.(\d+)\.(\d+)$',self.base_image['version'])
        if match:
            target['yy'] = match.group(1)
            target['mm'] = match.group(2)
            target['patch'] = match.group(3)
            target['version'] = self.base_image['version']
            self.base_image['release_version'] = self.base_image['version']

        # Parse `~/.cache/ryo-iso/SHA256SUMS` to determine the latest patch release
        regex = _re.compile(r'^([0-9A-Fa-f]{64}) \*'+self.base_image['distro']+"-"+r'(\d+)\.(\d+)\.?(\d?)'+"-"+self.iso_cfg['variant']+"-"+self.iso_cfg['arch']+".iso$")
        _logger.debug("Regex: " + str(regex))
        latest = {}
        latest_hash = None
        with open(str(self.cache['hash']),'r') as f:
            for line in f:
                # _logger.debug(line)
                match = regex.search(line)
                if match:
                    # NOTE: `SHA256SUMS` should only contain one yy.mm
                    latest['yy'] = match.group(2)
                    latest['mm'] = match.group(3)
                    if not latest.get('patch') or match.group(4) > latest['patch']:
                        latest['patch'] = match.group(4)
                        latest_hash = match.group(1)
                    latest['version'] = (latest['yy']
                                         + "." + latest['mm']
                    )
                    if (latest['patch'] != ""):
                        latest['version'] = latest['version'] + "." + latest['patch']
                    if target == latest:
                        break
        _logger.debug("Latest Version: " + latest['version'])

        current = self.base_image['release_url'].startswith('http://releases.ubuntu.com/')
        # If the target version is not the latest version switch to the release archive
        # TODO: Validate this codepath, lol.

        if target and target != latest and current:
            _logger.warning("Newer release version available")
            self.base_image['release_url'] = (
                'http://old-releases.ubuntu.com/releases/'
                + self.base_image['codename'] + '/')
            self.ubuntu_hash_cache()
            self.ubuntu_hash_check()
            self.ubuntu_hash_version()
            #self.base_image['release_version'] = self.base_image['version']
        else:
            self.base_image['release_version'] = latest['version']
            self.base_image['hash'] = latest_hash
            _logger.debug("Base Image Release Version: " + self.base_image['release_version'])
            _logger.debug("Base Image Hash: " + self.base_image['hash'])

            with (self.build_dir/'.release_version').open('w') as f:
                f.write(self.base_image['release_version'])

            with (self.build_dir/'.hash').open('w') as f:
                f.write(self.base_image['hash'])

            self.base_image['file'] = ("ubuntu-"
                + self.base_image['release_version']
                + "-" + self.iso_cfg['variant']
                + "-" + self.iso_cfg['arch']
                + ".iso"
            )
            self.base_image['path'] = self.base_image['dir'] / self.base_image['file']
            self.base_image['url'] = self.base_image['release_url'] + self.base_image['file']
            r = _requests.head(self.base_image['url'])
            self.base_image['size'] = int(r.headers['content-length'])

    def ubuntu_base_image_check(self):
        """
        Ubuntu - Verify the SHA256SUM of the upstream ISO image

        This function runs ``sha256sum -c`` on ``self.build_dir/'base_image.iso'``
        """
        # TODO: refactor out echo
        cmd = ('echo "'+self.base_image['hash']+" *"+self.base_image['file']+'"'
               + ' | sha256sum -c')
        _logger.debug(cmd)
        r = _delegator.run(cmd, cwd=str(self.base_image['dir']))
        valid = self.base_image['file']+": OK"
        if r.return_code == 0:
            for line in r.out.split('\n'):
                _logger.debug(line)
                if valid == line:
                    return_msg = "OK"
                    _logger.info("Verify: " + return_msg)
                    _os.symlink(str(self.base_image['path']),str(self.build_dir/'base_image.iso'))
                    return
        return_msg = "ERROR"
        _logger.error("Can not verify " + self.file['file'])
        _sys.exit(_os.EX_DATAERR)

    def ubuntu_update(self):
        # Update SHA256SUM 
        # curl --list-only ftp://releases.ubuntu.com/releases/16.04/
        # curl -s --remote-name http://releases.ubuntu.com/xenial/SHA256SUMS.gpg
        # http://old-releases.ubuntu.com/releases/xenial/SHA256SUMS
        # http://releases.ubuntu.com/xenial/ubuntu-16.04.6-desktop-amd64.iso
        print("STUB ubuntu_update()")
