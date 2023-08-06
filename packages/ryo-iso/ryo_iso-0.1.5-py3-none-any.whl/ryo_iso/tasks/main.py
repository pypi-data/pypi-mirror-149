import os as _os
import sys as _sys
import glob as _glob
import subprocess as _subprocess
import time as _time
import shlex as _shlex
import doit as _doit
import shutil as _shutil
import importlib_resources as _resources
from pathlib import Path as _Path
from contextlib import contextmanager as _contextmanager
from loguru import logger as _logger

from ryo_iso.tasks.init import task_init
import ryo_iso.config as _config
import ryo_iso.utils as _utils

DOIT_CONFIG = {
    'backend': 'json',
    'default_tasks': ['build'],
    'verbosity': 2,
    'failure_verbosity': 0
}

# If config context is defined
if _config._ctx is not None:
    _ctx = _config._ctx
    # Initialize Logger
    _logger.remove()
    if 'LOGURU_LEVEL' not in _os.environ.keys() and not _ctx['config'].app_cfg['debug']:
        # FIXME: Remove before flight
        _logger.add(_sys.stderr, level="WARNING")
    else:
        _logger.add(_sys.stderr, level="DEBUG")

    # Import progress bar or no-op.
    if not _ctx['config'].app_cfg['progress']:
        @_contextmanager
        def _tqdm(*args, **kwargs):
            if args:
                yield args[0]
            yield kwargs.get('iterable', None)
    else:
        from tqdm import tqdm as _tqdm

def task__reset_sudo_timestamp():
    """
    Reset ``sudo`` timestamp

    Invalidate credential cache

    :actions:
      - ``sudo -k``
      - ``sudo true``
    """
    return {
        'actions': ["sudo -k",
                    "sudo true"],
    }

def task__debug_config():
    """
    Debug configuration information

    Dump composited config

    :actions:
      - :func:`task__debug_config.print_debug`
    """
    def print_debug(targets):
        print(repr(_ctx['config']))

    return {
        'actions': [print_debug],
    }

def task__build_init():
    """
    Setup build directories

    Creates ``./build/log`` and ``./build/backup``

    :actions:
      - _doit.tools.create_folder, ['build/log']
      - _doit.tools.create_folder, ['build/backup']
    :targets:
      - build/log
      - build/backup
    """
    return {
        'actions': [(_doit.tools.create_folder, ['build/log']),
                    (_doit.tools.create_folder, ['build/backup'])],
        'targets': ['build/log','build/backup'],
    }

def task__hash_cache():
    """
    Cache latest upstream ISO hashes

    Download SHA256SUMS* to $XDG_CACHE_HOME/ryo-iso/

    :actions:
      - _ctx['config'].distro_hash_cache
      - :func:`ryo_iso.config.Config.ubuntu_hash_cache`
    :task_dep:
      - :func:`task__build_init`
    :targets:
      - ~/.cache/ryo-iso/SHA256SUMS
      - ~/.cache/ryo-iso/SHA256SUMS.gpg
    """
    return {
        'actions': [_ctx['config'].distro_hash_cache],
        'task_dep': ['_build_init'],
        'targets': list(_ctx['config'].cache.values()),
    }

def task__hash_check():
    """
    Check cached upstream ISO hashes

    Validate GPG signature for checksums in $XDG_CACHE_HOME/ryo-iso/

    :actions:
      - _ctx['config'].distro_hash_check
      - :func:`ryo_iso.config.Config.ubuntu_hash_check`
    :file_dep:
      - '~/.cache/ryo-iso/SHA256SUMS'
      - '~/.cache/ryo-iso/SHA256SUMS.gpg'
    :uptodate:
      - _doit.tools.result_dep(:func:`task__hash_cache`)
    """
    return {
        'actions': [_ctx['config'].distro_hash_check],
        'file_dep': list(_ctx['config'].cache.values()),
        'uptodate': [_doit.tools.result_dep('_hash_cache')],
    }

def task__hash_version():
    """
    Extract latest version information from the hash

    Locates the implicit full release version with fallback for archived releases

    :actions:
      - _ctx['config'].distro_hash_version
      - :func:`ryo_iso.config.Config.ubuntu_hash_version`
    :uptodate:
      - _doit.tools.result_dep(:func:`task__hash_check`)
    """
    return {
        'actions': [_ctx['config'].distro_hash_version],
        'uptodate': [_doit.tools.result_dep('_hash_check')],
    }

def task__base_image_download():
    """
    Download base ISO images

    The download directory for the base ISO image is configured in
    ``$XDG_CONFIG_HOME/ryo-iso/config.yml``; it defaults to
    ``distro_image_dir: ~/Downloads`` and is symlinked to ``base_image.iso``
    in the project directory.

    Enable/disable progress indicator via the ``progress`` parameter in
    :ref:`config.yml`

    :actions:
      - :func:`task__base_image_download.download_iso`
    :uptodate:
      - _doit.tools.result_dep(:func:`task__hash_version`)
    """
    def download_iso():
        """
        ISO downloader

        curl ISO dowload subprocess with resume and optional
        progress reporting.
        """

        iso_path = _ctx['config'].base_image['path']
        iso_size = _ctx['config'].base_image['size']
        iso_url = _ctx['config'].base_image['url']

        # TODO: Resume partial downloads
        if iso_path.is_file():
            _logger.debug("Base Image previously downloaded")
        else:
            cmd = "curl -J -C - --silent --remote-name " + iso_url
            with _tqdm(desc=iso_path.name,
                       total=iso_size, unit='byte', unit_scale=True,
                       ascii=False) as status:
                # FIXME: Error checking
                with _subprocess.Popen(_shlex.split(cmd), bufsize=0,
                                       cwd=str(iso_path.parent),
                                       stdout=_subprocess.DEVNULL,
                                       stderr=_subprocess.DEVNULL) as proc:
                    while proc.poll() is None:
                        if status and iso_path.is_file():
                            # Update progress bar
                            status.n = iso_path.stat().st_size
                            status.update(0)
                        _time.sleep(1)
                    if status:
                        # Set progress bar to 100%
                        status.n = iso_size
                        status.update(0)

    return {
        'actions': [download_iso],
        'uptodate': [_doit.tools.result_dep('_hash_version')],
    }

def task__base_image_check():
    """
    Check base ISO image hash

    Validate the base ISO image SHA256 checksum

    :actions:
      - _logger.debug, ["validate base ISO"]
      - :func:`ryo_iso.utils.profile_start`
      - _ctx['config'].distro_base_image_check,
      - :func:`ryo_iso.config.Config.ubuntu_base_image_check`
      - :func:`ryo_iso.utils.profile_stop`
    :task_dep:
      - :func:`task__build_init`
    :targets:
      - base_image.iso
    :uptodate:
      - True
    """
    return {
        'actions': [(_logger.debug, ["validate base ISO"]),
                    _utils.profile_start,
                    _ctx['config'].distro_base_image_check,
                    _utils.profile_stop],
        'task_dep': ['_base_image_download'],
        'targets': ['base_image.iso'],
        'uptodate': [True],
    }

def task__base_mbr_extract():
    """
    Extract MBR partition from base ISO image

    Extract MBR partition on Ubuntu Jammy or later...

    :actions:
      - _logger.debug, ["extract MBR"]
      - :func:`ryo_iso.utils.profile_start`
      - ``dd if=base_image.iso bs=1 count=446 of=base_image.mbr``
      - :func:`ryo_iso.utils.profile_stop`

    :file_dep:
      - base_image.iso
    :targets:
      - base_image.mbr
    :uptodate:
      - True
    """

    # TODO: This should probably use a calver compare, but there is some time before an alphabet overflow issue
    task_log = _Path('build/log/mbr_extract.log')
    # FIXME: Ubuntu specific code
    if _ctx['config'].base_image['codename'] >= 'jammy':
        return {
            'actions': [(_logger.debug, ["extract MBR"]),
                        _utils.profile_start,
                        'dd if=base_image.iso bs=1 count=446 of=base_image.mbr'
                        ' > %s 2>&1' % task_log,
                        _utils.profile_stop],
            'file_dep': ['base_image.iso'],
            'targets': ['base_image.mbr'],
            'uptodate': [True]
        }
    else:
        return {
            'actions': None,
            # 'file_dep': ['base_image.iso']
        }

def task__base_efi_extract():
    """
    Extract EFI partition from base ISO image

    Extract EFI partition on Ubuntu Jammy or later...

    :actions:
      - _logger.debug, ["extract EFI"]
      - :func:`ryo_iso.utils.profile_start`
      - ``dd if=base_image.iso of=base_image.efi``
      - :func:`ryo_iso.utils.profile_stop`

    :file_dep:
      - base_image.iso
    :targets:
      - base_image.efi
    :uptodate:
      - True
    """

    pass

    # TODO: Implement Internal feature flags? Move this from being a task to being a library?
    # FIXME: Ubuntu specific code
    task_log = _Path('build/log/efi_extract.log')
    if _ctx['config'].base_image['codename'] >= 'jammy':
        return {
            'actions': [(_logger.debug, ["extract EFI"]),
                        _utils.profile_start,
                        'dd if=base_image.iso bs=512'
                        ' skip="$(sfdisk --json base_image.iso | jq .partitiontable.partitions[1].start)"'
                        ' count="$(sfdisk --json base_image.iso | jq .partitiontable.partitions[1].size)"'
                        ' of=base_image.efi'
                        ' > %s 2>&1' % task_log,
                        _utils.profile_stop],
            'file_dep': ['base_image.iso'],
            'targets': ['base_image.efi'],
            'uptodate': [True]
        }
    else:
        return {
            'actions': None,
            # 'file_dep': ['base_image.iso']
        }


def task__base_image_extract():
    """
    Extract files from base ISO image

    Extract ISO image to ``./image`` in the project directory

    :actions:
      - _logger.debug, ["extract image"]
      - :func:`ryo_iso.utils.profile_start`
      - ``sudo xorriso -osirrox on -indev base_image.iso -extract / image``
      - :func:`ryo_iso.utils.profile_stop`

    :file_dep:
      - base_image.iso
    :targets:
      - image/.disk/base_installable
    :uptodate:
      - True
    """
    task_log = _Path('build/log/base_image_extract.log')
    return {
        'actions': [(_logger.debug, ["extract image"]),
                    _utils.profile_start,
                    'sudo xorriso -osirrox on -indev base_image.iso -extract / image'
                    ' > %s 2>&1' % task_log,
                    _utils.profile_stop],
        'file_dep': ['base_image.iso'],
        'task_dep': ['_base_mbr_extract','_base_efi_extract'],
        'targets': ['image/.disk/base_installable'],
        'uptodate': [True],
    }


def task__squashfs_extract():
    """
    Extract files from squashfs

    Extract squashfs to ``./squashfs-root`` in project directory

    :actions:
      - _logger.debug, ["extract squashfs"]
      - :func:`ryo_iso.utils.profile_start`
      - ``sudo unsquashfs image/casper/filesystem.squashfs``
      - :func:`ryo_iso.utils.profile_stop`
    :file_dep:
      - base_image.iso
      - image/.disk/base_installable
    :targets:
      - squashfs-root/etc/os-release
    """
    # TODO: Generate progress bar using `image/casper/filesystem.size`
    task_log = _Path('build/log/squashfs_extract.log')
    return {
        'actions': [(_logger.debug, ["extract squashfs"]),
                    _utils.profile_start,
                    'sudo unsquashfs image/casper/filesystem.squashfs'
                    ' > %s 2>&1' % task_log,
                    _utils.profile_stop],
        'file_dep': ['base_image.iso','image/.disk/base_installable'],
        'targets': ['squashfs-root/etc/os-release']
    }


@_doit.create_after(executed='_squashfs_extract')
def task__mount_dev():
    """
    Mount pseudo-filesystems in squashfs-root

    Mount /proc, /dev, /sys mountpoints inside squashfs-root

    :actions:
      - ``sudo mount %s %s %s``
    """
    yield {
        'name': None,
        'doc': 'Mount pseudo-filesystems in squashfs',
        'task_dep': ['_squashfs_extract'],
    }
    mnt = ({"src":"/dev", "dst":"squashfs-root/dev", "opt":"--bind"},
           {"src":"/dev/pts", "dst":"squashfs-root/dev/pts", "opt":"--bind"},
           {"src":"none", "dst":"squashfs-root/proc", "opt":"-t proc"},
           {"src":"none", "dst":"squashfs-root/sys", "opt":"-t sysfs"},)
           # NOTE: This mounts on the second try, not sure if actually needed.
           # {"src":"none","dst":"squashfs-root/proc/sys/fs/binfmt_misc","opt":"-t binfmt_misc"}
    for mount in mnt:
        if _os.path.isdir(mount['dst']) and not _os.path.ismount(mount['dst']):
            yield {
                'name': mount['dst'],
                'actions': ['sudo mount %s %s %s' % (mount['opt'],
                                                     mount['src'],
                                                     mount['dst'])]
            }

def task__umount_dev():
    """
    Unmount pseudo-filesystems from squashfs-root

    Unmount /proc, /dev, /sys mountpoints inside squashfs-root

    :actions:
      - :func:`ryo_iso.utils.umount_dev`
    :uptodate:
      - False
    """
    return {
        'actions': [_utils.umount_dev],
        'uptodate': [False],
    }

def task__squashfs_backup():
    """
    Backup files from image/squashfs

    Backup files to be restored after updating image/squashfs

    :actions:
      - ``sudo cp image/preseed/ubuntu.seed build/backup/ubuntu.seed``
      - ``sudo cp squashfs-root/etc/apt/sources.list build/backup/sources.list``
      - ``sudo mv squashfs-root/etc/resolv.conf squashfs-root/etc/resolv.conf.orig``
    :targets:
      - build/backup/ubuntu.seed
      - build/backup/sources.list
      - squashfs-root/etc/resolv.conf.orig
    :task_dep:
      - :func:`task__mount_dev`
    :uptodate:
      - True
    """
    return {
        'actions': ['sudo cp image/preseed/ubuntu.seed build/backup/ubuntu.seed || true',
                    'sudo cp squashfs-root/etc/apt/sources.list build/backup/sources.list',
                    'sudo mv squashfs-root/etc/resolv.conf squashfs-root/etc/resolv.conf.orig'],
        'targets': ['build/backup/sources.list',
                    'squashfs-root/etc/resolv.conf.orig'],
        'task_dep': ['_mount_dev'],
        'uptodate': [True],
    }

def task__squashfs_uname():
    """
    Patch ``uname`` in squashfs-root

    Monkey patches ``uname`` inside the chroot to report chrooted kernel version

    :actions:
      - ``sudo cp squashfs-root/bin/uname squashfs-root/bin/uname.orig``
      - :func:`task__squashfs_uname.patch`
      - ``sudo mv squashfs-root/tmp/uname squashfs-root/bin/uname``
    :targets:
      - squashfs-root/bin/uname.orig
    :task_dep:
      - :func:`task__squashfs_backup`
    """
    def patch():
        """
        Monkey patch ``uname``
        """
        uname_path = _Path("squashfs-root/tmp/uname")
        with _resources.path("ryo_iso.data", 'uname') as patched_uname:
            _logger.debug("Install %s to %s"%(patched_uname, uname_path))
            # NOTE: Python 3.5 shutil.copy does not accept pathlib.Path
            _shutil.copy(str(patched_uname),str(uname_path))

    return {
        'actions': ['sudo cp squashfs-root/bin/uname squashfs-root/bin/uname.orig',
                    patch,
                    'sudo mv squashfs-root/tmp/uname squashfs-root/bin/uname'],
        'targets': ['squashfs-root/bin/uname.orig'],
        'task_dep': ['_squashfs_backup'],
    }

def task__squashfs_modinfo():
    """
    Patch ``modinfo`` in squashfs-root

    Patches ``modinfo`` inside the chroot to report chrooted kernel version

    :actions:
      - ``sudo mv squashfs-root/sbin/modinfo squashfs-root/bin/modinfo``
      - :func:`task__squashfs_modinfo.patch`
      - ``sudo mv squashfs-root/tmp/modinfo squashfs-root/sbin/modinfo``
    :targets:
      - squashfs-root/bin/modinfo
    :task_dep:
      - :func:`task__squashfs_uname`
    """
    def patch():
        uname_path = _Path("squashfs-root/tmp/modinfo")
        with _resources.path("ryo_iso.data", 'modinfo') as patched_uname:
            _logger.debug("Install %s to %s"%(patched_uname, uname_path))
            # NOTE: Python 3.5 shutil.copy does not accept pathlib.Path
            _shutil.copy(str(patched_uname),str(uname_path))

    # NOTE: modinfo is a multi-call binary symlinked to kmod and must have the same name
    return {
        'actions': ['sudo mv squashfs-root/sbin/modinfo squashfs-root/bin/modinfo',
                    patch,
                    'sudo mv squashfs-root/tmp/modinfo squashfs-root/sbin/modinfo'],
        'targets': ['squashfs-root/bin/modinfo'],
        'task_dep': ['_squashfs_uname'],
    }

def task__squashfs_resolv():
    """
    Install resolv.conf into squashfs-root

    Installs the local resolv.conf into squashfs-root to enable chrooted networking.

    :actions:
      - ``sudo cp /etc/resolv.conf squashfs-root/etc/resolv.conf``
    :targets:
      - squashfs-root/etc/resolv.conf
    :task_dep:
      - :func:`task__squashfs_modinfo`
    :uptodate:
      - _doit.tools.check_timestamp_unchanged('squashfs-root/etc/resolv.conf')
    """
    return {
        'actions': ['sudo cp /etc/resolv.conf squashfs-root/etc/resolv.conf'],
        'targets': ['squashfs-root/etc/resolv.conf'],
        'task_dep': ['_squashfs_modinfo'],
        'uptodate': [True],
    }

def task__squashfs_apt_proxy():
    """
    Enable APT proxy

    Enable APT proxy while chrooted into squashfs-root

    :actions:
      - ``echo 'Acquire::http { Proxy \"http://localhost:3142\"; };' | sudo tee squashfs-root/etc/apt/apt.conf.d/01proxy``
    :targets:
      - squashfs-root/etc/apt/apt.conf.d/01proxy
    :task_dep:
      - :func:`task__mount_dev`
    :uptodate:
      - True
    """
    if 'apt' in _ctx['config'].iso_cfg.keys():
        return {
            'actions': ["echo 'Acquire::http { Proxy \"http://localhost:3142\"; };'"
                        ' | sudo tee squashfs-root/etc/apt/apt.conf.d/01proxy'
                        ' > /dev/null'],
            'targets': ['squashfs-root/etc/apt/apt.conf.d/01proxy'],
            'task_dep': ['_mount_dev'],
            'uptodate': [True],
        }

def task__squashfs_apt_key():
    """
    Install APT keys into squashfs

    Installs APT keys from ``./keys`` into squashfs-root
    Migrate to keys in ``/usr/share/keyrings``
    ``deb [arch=amd64 signed-by=/usr/share/keyrings/repo-keyring.gpg] http://repo.example.org/ ubuntu jammy main``

    :actions:
      - ``sudo cp keys/*.gpg squashfs-root/...``
    :targets:
      - ``squashfs-root/.../*.gpg``
    :uptodate:
      - True
    """
    keys = _glob.glob("keys/*.gpg")
    # FIXME: Ubuntu specific code
    if _ctx['config'].base_image['codename'] >= 'jammy':
        keyring_dir = "squashfs-root/usr/share/keyrings"
    else:
        keyring_dir = "squashfs-root/etc/apt/trusted.gpg.d"

    for key in keys:
        key = key.split('/')[1]
        yield {
            'name': key,
            'actions': ['sudo cp keys/%s %s' % (key, keyring_dir)],
            'targets': ['%s/%s' % (keyring_dir, key)],
            'uptodate': [True],
        }

def task__squashfs_apt_repo():
    """
    Install custom APT repositories

    Add repositories to ``/etc/apt`` in squashfs-root
    """
    task_log = _Path('build/log/squashfs_apt_repo.log')
    components = ['main','restricted','universe','multiverse']

    if ('apt' in _ctx['config'].iso_cfg.keys()
        and 'repository' in _ctx['config'].iso_cfg['apt'].keys()):

        repos = _ctx['config'].iso_cfg['apt']['repository']

        # Order dependencies if ``/etc/apt/sources.list`` is being updated
        src_files = filter(_os.path.isfile,repos)
        sources = list(filter(lambda f: _Path(f).name == 'sources.list',src_files))
        if len(sources) == 0:
            update = None
        elif len(sources) == 1:
            update = sources[0]
        else:
            _logger.error("Multiple sources.list configured " + repr(sources))
            _sys.exit(_os.EX_CONFIG)

        yield {
            'name': None,
            'doc': 'Install custom APT repositories',
        }
        for repo in repos:
            if (repo in components
                or repo.startswith("ppa:")
                or repo.startswith("deb ")
                or repo.startswith("deb-src ")):
                yield {
                    'name': repo,
                    'actions': [(_logger.debug, ['Adding repository: %s' % repo]),
                                'sudo chroot squashfs-root add-apt-repository'
                                ' --yes "%s" >> %s 2>&1' % (repo,task_log)],
                    # Ensure that sources.list is updated before add-apt-repository is run
                    'task_dep': ['_squashfs_apt_repo:%s' % update if update else '_squashfs_apt_key','_squashfs_resolv'],
                    'uptodate': [False],
                }
            elif _os.path.isfile(repo):
                if _Path(repo).name == 'sources.list':
                    yield {
                        'name': repo,
                        'actions': [(_logger.debug, ["Updating sources.list: %s" % _Path(repo).name]),
                                    'sudo cp %s squashfs-root/etc/apt/sources.list' % repo],
                        'targets': ['squashfs-root/etc/apt/sources.list'],
                        'task_dep': ['_squashfs_apt_key'],
                        'uptodate': [_doit.tools.check_timestamp_unchanged('squashfs-root/etc/apt/sources.list')],
                    }
                else:
                    yield {
                        'name': repo,
                        'actions': [(_logger.debug, ['Adding to sources.list.d: %s' % _Path(repo).name]),
                                    'sudo cp %s squashfs-root/etc/apt/sources.list.d/.' % repo],
                        'targets': ['squashfs-root/etc/apt/sources.list.d/%s' % _Path(repo).name],
                        'task_dep': ['_squashfs_apt_key'],
                        'uptodate': [_doit.tools.check_timestamp_unchanged('squashfs-root/etc/apt/sources.list.d')],
                    }
            else:
                _logger.error("Configuration error: "+repo)
                _sys.exit(_os.EX_CONFIG)

@_doit.create_after(executed='_mount_dev')
def task__squashfs():
    """
    Setup squashfs-root meta-task

    Calls all of the sub-tasks for setup of squashfs-root

    :task_dep:
      - :func:`task__squashfs_extract`
      - :func:`task__mount_dev`
      - :func:`task__squashfs_backup`
      - :func:`task__squashfs_uname`
      - :func:`task__squashfs_modinfo`
      - :func:`task__squashfs_resolv`
      - :func:`task__squashfs_apt_proxy`
      - :func:`task__squashfs_apt_key`
      - :func:`task__squashfs_apt_repo`
    """
    return {
        'actions': None,
        'task_dep': ['_squashfs_extract',
                     '_mount_dev',
                     '_squashfs_backup',
                     '_squashfs_uname',
                     '_squashfs_modinfo',
                     '_squashfs_resolv',
                     '_squashfs_apt_proxy',
                     '_squashfs_apt_key',
                     '_squashfs_apt_repo'],
    }

def task__chroot_apt_up():
    """
    Chroot APT update & upgrade

    Chroot into squashfs-root and run ``apt update`` and ``apt-upgrade``

    :actions:
      - _logger.debug, ["apt update/upgrade"]
      - :func:`ryo_iso.utils.profile_start`
      - ``sudo chroot squashfs-root apt-get update -y``
      - ``sudo chroot squashfs-root apt-get upgrade -y``
      - :func:`ryo_iso.utils.profile_stop`
    :task_dep:
      - :func:`task__squashfs`
    :uptodate:
      - _doit.tools.check_timestamp_unchanged('squashfs-root/etc/apt')
      - _doit.tools.check_timestamp_unchanged('squashfs-root/etc/apt/sources.list.d')
    """
    task_log = _Path('build/log/chroot_apt_up.log')
    return {
        'actions': [(_logger.debug, ["apt update/upgrade"]),
                    _utils.profile_start,
                    'sudo chroot squashfs-root apt-get update -y'
                    ' > %s 2>&1' % task_log,
                    'sudo chroot squashfs-root apt-get upgrade -y'
                    ' >> %s 2>&1' % task_log,
                    _utils.profile_stop],
        'task_dep': ['_squashfs'],
        'uptodate': [_doit.tools.check_timestamp_unchanged('squashfs-root/etc/apt'),
                     _doit.tools.check_timestamp_unchanged('squashfs-root/etc/apt/sources.list.d')],
    }

def task__chroot_apt_purge():
    """
    Chroot and purge APT packages

    Purges debian packages from squashfs-root chroot

    :actions:
      - _logger.debug, ["apt purge: "+pkg]
      - ``sudo chroot squashfs-root apt-get purge -y %s``
    :task_dep:
      - :func:`task__chroot_apt_up`
    """
    task_log = _Path('build/log/chroot_apt_purge.log')
    # NOTE: Purging is unordered
    if ('apt' in _ctx['config'].iso_cfg.keys()
        and 'purge' in _ctx['config'].iso_cfg['apt'].keys()):

        pkgs = _ctx['config'].iso_cfg['apt']['purge']
        for pkg in pkgs:
            yield {
                'name': pkg,
                'actions': [(_logger.debug, ["apt purge: "+pkg]),
                            'sudo chroot squashfs-root apt-get purge -y %s'
                            #' >> %s 2>&1' % (pkg,task_log)],
                            ' >> %s' % (pkg,task_log)],
                'task_dep': ['_chroot_apt_up'],
            }

def task__chroot_apt_install():
    """
    Chroot and install APT packages

    Installs debian packages into squashfs-root chroot
    """
    task_log = _Path('build/log/chroot_apt_install.log')
    # TODO: Config support for `--no-install-recommends --no-upgrade`
    if ('apt' in _ctx['config'].iso_cfg.keys()
        and 'install' in _ctx['config'].iso_cfg['apt'].keys()):

        yield {
            'name': None,
            'doc': 'Chroot and install APT packages',
        }
        yield {
            'name': 'setup',
            'actions': [_utils.profile_start],
            'task_dep': ['_chroot_apt_purge'],
        }

        pkgs = _ctx['config'].iso_cfg['apt']['install']
        prev = None
        for pkg in pkgs:
            yield {
                'name': pkg,
                'actions': [(_logger.debug, ["apt install: "+pkg]),
                            'sudo chroot squashfs-root apt-get install -y %s'
                            ' < /dev/null >> %s 2>&1' % (pkg,task_log)],
                # Chain sub-tasks in DAG for ordered install
                'task_dep': ['_chroot_apt_install:%s' % prev if prev else '_chroot_apt_purge'],
            }
            prev = pkg

        yield {
            'name': 'teardown',
            'getargs': {'start': ('_chroot_apt_install:setup', 'start')},
            'actions': [_utils.profile_stop],
            'task_dep': ['_chroot_apt_install:%s'%prev if prev else '_chroot_apt_install:start'],
        }

def task__chroot_dpkg_install():
    """
    Chroot and install Debian packages

    Installs local debian packages into squashfs-root chroot

    :actions:
      - _logger.debug, ["dpkg Install: "+pkg]
      - ``sudo cp dpkg/%s squashfs-root%s``
      - ``sudo chroot squashfs-root dpkg -i %s/%s``
    :targets:
      - squashfs-root/var/cache/apt/archives/%s
    :task_dep:
      - :func:`task__chroot_apt_install`
    """
    task_log = _Path('build/log/chroot_dpkg_install.log')
    if ('dpkg' in _ctx['config'].iso_cfg.keys()
        and 'install' in _ctx['config'].iso_cfg['dpkg'].keys()):

        # TODO: Make this configurable
        dst = "/var/cache/apt/archives"

        pkgs = _ctx['config'].iso_cfg['dpkg']['install']
        prev = None
        for pkg in pkgs:
            yield {
                'name': pkg,
                'actions': [(_logger.debug, ["dpkg Install: "+pkg]),
                            'sudo cp dpkg/%s squashfs-root%s' % (pkg,dst),
                            'sudo chroot squashfs-root dpkg -i %s/%s'
                            ' >> %s 2>&1' % (dst,pkg,task_log)],
                'targets': ['squashfs-root%s/%s' % (dst,pkg)],
                # Chain sub-tasks in DAG for ordered install
                'task_dep': ['_chroot_dpkg_install:%s'%prev if prev else '_chroot_apt_install'],
            }
            prev = pkg

def task__chroot_pip_cache():
    """
    Chroot and update pip cache

    Pre-load Python packages into squashfs-root chroot pip cache
    """
    pip_dir = _Path('./python-wheels/')
    if ('pip' in _ctx['config'].iso_cfg.keys()
        and pip_dir.is_dir()):

        pip_cache = _ctx['config'].iso_cfg['pip']['cache']
        return {
            'actions': ['sudo chroot squashfs-root mkdir -p %s' % pip_cache,
                        'sudo cp -r %s squashfs-root/%s/wheels' % (pip_dir,pip_cache)],
            'task_dep': ['_chroot_dpkg_install','_chroot_apt_install'],
        }
    else:
        return {
            'actions': None,
            'task_dep': ['_chroot_dpkg_install','_chroot_apt_install'],
        }

def task__chroot_pip_install():
    """
    Chroot and install pip packages

    Installs debian packages into squashfs-root chroot
    """
    task_log = _Path('build/log/chroot_pip_install.log')
    # TODO: pip2 support, lol.
    if ('pip' in _ctx['config'].iso_cfg.keys()
        and 'install' in _ctx['config'].iso_cfg['pip'].keys()):

        yield {
            'name': None,
            'doc': 'Chroot and install pip packages',
        }
        yield {
            'name': 'setup',
            'actions': [_utils.profile_start],
        }

        target = _ctx['config'].iso_cfg['pip']['target']
        cmd = "sudo chroot squashfs-root pip3 install"
        cmd += ' --verbose --upgrade --prefix=/usr/local'
        pkgs = _ctx['config'].iso_cfg['pip']['install']

        prev = None
        for pkg in pkgs:
            yield {
                'name': pkg,
                'actions': [(_logger.debug, ["pip install: "+pkg]),
                            '%s %s >> %s 2>&1' % (cmd,pkg,task_log)],
                'task_dep': ['_chroot_pip_install:%s'%prev if prev else '_chroot_pip_cache'],
            }
            prev = pkg

        yield {
            'name': 'teardown',
            'getargs': {'start': ('_chroot_pip_install:setup', 'start')},
            'actions': [_utils.profile_stop],
            'task_dep': ['_chroot_pip_install:%s'%prev if prev else '_chroot_pip_install:start'],
        }

def task__chroot_pip_local():
    """
    Chroot and install local pip packages from wheels

    Installs Python packages into squashfs-root chroot
    """
    task_log = _Path('build/log/pip_local.log')
    if ('pip' in _ctx['config'].iso_cfg.keys()
        and 'local' in _ctx['config'].iso_cfg['pip'].keys()):

        pip_cache = _ctx['config'].iso_cfg['pip']['cache']
        target = _ctx['config'].iso_cfg['pip']['target']
        cmd = "sudo chroot squashfs-root pip3 install"
        cmd += " --upgrade --prefix=/usr/local"
        cmd += " --no-index --find-links=%s/wheels" % (pip_cache)
        pkgs = _ctx['config'].iso_cfg['pip']['local']

        prev = None
        for pkg in pkgs:
            yield {
                'name': pkg,
                'actions': [(_logger.debug, ["pip local: "+pkg]),
                            '%s %s >> %s' % (cmd,pkg,task_log)],
                'task_dep': ['_chroot_pip_local:%s'%prev if prev else '_chroot_pip_cache'],
            }
            prev = pkg

def task__chroot_patch():
    """
    Apply patch script

    If all else fails insert kludges here
    .. note:: The :ref:`patch <patch>` script is run outside of the chroot

    **if ('patch' in _ctx['config'].iso_cfg.keys()):**
      :actions:
        - _logger.debug, ["Applying patch script"]
        - ``patch.bash`` # as defined in iso.yml
    **else:**
      :actions:
        - None

    :task_dep:
      - :func:`task__chroot_apt_install`
      - :func:`task__chroot_dpkg_install`
      - :func:`task__chroot_pip_install`
      - :func:`task__chroot_pip_local`
    """
    task_log = _Path('build/log/patch.log')
    if ('patch' in _ctx['config'].iso_cfg.keys()):

        patch = _ctx['config'].iso_cfg['patch']

        return {
            'actions': [(_logger.debug, ["Applying patch script"]),
                        '%s > %s 2>&1' % (patch,task_log)],
            'task_dep': ['_chroot_apt_install',
                         '_chroot_dpkg_install',
                         '_chroot_pip_install',
                         '_chroot_pip_local'],
        }

    else:
        return {
            'actions': None,
            'task_dep': ['_chroot_apt_install',
                         '_chroot_dpkg_install',
                         '_chroot_pip_install',
                         '_chroot_pip_local'],
        }

@_doit.create_after(executed='_squashfs')
def task__chroot():
    """
    Chrooted meta-task

    Calls all of the sub-tasks applied inside the squashfs-root chroot
    """
    return {
        'actions': ['sudo mv squashfs-root/etc/resolv.conf.orig squashfs-root/etc/resolv.conf',
                    'sudo rm -f squashfs-root/etc/apt/apt.conf.d/01proxy',
                    'sudo rm -f squashfs-root/var/cache/apt/archives/*.deb',
                    'sudo rm -f squashfs-root/*.old',
                    'sudo mv squashfs-root/bin/uname.orig squashfs-root/bin/uname',
                    'sudo mv squashfs-root/bin/modinfo squashfs-root/sbin/modinfo',
                    'sudo cp build/backup/sources.list squashfs-root/etc/apt/sources.list',
                    'sudo rm -rf squashfs-root/home/*',
                    'sudo rm -rf squashfs-root/root/.cache'],
        'task_dep': ['_squashfs',
                     '_chroot_apt_up',
                     '_chroot_apt_purge',
                     '_chroot_apt_install',
                     '_chroot_dpkg_install',
                     '_chroot_pip_cache',
                     '_chroot_pip_install',
                     '_chroot_pip_local',
                     '_chroot_patch'],
    }


def task__image_preseed():
    """
    Install preseed into image

    Installs preseed configuration into the extracted image

    :uptodate:
      - _doit.tools.check_timestamp_unchanged('image/preseed/ubuntu.seed')
    """
    if _os.path.isfile('ubuntu.seed'):
        return {
            'actions': ['sudo cp ubuntu.seed image/preseed/ubuntu.seed'],
            'targets': ['image/preseed/ubuntu.seed'],
            'task_dep': ['_umount_dev'],
            'uptodate': [_doit.tools.check_timestamp_unchanged('image/preseed/ubuntu.seed')],
        }
    else:
        return {
            'actions': None,
            'task_dep': ['_umount_dev'],
        }

def task__image_squashfs_size():
    """
    Store the uncompressed squash filesystem size

    Compute and store squashfs size

    :uptodate:
      - _doit.tools.check_timestamp_unchanged('image/casper/filesystem.size')
    """
    if _os.path.isfile('image/casper/filesystem.size'):
        return {
            'actions': ['sudo du -sx --block-size=1 squashfs-root/ | cut -f1 | sudo tee image/casper/filesystem.size > /dev/null'],
            'targets': ['image/casper/filesystem.size'],
            'task_dep': ['_umount_dev'],
            'uptodate': [_doit.tools.check_timestamp_unchanged('image/casper/filesystem.size')],
        }
    else:
        return {
            'actions': None,
            'task_dep': ['_umount_dev'],
        }

def task__image_squashfs_manifest():
    """
    Store the squashfs manifest

    Compute and store squashfs manifest

    :uptodate:
      - _doit.tools.check_timestamp_unchanged('image/casper/filesystem.manifest')
    """
    task_log = _Path('build/log/manifest.log')
    return {
        'actions': ["sudo chroot squashfs-root dpkg-query -W --showformat='${Package} ${Version}\n'"
                    ' | sudo tee image/casper/filesystem.manifest'
                    ' > %s 2>&1' % task_log],
        'targets': ['image/casper/filesystem.manifest'],
        'task_dep': ['_umount_dev'],
        'uptodate': [_doit.tools.check_timestamp_unchanged('image/casper/filesystem.manifest')],
    }

def task__image_squashfs_make():
    """
    Make squashfs

    Make image squashfs from squashfs-root
    """
    return {
        'actions': ['sudo mksquashfs squashfs-root image/casper/filesystem.squashfs -b 1048576 -noappend'],
        'targets': ['image/casper/filesystem.squashfs'],
        'task_dep': ['_image_squashfs_size',
                     '_image_squashfs_manifest'],
    }

def task__image_checksum():
    """
    Generate checksums for image

    Generate md5sums for image contents

    :uptodate:
      - _doit.tools.check_timestamp_unchanged('image/md5sum.txt')
    """
    return {
        'actions': [_doit.tools.CmdAction('find -type f -print0 | xargs -0 md5sum | grep -v isolinux | grep -v md5sum.txt | sudo tee md5sum.txt > ../build/log/md5sum.log',cwd='./image')],
        'targets': ['image/md5sum.txt'],
        'task_dep': ['_image_squashfs_make'],
        'uptodate': [_doit.tools.check_timestamp_unchanged('image/md5sum.txt')],
    }

@_doit.create_after(executed='_chroot')
def task__image():
    """
    Setup image meta-task

    Calls all of the sub-tasks for final setup of image
    """
    return {
        'actions': None,
        'task_dep': ['_chroot',
                     '_umount_dev',
                     '_image_preseed',
                     '_image_squashfs_size',
                     '_image_squashfs_manifest',
                     '_image_squashfs_make',
                     '_image_checksum'],
    }

def task__qemu_setup():
    """
    Setup QEMU

    Create disk image for VM install
    """
    disk_image = _Path('build/image.raw')
    task_log = _Path('build/log/qemu_setup.log')

    # qemu_disk_size = _ctx['config'].iso_cfg['qemu']['disk_size']

    def create_image():
        # 10GB disk image
        blocksize = 64* 1024
        count = 20 * 1000 * 16
        total_bytes = blocksize * count

        cmd = "dd if=/dev/zero of=%s bs=%d count=%d" % (str(disk_image), blocksize, count)
        with _tqdm(desc='Creating QEMU disk image',
                   total=total_bytes, unit='byte', unit_scale=True,
                   ascii=False) as status:
            with task_log.open('w') as log:
                with _subprocess.Popen(_shlex.split(cmd), bufsize=0,
                                       stdout=log,
                                       stderr=log) as proc:
                    while proc.poll() is None:
                        if status and disk_image.is_file():
                            status.n = disk_image.stat().st_size
                            status.update(0)
                        _time.sleep(1)
                    if status:
                        status.n = total_bytes
                        status.update(0)

    return {
        'actions': [_utils.profile_start,
                    create_image,
                    _utils.profile_stop],
        'task_dep': ['_build_init'],
        'targets': [disk_image],
        'uptodate': [True],
    }

def task_install():
    """
    Install ISO into QEMU VM

    Install ISO into VM
    """
    qemu_cmd = "qemu-system-x86_64 -boot once=d,reboot-timeout=-1 -no-reboot -cdrom build/image.iso -drive file=build/image.raw,if=virtio,format=raw -m 2048 -vga virtio -enable-kvm -kernel ./image/casper/vmlinuz -append 'file=/cdrom/preseed/ubuntu.seed boot=casper noprompt debug-ubiquity automatic-ubiquity DEBCONF_DEBUG=5' -initrd ./image/casper/initrd"

    return {
        'actions': [(_logger.debug, [qemu_cmd]),
                    qemu_cmd],
        'task_dep': ['_qemu_setup'],
        'uptodate': [False],
    }

def task_start():
    """
    Start QEMU VM from installed image

    Start VM from image
    """
    if ('qemu' in _ctx['config'].iso_cfg.keys() and 'args' in _ctx['config'].iso_cfg['qemu'].keys()):
        qemu_args = _ctx['config'].iso_cfg['qemu']['args']
    else:
        qemu_args = ''

    qemu_cmd = "qemu-system-x86_64 -boot order=c,reboot-timeout=-1 -no-reboot -cdrom build/image.iso -drive file=build/image.raw,if=virtio,format=raw -m 8192 -smp 4 -vga virtio -enable-kvm -device qemu-xhci %s" % (qemu_args)

    return {
        'actions': [(_logger.debug, [qemu_cmd]),
                    qemu_cmd],
        'file_dep': ['build/image.raw'],
        'uptodate': [False],
    }

def task_build():
    """
    Roll Your Own ISO

    This is the primary build task
    """

    def cleanup():
        _utils.umount_dev()
        _utils.cleanup_data()

    task_log = _Path('build/log/build.log')
    volume_id = _ctx['config'].iso_cfg['name']
    output_image = _Path('build/image.iso')
    # NOTE: "By default the program arguments of a xorriso run are interpreted as a sequence of commands"
    # https://www.gnu.org/software/xorriso/man_1_xorriso.html
    # FIXME: Ubuntu specific code
    if _ctx['config'].base_image['codename'] >= 'jammy':
        return {
            'actions': [(_logger.debug, ["Volume ID: "+volume_id]),
                        'xorriso -as mkisofs -V "%s" -r -J -joliet-long -l'
                        ' -iso-level 3 -partition_offset 16'
                        ' --grub2-mbr base_image.mbr --mbr-force-bootable'
                        ' -append_partition 2 0xEF base_image.efi -appended_part_as_gpt'
                        ' -c /boot.catalog -b /boot/grub/i386-pc/eltorito.img'
                        ' -no-emul-boot -boot-load-size 4 -boot-info-table'
                        ' --grub2-boot-info -eltorito-alt-boot'
                        ' -e --interval:appended_partition_2:all:: -no-emul-boot'
                        ' -o %s image'
                        ' > %s 2>&1' % (volume_id,output_image,task_log)],
            'targets': [output_image],
            'task_dep': ['_reset_sudo_timestamp',
                         '_image'],
            'clean': [cleanup],
        }
    else:
        return {
            'actions': [(_logger.debug, ["Volume ID: "+volume_id]),
                        'xorriso -as mkisofs -V "%s" -R -J -joliet-long -l'
                        ' -cache-inodes'
                        ' -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin'
                        ' -partition_offset 16'
                        ' -b isolinux/isolinux.bin -c isolinux/boot.cat'
                        ' -boot-load-size 4 -boot-info-table '
                        ' -no-emul-boot -eltorito-alt-boot -e boot/grub/efi.img'
                        ' -no-emul-boot -isohybrid-gpt-basdat -isohybrid-apm-hfsplus'
                        ' -o %s image'
                        ' > %s 2>&1' % (volume_id,output_image,task_log)],
            'targets': [output_image],
            'task_dep': ['_reset_sudo_timestamp',
                         '_image'],
            'clean': [cleanup],
        }
