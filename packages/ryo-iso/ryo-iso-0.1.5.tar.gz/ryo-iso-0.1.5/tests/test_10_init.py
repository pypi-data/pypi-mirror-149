import pytest
import os
import delegator
import shutil
import tempfile
from pathlib import Path

def test_init(pytestconfig,request,data_path):
    import ryo_iso.cli
    ryo_iso.cli.cli(['init'])
    assert(os.path.isfile(Path(data_path)/"iso.yml"))

    c = delegator.run("grep image: iso.yml")
    assert(c.out == "image: ubuntu/jammy\n")
