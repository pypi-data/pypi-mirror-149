import pytest
import os
import delegator
import shutil
import tempfile
import importlib
from pathlib import Path

def test_init(pytestconfig,request,data_path):
    import ryo_iso.cli

    with (data_path/'iso.yml').open('w') as f:
        f.write("""# test config file
image: ubuntu/22.04
arch: amd64
variant: desktop
apt:
  install:
    - git
    - python3-pip

pip:
  install:
    - doit
""")

    importlib.reload(ryo_iso.cli)
    ryo_iso.cli.cli(['_hash_version'])

    with (data_path/'.release_version').open('r') as f:
        image_version = f.read()
    assert(image_version == '22.04')

    with (data_path/'.hash').open('r') as f:
        image_hash = f.read()
    assert(image_hash == 'b85286d9855f549ed9895763519f6a295a7698fb9c5c5345811b3eefadfb6f07')
