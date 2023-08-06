import os

from inspect import isclass
from pkgutil import iter_modules
from importlib import import_module


def load(dire, interface, package_root):
    # iterate through the modules in the dire folder

    project_package_location = os.path.dirname(os.path.realpath(package_root))

    for (_, module_name, _) in iter_modules([dire]):

        absolute_package = str(dire).replace(str(project_package_location), '')[1:].replace('/', '.')

        args = [f'{absolute_package}.{module_name}']

        module = import_module(*args)

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and issubclass(attribute, interface):
                # Add the class to this package's variables
                globals()[attribute_name] = attribute
