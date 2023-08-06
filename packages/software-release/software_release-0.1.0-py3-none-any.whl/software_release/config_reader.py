"""Helpers to read settings from setup.cfg or pyproject.toml
"""
import configparser
import logging
import os
# import toml


logger = logging.getLogger(__name__)


def config(repository_root_path):

    parser = configparser.ConfigParser()
    parser.read(
        [
            os.path.join(repository_root_path, 'setup.cfg'),
        ]
    )

    # toml_conf_path = os.path.join(repository_root_path, "pyproject.toml")
    # if os.path.isfile(toml_conf_path):
    #     # Overwrite with any settings from pyproject.toml
    #     with open(toml_conf_path, "r") as pyproject_toml:
    #         try:
    #             pyproject_toml = toml.load(pyproject_toml)
    #             pyproject_toml_settings = (
    #                 pyproject_toml.get("tool", {}).get("semantic_release", {}).items()
    #             )
    #             for key, value in pyproject_toml_settings:
    #                 parser["semantic_release"][key] = str(value)
    #         except toml.TomlDecodeError:
    #             logger.debug("Could not decode pyproject.toml")
    # parser['semantic_release']['setup_py'] = os.path.join(current_dir, 'setup.py')
    # parser['semantic_release']['changelog_rst'] = os.path.join(current_dir, 'CHANGELOG.rst')
    # parser['semantic_release']['readme_rst'] = os.path.join(current_dir, 'README.rst')
    # parser['semantic_release']['readme_md'] = os.path.join(current_dir, 'README.md')
    return parser
