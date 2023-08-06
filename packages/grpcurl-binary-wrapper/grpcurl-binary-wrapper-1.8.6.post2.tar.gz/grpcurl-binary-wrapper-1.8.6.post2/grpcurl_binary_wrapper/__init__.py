#!/usr/bin/env python

import os
import stat
import sys
import urllib.request
import tarfile
import platform

from os.path import join
from pathlib import Path


BASE_DIR = os.path.dirname(__file__)
GRPCURL_VERSION = "1.8.6"
GRPCURL_EXECUTABLE_SYSTEM = os.path.join(sys.prefix, 'lib/grpcurl')
GRPCURL_EXECUTABLE_LOCAL = os.path.join(BASE_DIR, 'lib/grpcurl')
GRPCURL_EXECUTABLE = (
    GRPCURL_EXECUTABLE_SYSTEM if os.path.exists(
        GRPCURL_EXECUTABLE_SYSTEM)
    else GRPCURL_EXECUTABLE_LOCAL
)


def download(version=GRPCURL_VERSION):
    platform_name = platform.system().lower()
    base_url = \
        f"https://github.com/fullstorydev/grpcurl/releases/download/v{version}"
    file_name = f"grpcurl_{version}_{platform_name}_x86_64.tar.gz"
    download_url = f"{base_url}/{file_name}"

    download_directory = "downloads"
    extract_directory = "grpcurl_binary_wrapper/lib"
    target_file = f"{download_directory}/{file_name}"

    os.makedirs(download_directory, exist_ok=True)
    os.makedirs(extract_directory, exist_ok=True)
    Path(join(extract_directory, "__init__.py")).touch()

    urllib.request.urlretrieve(download_url, target_file)

    with tarfile.open(target_file) as grpcurl_zip_archive:
        grpcurl_zip_archive.extractall(extract_directory)

    executable_path = f"{extract_directory}/grpcurl"
    executable_stat = os.stat(executable_path)
    os.chmod(executable_path, executable_stat.st_mode | stat.S_IEXEC)


def main():
    args = [] if len(sys.argv) < 2 else sys.argv[1:]
    os.execv(GRPCURL_EXECUTABLE, ["grpcurl"] + args)
