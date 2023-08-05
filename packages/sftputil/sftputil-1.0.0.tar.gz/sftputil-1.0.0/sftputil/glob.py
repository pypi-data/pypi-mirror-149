# coding: utf-8
"""Strongly inspired by https://github.com/python/cpython/blob/3.8/Lib/glob.py"""

import os
import fnmatch
import re


def iglob(sftp, pathname, recursive, dironly):
    """SFTP implementation of glob.iglob, but lighter

    The pattern may contain simple shell-style wildcards a la fnmatch. However, unlike
    fnmatch, filenames starting with a dot are special cases that are not matched by
    '*' and '?' patterns.  If recursive is true, the pattern '**' will match any files
    and zero or more directories and subdirectories.
    """

    dirname, basename = os.path.split(pathname)

    if not _has_magic(str(pathname)):
        assert not dironly
        # No special characters, simply yield the pathname if it exists
        if basename:
            if sftp.exists(pathname):
                yield pathname
        else:
            # Patterns ending with a slash should match only directories
            if sftp.is_dir(dirname):
                yield pathname
        return

    # TODO: WHAT IS THIS COMMENTED CODE?
    # if not dirname:
    #     # The path does not contain parent directory
    #     # Search for a recursive pattern ** or directly a file pattern
    #     if recursive and _is_recursive(basename):
    #         yield from _glob_r_p(sftp, dirname, basename, dironly)
    #     else:
    #         yield from _glob_nr_p(sftp, dirname, basename, dironly)
    #     return

    # Before searching for the basename, search for every dirname matching the pattern.
    if dirname != pathname and _has_magic(dirname):
        dirs = iglob(sftp, dirname, recursive, True)
    else:
        dirs = [dirname]

    # Then, search for the basename using the appropriate glob function.
    if _has_magic(basename):
        if recursive and _is_recursive(basename):
            glob_in_dir = _glob_r_p
        else:
            glob_in_dir = _glob_nr_p
    else:
        glob_in_dir = _glob_nr_l
    for dirname in dirs:
        for name in glob_in_dir(sftp, dirname, basename, dironly):
            yield os.path.join(dirname, name)


def _has_magic(s):
    magic_check = re.compile(r"([*?[])")
    return magic_check.search(str(s)) is not None


def _is_recursive(pattern):
    return pattern == "**"


def _is_hidden(path):
    return path[0] in (".")


def _glob_nr_l(sftp, dirname, basename, dironly):
    """Non-recursively glob inside a dir using a literal."""
    if not basename:
        if sftp.is_dir(dirname):
            return [basename]
    else:
        if sftp.exists(os.path.join(basename, dirname)):
            return [basename]
    return []


def _glob_nr_p(sftp, dirname, pattern, dironly):
    """Non-recursively glob inside a dir using a pattern."""
    names = list(_iter_dir(sftp, dirname, dironly))
    if not _is_hidden(pattern):
        names = (n for n in names if not _is_hidden(n))
    return fnmatch.filter(names, pattern)


def _glob_r_p(sftp, dirname, pattern, dironly):
    """Recursively yields relative pathnames inside a directory"""
    assert _is_recursive(pattern)
    yield pattern[:0]
    for _, folders, files in sftp.walk(dirname):
        yield from folders
        if not dironly:
            yield from files


def _iter_dir(sftp, dirname, dironly):
    """Iter over items in a directory.

    If dironly is false, yields all file names inside a directory.
    If dironly is true, yields only directory names.
    """
    _, folders, files = next(sftp.walk(dirname))
    yield from folders
    if not dironly:
        yield from files
