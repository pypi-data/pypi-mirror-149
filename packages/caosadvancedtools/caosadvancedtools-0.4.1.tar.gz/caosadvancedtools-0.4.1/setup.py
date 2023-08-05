#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
#
"""caosadvancedtools"""
import os
import subprocess
import sys

from setuptools import find_packages, setup

########################################################################
# The following code is largely based on code in numpy
########################################################################
#
# Copyright (c) 2005-2019, NumPy Developers.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#    * Neither the name of the NumPy Developers nor the names of any
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
########################################################################

MAJOR = 0
MINOR = 4
MICRO = 1
PRE = ""  # e.g. rc0, alpha.1, 0.beta-23
ISRELEASED = True

if PRE:
    VERSION = "{}.{}.{}-{}".format(MAJOR, MINOR, MICRO, PRE)
else:
    VERSION = "{}.{}.{}".format(MAJOR, MINOR, MICRO)


# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}

        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)

            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, env=env)

        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except (subprocess.SubprocessError, OSError):
        GIT_REVISION = "Unknown"

    return GIT_REVISION


def get_version_info():
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of caosadvancedtools.version messes up the build under
    # Python 3.
    FULLVERSION = VERSION

    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('src/caosadvancedtools/version.py'):
        # must be a source distribution, use existing version file
        try:
            from caosadvancedtools.version import git_revision as GIT_REVISION
        except ImportError:
            raise ImportError("Unable to import git_revision. Try removing "
                              "src/caosadvancedtools/version.py and the build directory "
                              "before building.")
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev0+' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION


def write_version_py(filename='src/caosadvancedtools/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM caosadvancedtools SETUP.PY
#
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    FULLVERSION, GIT_REVISION = get_version_info()

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


def setup_package():
    # load README
    with open("README.md", "r") as fh:
        long_description = fh.read()

    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
    sys.path.insert(0, src_path)

    # Rewrite the version file everytime
    write_version_py()

    metadata = dict(
        name='caosadvancedtools',
        version=get_version_info()[0],
        description='advanced utilities for caosdb',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Henrik tom Wörden',
        author_email='h.tomwoerden@indiscale.com',
        install_requires=["caosdb>=0.7.0",
                          "jsonschema>=4.4.0",
                          "numpy>=1.17.3",
                          "openpyxl>=3.0.0",
                          "pandas>=1.2.0",
                          "xlrd>=2.0",
                          ],
        extras_require={"h5-crawler": ["h5py>=3.3.0", ],
                        },
        packages=find_packages('src'),
        package_dir={'': 'src'},
        setup_requires=["pytest-runner>=2.0,<3dev"],
        tests_require=["pytest", "pytest-pythonpath", "pytest-cov", "coverage>=4.4.2"],
    )
    try:
        setup(**metadata)
    finally:
        del sys.path[0]
    return


if __name__ == '__main__':
    setup_package()
