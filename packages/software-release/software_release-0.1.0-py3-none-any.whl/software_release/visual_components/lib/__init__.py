from software_release.utils import load
import os

from ..visual_component import VisualComponent


my_dir = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(my_dir, '..', '..')

load(my_dir, VisualComponent, root)
