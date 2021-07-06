#!/usr/bin/env python

import sys
import pathlib

#Add pytest
#Build framework for  commandline tools.

"""
function to handle bad version string
"""
def validate_version_str(version_string: str):
    #replace with regex
    if not version_string.startswith("v"):
        sys.exit(f"version string: {version_string} doesn't start with v")
    if not version_string[1:].isdigit():
        sys.exit(f"version string: {version_string} doesnt end in numerics 00 - 99")
    if not len(version_string) == 4:
        sys.exit(f"version string: {version_string} doesnt end in numerics 000 - 999")

if __name__ == '__main__':

    project = None
    service = None
    version = None

    #replace with argparse for better error handling and help?
    if not ":" in sys.argv[1]:
        project = sys.argv[1]

    else:
        split_context = sys.argv[1].split(":")
        split_count = len(split_context)

        if len(split_context) == 2:
            project, service = split_context

        if len(split_context) == 3:
            project, service, version = split_context
            validate_version_str(version)

    path = pathlib.Path.home() / "git"
    if project is not None:
        path /= project

    if service is not None:
        path /= service

    if version is not None:
        path /= version

    #add beta or alpha flags

    path_str = path.absolute().as_posix()

    if path.is_dir():
        print(path_str)

    else:
        path.mkdir(parents=True, exist_ok=True)
        print (path_str)