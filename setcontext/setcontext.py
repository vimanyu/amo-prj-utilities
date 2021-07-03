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


def valid_envvar(var: str) -> bool:
    return (var in os.environ.keys()) and (os.environ[var] != "")

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

class SetContext(object):

    def build_directory_path(self):
        """
        This builds the path of the project from environment variables. If no project environment variables exist,
        Then the directory defaults to ~/git

        eval `python setcontext.py build_directory_path`
        """
        path = pathlib.Path.home() / "git"
        if valid_envvar("PROJECT"):
            path /= os.environ['PROJECT']

        if valid_envvar("SERVICE"):
            path /= os.environ['SERVICE']

        if valid_envvar("VERSION"):
            path /= os.environ['VERSION']

        # add beta or alpha flags

        path_str = path.absolute().as_posix()

        if path.is_dir():
            print(path_str)

        else:
            path.mkdir(parents=True, exist_ok=True)
            print(path_str)
    #memoize



    """This is really gross but I dont really have a choice."""
    """eval `python setcontext.py set_env "myprj:myserv:v001"`"""
    def set_env(self, project_name=None):

        project = ""
        service = ""
        version = ""

        # replace with argparse for better error handling and help?
        if not ":" in project_name:
            project = project_name
            version = ""

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

            print(f"echo Setting SERVICE to {service};")
            print(f"export SERVICE={service};")

            print(f"echo Setting VERSION to {version};")
            print(f"export VERSION={version};")


    """eval `python setcontext.py set_terminal_prompt`"""
    def set_terminal_prompt(self):
        prompt_string = "PS1="
        if valid_envvar("PROJECT"):
            prompt_string += "'%F{55}'${PROJECT}"
        if valid_envvar("SERVICE"):
            prompt_string += "'%F{default}:%F{46}'${SERVICE}"
        if valid_envvar("VERSION"):
            prompt_string += "'%F{default}:%F{38}'${VERSION}"


        prompt_string += "'%F{default} >> '"
        print(prompt_string)


    def create_project(self):
        pass

    def set_project(self):
        print("conda activate ${PROJECT}")
        #print("PROJECT")
        self.set_terminal_prompt()
        print("git init")
        print("hub create")

    def print_project_variables(self):
        self.pprint(os.environ['PROJECT'], 'red', 2)
        self.pprint(os.environ['SERVICE'], 'red', 2)
        self.pprint(os.environ['VERSION'], 'red', 2)






    def setcontext(self, context: str):
        """
        Main program to call all the sub functions for setting context between projects.
        This generates a bash script to be called from the shell and evaluated.

        Ex:
        eval `python setcontext.py setcontext my_project_name:my_service_or_module/v<001-999>

        :param context:
            A string to determine where you are working. project:service:version
        """
        if not valid_envvar("PROJECT"):
            #create project
            self.validate_project_name(context)
            self.validate_gcloud_projects()
            self.set_env()
            self.set_terminal_prompt()
        else:
            #set path to change dir
            #set conda env
            #set gcloud project
            #set terminal prompt
            #serach for service
            if not valid_envvar("SERVICE"):
                #create service
                pass

            else:
                pass
                #change to service



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






if __name__ == '__main__':
    fire.Fire(SetContext)



