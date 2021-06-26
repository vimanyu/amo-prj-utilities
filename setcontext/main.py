#!/usr/bin/env python

import sys
import pathlib

if __name__ == '__main__':
    path = pathlib.Path.home() / "git"
    path_str = path.absolute().as_posix()
    sys.exit(path_str)