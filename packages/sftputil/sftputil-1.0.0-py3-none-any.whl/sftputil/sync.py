# coding: utf-8

import pathlib
import os
import re


def sync_pull(
    sftp,
    remote_path,
    local_directory,
    recursive=True,
    ignore=None,
    keep_tree=False,
):
    """Like rsync but with SFTP, to download files.

    WARNING: at the moment, sync is only done based on names. An improvement is to
    take other parameters into acccount like hash or size.

    Args:
        sftp: (sftputil.SFTP) the SFTP connection to use for sync.
        remote_path: (str|pathlib.Path) The remote path to sync. Can be a directory
            or a file.
        local_directory: (str|pathlib.Path) The local path where to sync the
            remote_path. Must be an existing directory.
        recursive: (bool) Whether to sync subdirectories as well.
        ignore: (regex str) a pattern to ignore some paths (matches the full path).
        keep_tree: (bool) If True, the whole directory path given in `remote_path`
            is created in `local_directory`. If False, only the leaf is
            synchronized. Default is False.
            Example:
                if `remote_path` is `/dir1/dir2/dir3/file`
                When keep_tree=True, the file is written on this local path:
                `<local_directory>/dir1/dir2/dir3/file`
                When keep_tree=False, the file is written on this local path:
                `<local_directory>/file`

    Raises:
        NotADirectoryError if `local_directory` is not a local directory.
        FileNotFoundError if the `remote_path` points to nothing.
    """
    remote_path = pathlib.PurePosixPath(remote_path)
    # Check the remote_path existence
    if not sftp.exists(remote_path):
        raise FileNotFoundError(f"'{remote_path}' not found on '{sftp.hostname}'")

    # Create the local directory if it does not exist
    local_base_dir = pathlib.Path(local_directory)
    if not local_base_dir.is_dir():
        raise NotADirectoryError(local_base_dir)

    # If remote_path is a file, just get it without walking
    if sftp.is_file(remote_path):
        _sync_pull_files(
            sftp,
            [remote_path.name],
            remote_path.parent,
            local_base_dir,
            remote_path,
            keep_tree,
            ignore,
        )
        return

    for walked_path, dirs, files in sftp.walk(remote_path):
        # Start by syncing files
        _sync_pull_files(
            sftp, files, walked_path, local_base_dir, remote_path, keep_tree, ignore
        )
        # If sync is not recursive, just stop there
        if not recursive:
            break
        # Create directories if necessary
        for dirname in dirs:
            local_dir_path = _build_local_path(
                local_base_dir, remote_path, walked_path, dirname, keep_tree
            )
            local_dir_path.mkdir(parents=True, exist_ok=True)


def _build_local_path(
    local_base, remote_base, target_dirname, target_basename, keep_tree
):
    """Build an approriate local path to get a file from remote host.

    If some intermediate directories must be created, they will.

    Args:
        local_base: (pathlib.Path) the top-level local directory to where the
            synchronization is performed.
        remote_base: (pathlib.Path) the top-level remote directory from where the
            synchronization is performed.
        target_dirname: (pathlib.Path) the full path to the directory of the leaf.
        target_basename: (pathlib.Path) the name of the leaf.
        keep_tree: (bool) Whether to keep remote tree in local filesystem.
    """
    if keep_tree:
        result_path = local_base.joinpath(
            str(target_dirname).lstrip("/"),  # remove / to make path relative
            target_basename,
        )
        result_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        remote_base_dirname = os.path.dirname(str(remote_base))
        result_path = local_base.joinpath(
            re.sub(
                remote_base_dirname, "", str(target_dirname)
            ),  # remove useless parent tree
            target_basename,
        )
    return result_path


def _sync_pull_files(
    sftp, filenames, remote_dir, local_base, remote_base, keep_tree, ignore=None
):
    """Synchronize a list of files.

    Args:
        sftp: (sftputil.SFTP) the SFTP connection to use for sync.
        files: (list[str]) a list of filenames existing in the `remote_dir`.
        remote_dir: (pathlib.Path) a full path to an existing directory on the
            remote host.  This directory must contain the files listed in `files`.
        local_base: (pathlib.Path) the top-level local directory to where the
            synchronization is performed.
        remote_base: (pathlib.Path) the top-level remote directory from where the
            synchronization is performed.
        keep_tree: (bool) Whether to keep remote tree in local filesystem.
        ignore: (str) (optional) full-path-pattern pattern to ignore some files.

    Raises:
        FileNotFoundError if one of the requested files is not found on remote host.
    """
    for filename in filenames:
        local_file_path = _build_local_path(
            local_base, remote_base, remote_dir, filename, keep_tree
        )
        remote_file_path = remote_dir.joinpath(filename)
        # Ignore file from regex
        if ignore is not None and re.search(ignore, str(remote_file_path)):
            continue
        # Ignore if the file already exists
        # TODO: check if the file is identical ?
        if local_file_path.exists():
            continue
        # Download the file to the local file system
        try:
            sftp.get(str(remote_file_path), str(local_file_path))
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "Cannot find '{}'".format(remote_file_path)
            ) from exc
