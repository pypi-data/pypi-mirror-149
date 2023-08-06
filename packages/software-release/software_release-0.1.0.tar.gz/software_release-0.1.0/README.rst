SOFTWARE RELEASE

Automate Releasing of Software, following Semantic Versioning

.. start-badges

| |build| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|


|
| **Source Code:** https://github.com/boromir674/software-release
| **Pypi Package:** https://pypi.org/project/software_release/
|


Features
========


1. **software_release** `python package`

   a. **Great Feature**
   b. **Nice Feature**

2. **Test Suite** using `Pytest`
3. **Parallel Execution** of Unit Tests, on multiple cpu's
4. **Automation**, using `tox`

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build` python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org` and `test.pypi.org` servers
   d. **Type Check Command**, using `mypy`
5. **CI Pipeline**, running on `Github Actions`

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`
      2. Python Interpreters: `3.8`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`


Prerequisites
=============

You need to have `Python` installed.

Quickstart
==========

Using `pip` is the approved way for installing `software_release`.

.. code-block:: sh

    python3 -m pip install software_release


TODO demonstrate a use case


License
=======

|gh-lic|

* `GNU Affero General Public License v3.0`_


License
=======

* Free software: GNU Affero General Public License v3.0


.. MACROS/ALIASES

.. start-badges

.. Test Workflow Status on Github Actions for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/software-release/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/software-release/actions/workflows/test.yaml?query=branch%3Amaster

.. above url to workflow runs, filtered by the specified branch

.. |release_version| image:: https://img.shields.io/pypi/v/software_release
    :alt: Production Version
    :target: https://pypi.org/project/software_release/

.. |wheel| image:: https://img.shields.io/pypi/wheel/software-release?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/software_release

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/software-release?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/software_release

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/software-release/v0.1.0/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/software-release/compare/v0.1.0..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/software-release/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)

.. Github License (eg AGPL, MIT)
.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/software-release
    :alt: GitHub
    :target: https://github.com/boromir674/software-release/blob/master/LICENSE


.. LINKS

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/software-release/blob/master/LICENSE
