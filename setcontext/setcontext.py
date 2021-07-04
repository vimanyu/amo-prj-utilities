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

PATH = pathlib.Path.home() / "git"

class CONTEXT:
    PROJECT = "PROJECT"
    SERVICE = "SERVICE"
    VERSION = "VERSION"


def is_environment_variable_valid(var: str) -> bool:
    return (var in os.environ.keys()) and (os.environ[var] != "")

def is_project_name_valid(name: str) -> bool:
    patterns = '^[a-z0-9/-]*$'
    if re.search(patterns, name):
        return True
    else:
        return False

def does_gcloud_project_exist(project_name: str) -> bool:
    output = subprocess.check_output("gcloud projects list --format json".split(" "))
    json_str = output.decode('utf-8')
    json_data = json.loads(json_str)
    project_names = [project['name'] for project in json_data]

    return False if project_name in project_names else True

def does_project_exist(project_name: str) -> bool:
    path = PATH
    path /= project_name
    return path.is_dir()

def does_service_exist(service_or_version_name: str) -> bool:
    path = pathlib.Path.cwd()
    path /= service_or_version_name
    return path.is_dir()

def is_version_string_valid(version_string: str):
    #replace with regex
    return version_string.startswith("v") and version_string[1:].isdigit() and len(version_string) == 4

def split_namespace(namespace: str) -> tuple(str):
    project = ""
    service = ""
    version = ""

    # replace with argparse for better error handling and help?
    if not ":" in namespace:
        project = namespace
        service, version = ""

    else:
        split_context = namespace.split(":")
        split_count = len(split_context)

        if split_count == 2:
            project, service = split_context
            version = ''

        if split_count == 3:
            project, service, version = split_context
            is_version_string_valid(version)

    return project, service, version

def set_environment_variable(type: str, value: str):
    """

    :param type:
        The type of variable replaced to set context, either PROJECT, SERVICE or VERSION
    :param value:
    """
    type_upper = type.upper()
    if type_upper in ["PROJECT", "SERVICE", "VERSION"]:
        print(f"echo Setting {type_upper} to {value};")
        print(f"export {type_upper}={value};")


class SetContext(object):

    def change_directory_path(self, project=None, service=None, version=None):
        """
        This builds the path of the project from environment variables. If no project environment variables exist,
        Then the directory defaults to ~/git

        eval `python setcontext.py build_directory_path`
        """
        path = PATH
        if project:
            path /= project

        if service:
            path /= service

        if version:
            path /= version

        # add beta or alpha flags

        path_str = path.absolute().as_posix()

        if path.is_dir():
            print(path_str)

        else:
            path.mkdir(parents=True, exist_ok=True)
            print(path_str)
    #memoize


    def set_environment_variables(self, context_string=None):
        """
        Prints a string for a bash shell to evaulate.

        eval `python setcontext.py set_environment_variables myproject:myservice:v001`

        :param context_string:
            myproject:myservice:v001
        """
        project = ""
        service = ""
        version = ""

        # replace with argparse for better error handling and help?
        if not ":" in context_string:
            project = context_string
            service, version = ""

        else:
            split_context = context_string.split(":")
            split_count = len(split_context)

            if len(split_context) == 2:
                project, service = split_context
                version = ''

            if len(split_context) == 3:
                project, service, version = split_context
                is_version_string_valid(version)

        if is_project_name_valid(project):
            print(f"echo Setting PROJECT to {project};")
            print(f"export PROJECT={project};")

            print(f"echo Setting SERVICE to {service};")
            print(f"export SERVICE={service};")

            print(f"echo Setting VERSION to {version};")
            print(f"export VERSION={version};")


    """eval `python setcontext.py set_terminal_prompt`"""
    def set_terminal_prompt(self):
        prompt_string = "PS1="
        if is_environment_variable_valid("PROJECT"):
            prompt_string += "'%F{55}'${PROJECT}"
        if is_environment_variable_valid("SERVICE"):
            prompt_string += "'%F{default}:%F{46}'${SERVICE}"
        if is_environment_variable_valid("VERSION"):
            prompt_string += "'%F{default}:%F{38}'${VERSION}"


        prompt_string += "'%F{default} >> '"
        print(prompt_string)




    def create_project(self):
        pass

    def create_conda_env(self, env_name):
        print(f"conda create -y -q --name {env_name} python=3.9")

    def set_conda_env(self, env_name):
        print(f"conda activate {env_name}")

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



    def setcontext(self, namespace: str):
        """
        Main program to call all the sub functions for setting context between projects.
        This generates a bash script to be called from the shell and evaluated.

        Ex:
        eval `python setcontext.py setcontext my_project_name:my_service_or_module/v<001-999>

        :param namespace:
            A string to determine where you are working. project:service:version
        """

        project, service, version = split_namespace(namespace)
        if project and is_project_name_valid(project):
            if does_project_exist():


            else:
                if is_project_name_valid(project):
                    if not does_gcloud_project_exist():



            is_project_name_valid(namespace)



        if not is_environment_variable_valid("PROJECT"):
            if os.environ["PROJECT"] != namespace:


            #create project

            self.
            self.set_environment_variables()
            self.create_conda_env(os.environ['PROJECT'])
            self.set_conda_env(os.environ['PROJECT'])
            self.set_terminal_prompt()
        else:
            #set path to change dir
            self.change_directory_path(project=os.environ["PROJECT"])
            #set conda env
            #set gcloud project
            #set terminal prompt
            #serach for service
            if not is_environment_variable_valid("SERVICE"):
                #create service
                pass

            else:
                pass
                self.build_directory_path(project=os.environ["PROJECT"])
                #change to service



    @classmethod
    def pprint(cls, msg, color, indent=0):
        cprint("\t"*indent + msg, color)









if __name__ == '__main__':
    fire.Fire(SetContext)



