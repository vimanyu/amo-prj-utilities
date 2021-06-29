#!/usr/bin/env python

import os
import sys
import re
import json
import pathlib
from pprint import pprint

import subprocess

GITDIR = pathlib.Path.home() / "git"

def validate_project_name(name : str) -> bool:
    patterns = '^[a-z0-9/-]*$'
    if re.search(patterns, name):
        return True
    else:
        return False







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    arg = sys.argv[1]
    if (len(sys.argv) == 2):
        arg = sys.argv[1]
        print(f"Validating project name {arg}")
        if validate_project_name(arg):
            sys.exit(0)
        else:
            sys.exit("Invalid project name, project must be lowercase and hyphen")


    output = subprocess.check_output("gcloud projects list --format json".split(" "))
    json_str = output.decode('utf-8')
    json_data = json.loads(json_str)
    project_names = [project['name'] for project in json_data]

    if arg in project_names:
        sys.exit(0)
    else:
        sys.exit("Project exists")



