import os

from software_release.utils import load
from ..interactive_dialog import Dialog


my_dir = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(my_dir, '..', '..', '..')

load(my_dir, Dialog, root)
