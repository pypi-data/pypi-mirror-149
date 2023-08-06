"""Plugin for setuptools providing npm commands."""
import os
import shlex
import subprocess
from distutils import log

from setuptools import Command

__version__ = '0.2'


# Taken from https://github.com/python-babel/babel/blob/master/babel/messages/frontend.py
def listify_value(arg, split=None):
    """
    Make a list out of an argument.
    Values from `distutils` argument parsing are always single strings;
    values from `optparse` parsing may be lists of strings that may need
    to be further split.
    No matter the input, this function returns a flat list of whitespace-trimmed
    strings, with `None` values filtered out.
    >>> listify_value("foo bar")
    ['foo', 'bar']
    >>> listify_value(["foo bar"])
    ['foo', 'bar']
    >>> listify_value([["foo"], "bar"])
    ['foo', 'bar']
    >>> listify_value([["foo"], ["bar", None, "foo"]])
    ['foo', 'bar', 'foo']
    >>> listify_value("foo, bar, quux", ",")
    ['foo', 'bar', 'quux']
    :param arg: A string or a list of strings
    :param split: The argument to pass to `str.split()`.
    :return:
    """
    out = []

    if not isinstance(arg, (list, tuple)):
        arg = [arg]

    for val in arg:
        if val is None:
            continue
        if isinstance(val, (list, tuple)):
            out.extend(listify_value(val, split=split))
            continue
        out.extend(s.strip() for s in str(val).split(split))
    assert all(isinstance(val, str) for val in out)
    return out


class npm_install(Command):
    """Custom command that runs npm install."""

    description = 'npm install dependencies'
    user_options = [
        ('no-clean', None, 'use npm install instead of npm clean-install'),
    ]
    boolean_options = ['no-clean']

    def initialize_options(self):
        self.no_clean = False

    def finalize_options(self):
        pass

    def run(self):
        command = 'install' if self.no_clean else 'clean-install'
        log.info("-> npm %s", command)
        subprocess.run(['npm', command], check=True)


class npm_run(Command):
    """Custom command that runs npm run."""

    description = 'npm run script'
    user_options = [
        ('script=', None, 'semicolon or newline separated list of npm scripts to run'),
    ]

    def initialize_options(self):
        self.script = []

    def finalize_options(self):
        self.script = listify_value(listify_value(self.script, split=';'), '\n')

    def run(self):
        for script in self.script:
            log.info("-> npm run %s", script)
            subprocess.run(['npm', 'run', *shlex.split(script)], check=True)


def npm_not_skipped(build) -> bool:
    """Return whether npm command should be run.

    This can be used as predicate in distutils sub_commands.
    """
    return not bool(os.environ.get('SKIP_NPM', False))
