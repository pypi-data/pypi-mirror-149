import os
from software_release.commands.base_command import BaseCommand
from software_release.utils import load


my_dir = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(my_dir, '..')

load(my_dir, BaseCommand, root)

