import sys
import ryo_iso
from doit.doit_cmd import DoitMain
from doit.cmd_base import ModuleTaskLoader

cfgs = ryo_iso.Config.data.values()
# Only allow init task if config files do not exist
if not all(map(lambda x: x.exists(), cfgs)):
    import ryo_iso.tasks.init
    module = ryo_iso.tasks.init
else:
    # Initialize configuration context
    ryo_iso.config._ctx = {}
    ryo_iso.config._ctx['config'] = ryo_iso.config.Config()

    import ryo_iso.tasks.main
    module = ryo_iso.tasks.main

def cli(argv=None):
    if argv is not None:
        DoitMain(ModuleTaskLoader(module)).run(argv)
    else:
        sys.exit(DoitMain(ModuleTaskLoader(module)).run(sys.argv[1:]))
