# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2014-2017 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
import errno
import logging
import os
import subprocess


from byov import errors


logger = logging.getLogger(__name__)


def run(args, cmd_input=None, raise_on_error=True):
    """Run the specified command capturing output and errors.

    :param args: A list of a command and its arguments.

    :param cmd_input: A unicode string to feed the command with.

    :param raise_on_error: A boolean controlling whether or not an exception is
        raised if the command fails.

    :return: A tuple of the return code, the output and the errors as unicode
        strings.

    """
    stdin = None
    if cmd_input is not None:
        stdin = subprocess.PIPE
        cmd_input = cmd_input.encode('utf8')
    logger.debug('Running {}'.format(' '.join(args)))
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=stdin)
    out, err = proc.communicate(cmd_input)
    out = out.decode('utf8')
    err = err.decode('utf8')
    if raise_on_error and proc.returncode:
        raise errors.CommandError(args, proc.returncode, out, err)
    logger.debug('Returned: {}'.format(proc.returncode))
    if out:
        logger.debug('stdout: {}'.format(out))
    if err:
        logger.debug('stderr: {}'.format(err))
    return proc.returncode, out, err


def raw_run(args):
    """Run the specified command without redirecting anything.

    This is mainly useful to wrap a command leaving std{in,out,err}
    untouched so the user can interact.

    :param args:  A list of a command and its arguments.

    :return: The return code.
    """
    logger.debug('Running {}'.format(' '.join(args)))
    proc = subprocess.Popen(args)
    proc.wait()
    return proc.returncode


def pipe(args):
    """Run the specified command as a pipe.

    The caller is responsible for processing the output and the errors.

    :param args:  A list of a command and its arguments.

    :return: The Popen object.
    """
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc


def which(cmd, path, mode=os.F_OK | os.X_OK):
    """Given a command, mode, and a PATH list of strings, return the path which
    conforms to the given mode on the PATH, or None if there is no such file.

    `mode` defaults to os.F_OK | os.X_OK.

    This is heavily inspired by shutils.which but the API and implementation is
    significantly different and the implementation way simpler.
    """
    if path:
        files = [cmd]

        seen = set()
        for d in path:
            normdir = os.path.normcase(d)
            if normdir not in seen:
                seen.add(normdir)
                for thefile in files:
                    name = os.path.join(d, os.path.normpath(thefile))
                    if os.path.exists(name):
                        if os.access(name, mode):
                            return name
                        else:
                            raise PermissionError(
                                errno.EACCES,
                                name + ' is not executable', cmd)
        raise FileNotFoundError(errno.ENOENT, '{} not found in: {}'.format(
            cmd, path), cmd)
