import glob
from os.path import basename, dirname, isfile, join

import automodinit

__all__ = []
automodinit.automodinit(__name__, __file__, globals())
del automodinit
modules = glob.glob(join(dirname(__file__), "*.py"))
supported = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]