#!/usr/bin/env python
# coding: utf-8

"""Main module of the library."""

import pathlib
import socket
from stat import S_ISDIR, S_ISREG
import paramiko

from sftputil.glob import iglob as _iglob
from sftputil.sync import sync_pull as _sync_pull


class SFTP(paramiko.sftp_client.SFTPClient):
    """A wrapper around paramiko’s SFTPClient, with some improvements."""

    def __init__(self, hostname, username, port=22, key_file=None, password=None):
        """Create a SFTP connection from scratch"""
        self.hostname = hostname
        # Create Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((hostname, port))
        sock.settimeout(None)
        # Create Transport over Socket
        transport = paramiko.Transport(sock)
        transport.start_client()
        # supposed to check for key in keys, but I don't much care right now
        # keys = paramiko.util.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
        # key = transport.get_remote_server_key()
        if key_file is not None:
            if isinstance(key_file, str):
                key_file = open(key_file, "r")
            key_head = key_file.readline()
            key_file.seek(0)
            if "DSA" in key_head:
                keytype = paramiko.DSSKey
            elif "RSA" in key_head:
                keytype = paramiko.RSAKey
            elif "ECDSA" in key_head:
                keytype = paramiko.RSAKey
            elif "Ed25519" in key_head:
                keytype = paramiko.RSAKey
            else:
                raise Exception(
                    "Can't identify key type from key head '{}'".format(key_head)
                )
            pkey = keytype.from_private_key(key_file)
            transport.auth_publickey(username, pkey)
        else:
            if password is not None:
                transport.auth_password(username, password, fallback=False)
            else:
                raise Exception("Must supply either key_file or password")
        # Create Channel over Transport over Socket
        channel = transport.open_session(window_size=None, max_packet_size=None)
        if channel is None:
            raise RuntimeError(
                "Cannot create a SSH channel toward '{}'".format(hostname)
            )
        channel.invoke_subsystem("sftp")
        # Create SFTP over Channel over Transport over Socket
        super().__init__(channel)

    def walk(self, remotepath):
        """Walk from a remote directory like os.walk

        Args:
            remotepath: (str|pathlib.Path) the top directory to walk from.
                If it points to a file, it yields nothing and ends immediately.
                If it points to nothing, it raises an error.

        Raise:
            FileNotFoundError: if `remotepath` does not exist.
        """
        path = pathlib.Path(remotepath)
        if not self.exists(path):
            raise FileNotFoundError(path)
        if self.is_file(path):
            return
        files = []
        folders = []
        for fattr in self.listdir_iter(str(remotepath)):
            if S_ISDIR(fattr.st_mode):
                folders.append(fattr.filename)
            else:
                files.append(fattr.filename)
        yield path, folders, files
        for folder in folders:
            new_path = path.joinpath(folder)
            for new_tuple in self.walk(new_path):
                yield new_tuple

    def sync_pull(
        self, remote_path, local_directory, recursive=True, ignore=None, keep_tree=False
    ):
        """Like rsync but with SFTP, to download files.

        Read `sftp.sync.sync_pull` documentation.
        """
        _sync_pull(self, remote_path, local_directory, recursive, ignore, keep_tree)

    def exists(self, path):
        """Whether the path points to an existing file or directory.

        Follow symlinks.

        Args:
            path: remote path to check

        Returns:
            (bool) True if the path exists, False else.
        """
        try:
            self.stat(str(path))
        except FileNotFoundError:
            return False
        return True

    def is_dir(self, path):
        """Whether the path points to an existing directory.

        Follow symlinks.

        Args:
            path: remote path to check

        Returns:
            (bool) True if the path points to a dir, False else.
        """
        try:
            attr = self.stat(str(path))
        except FileNotFoundError:
            return False
        if S_ISDIR(attr.st_mode):
            return True
        return False

    def is_file(self, path):
        """Whether the path points to an existing file.

        Follow symlinks.

        Args:
            path: remote path to check

        Returns:
            (bool) True if the path points to a file, False else.
        """
        try:
            attr = self.stat(str(path))
        except FileNotFoundError:
            return False
        if S_ISREG(attr.st_mode):
            return True
        return False

    def iglob(self, pathname, recursive=True):
        """SFTP implementation of glob.iglob, but lighter"""
        yield from _iglob(self, pathname, recursive, False)

    def glob(self, pathname, recursive=True):
        """SFTP implementation of glob.glob, but lighter"""
        return list(self.iglob(pathname, recursive))
