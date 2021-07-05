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
Global variable for local git repo.
"""
PATH = pathlib.Path.home() / "git"


class CONTEXT:
    """

    Enum type class to remove strings from code.
    These are the essential environment variable names.

    """
    PROJECT = "PROJECT"
    SERVICE = "SERVICE"
    VERSION = "VERSION"


def is_environment_variable_valid(var: str) -> bool:
    """

    Function to check if variable exists and is non-empty.

    :param var:
        Name of the environment variable.
    :return:
    """
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

def does_service_version_exist(service_or_version_name: str) -> bool:
    """

    Function to test if the service or version exists. Essentially checking if a sub namespace exists.

    :param service_or_version_name:
        Name of the service or version

    :return:
        True if the path is an existing directory.
    """
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

def set_context_env_variable(context_type: str, value: str) -> None:
    """

    :param context_type:
        The type of variable replaced to set context, either PROJECT, SERVICE or VERSION

    :param value:
        The value to set for the environment variable.

    """
    type_upper = context_type.upper()
    if type_upper in ["PROJECT", "SERVICE", "VERSION"]:
        print(f"echo Setting {type_upper} to {value};")
        print(f"export {type_upper}={value};")


def clear_context_env_variables():
    """

    Sets the context environment variables to '' to avoid shell navigation errors. If a user sets the contexts to a project
    from a lower namespace such as a service or a version, we will want the environment variables to be empty.

    """
    for var in ["PROJECT", "SERVICE", "VERSION"]:
        set_context_env_variable(context_type=var, value='')


def pprint(msg: str, color: str = 'default', indent: int = 0) -> None:
    """

    Print's colored text to the terminal with arguments for indents

    :param msg:
        The message

    :param color:
        Termcolor.cprints colors 'red', 'green', 'blue'

    :param indent:
        The amount of tabs you want precedding your message.
    """
    cprint("\t"*indent + msg, color)


class SetContext(object):

    def change_directory_path(self,
                              project_name=None,
                              service_name=None,
                              version_name=None):
        """
        This builds the path of the project from environment variables. If no project environment variables exist,
        Then the directory defaults to ~/git

        eval `python setcontext.py build_directory_path`
        """
        path = PATH
        if project_name:
            path /= project_name

        if service_name:
            path /= service_name

        if version_name:
            path /= version_name

        # add beta or alpha flags

        path_str = path.absolute().as_posix()

        if path.is_dir():
            print(path_str)

        else:
            path.mkdir(parents=True, exist_ok=True)
            print(path_str)
    #memoize

    def set_terminal_prompt(self):
        """

        Outputs a string to be evaluated by bash that will set the terminal prompt based on environment variables.
        Can be run from bash: eval `python setcontext.py set_terminal_prompt`

        """
        prompt_string = "PS1="

        if is_environment_variable_valid(CONTEXT.PROJECT):
            prompt_string += "'%F{55}'${PROJECT}"

        if is_environment_variable_valid(CONTEXT.SERVICE):
            prompt_string += "'%F{default}:%F{46}'${SERVICE}"

        if is_environment_variable_valid(CONTEXT.VERSION):
            prompt_string += "'%F{default}:%F{38}'${VERSION}"

        prompt_string += "'%F{default} >> '"
        print(prompt_string)




    def create_gcloud_project(self, project_name: str) -> None:
        """

        Outputs a string to be evaluated by bash that will create a gcloud project.
        Can be run from bash: eval `python setcontext.py create_gcloud_project --project_name=<project_name>`

        :param project_name:
            The name of the project gcloud will create
        """
        print(f"gcloud components update --quiet && gcloud projects create {project_name}")

    def create_conda_env(self, env_name: str) -> None:
        """

        Outputs a string to be evaluated by bash that will create a conda environment.

        :param env_name:
            The name of the conda environment, it is meant to match the project name
        """
        print(f"conda create -y -q --name {env_name} python=3.9")

    def set_conda_env(self, env_name: str) -> None:
        """

        Outputs a string to be evaluated by bash that will set the conda environment.

        :param env_name:
        """
        print(f"conda activate {env_name}")

    def create_git_repo(self):
        """

        Outputs a string to be evaluated by bash that will initialize a git remo and use hub create to create a remote repo.

        """
        print("git init && hub create")

    def print_project_variables(self):
        pprint(os.environ[CONTEXT.PROJECT], 'red', 2)
        pprint(os.environ[CONTEXT.SERVICE], 'red', 2)
        pprint(os.environ[CONTEXT.VERSION], 'red', 2)



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
            clear_context_env_variables()
            set_context_env_variable(CONTEXT.PROJECT, project)
            if does_project_exist(project):

                self.change_directory_path(project_name=CONTEXT.PROJECT)
                self.set_conda_env(env_name=CONTEXT.PROJECT)


            else:
                if not does_gcloud_project_exist():
                    self.change_directory_path(project_name=CONTEXT.PROJECT)
                    self.create_gcloud_project(project_name=CONTEXT.PROJECT)
                    self.create_conda_env(env_name=CONTEXT.PROJECT)
                    self.create_git_repo()

            if service:
                set_context_env_variable(CONTEXT.SERVICE, service)
                if does_service_version_exist(service) and not version:
                    self.change_directory_path(project_name=CONTEXT.PROJECT,
                                               service_name=CONTEXT.SERVICE)


                else:
                    #create service
                    self.change_directory_path(project_name=CONTEXT.PROJECT,
                                               service_name=CONTEXT.SERVICE,
                                               version_name='v001')

                if version:
                    set_context_env_variable(CONTEXT.VERSION, version)
                    self.change_directory_path(project_name=CONTEXT.PROJECT,
                                               service_name=CONTEXT.SERVICE,
                                               version_name=CONTEXT.VERSION)
            self.set_terminal_prompt()






            is_project_name_valid(namespace)













if __name__ == '__main__':
    fire.Fire(SetContext)



