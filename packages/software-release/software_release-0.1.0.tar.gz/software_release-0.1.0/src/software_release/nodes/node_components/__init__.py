from software_release.nodes import Node
from software_release.utils import load
import os



my_dir = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(my_dir, '..', '..')

load(my_dir, Node, root)


# Probably we do not need the __all__ to be defined
# simple do in client code 'import node_components'

# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

