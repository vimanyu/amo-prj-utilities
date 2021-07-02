#!/usr/bin/env python

import fire
import json
import os
import re
import pathlib
import subprocess
import sys
from termcolor import cprint


#Add pytest
#Build framework for  commandline tools.

"""
function to handle bad version string
"""

class SetContext(object):

    def validate_project_name(self, name: str) -> bool:
        patterns = '^[a-z0-9/-]*$'
        if re.search(patterns, name):
            return True
        else:
            return False

    def validate_gcloud_projects(self, project_name: str) -> bool:
        output = subprocess.check_output("gcloud projects list --format json".split(" "))
        json_str = output.decode('utf-8')
        json_data = json.loads(json_str)
        project_names = [project['name'] for project in json_data]

        return False if project_name in project_names else True


    """This is really gross but I dont really have a choice."""
    """eval `python setcontext.py set_env "myprj:myserv:v001"`"""
    def set_env(self, project_name=None):


        project = None
        service = None
        version = None

        # replace with argparse for better error handling and help?
        if not ":" in project_name:
            project = project_name

        else:
            split_context = project_name.split(":")
            split_count = len(split_context)

            if len(split_context) == 2:
                project, service = split_context

            if len(split_context) == 3:
                project, service, version = split_context
                validate_version_str(version)

        if self.validate_project_name(project):
            print(f"echo Setting PROJECT to {project};")
            print(f"export PROJECT={project};")
            if service:
                print(f"echo Setting SERVICE to {service};")
                print(f"export SERVICE={service};")
            if version:
                print(f"echo Setting VERSION to {version};")
                print(f"export VERSION={version};")


    def print_project_env_var(self):
        self.pprint(os.environ['PROJECT'], 'red', 2)
        self.pprint(os.environ['SERVICE'], 'red', 2)
        self.pprint(os.environ['VERSION'], 'red', 2)

    @classmethod
    def pprint(cls, msg, color, indent=0):
        cprint("\t"*indent + msg, color)


def validate_version_str(version_string: str):
    #replace with regex
    if not version_string.startswith("v"):
        sys.exit(f"version string: {version_string} doesn't start with v")
    if not version_string[1:].isdigit():
        sys.exit(f"version string: {version_string} doesnt end in numerics 00 - 99")
    if not len(version_string) == 4:
        sys.exit(f"version string: {version_string} doesnt end in numerics 000 - 999")



def set_directory():
    path = pathlib.Path.home() / "git"
    project, service, version = None
    if project is not None:
        path /= project

    if service is not None:
        path /= service

    if version is not None:
        path /= version

    # add beta or alpha flags

    path_str = path.absolute().as_posix()

    if path.is_dir():
        print(path_str)

    else:
        path.mkdir(parents=True, exist_ok=True)
        print(path_str)


if __name__ == '__main__':
    fire.Fire(SetContext)



