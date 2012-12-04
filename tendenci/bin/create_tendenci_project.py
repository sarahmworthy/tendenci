#!/usr/bin/env python

from __future__ import with_statement
from distutils.dir_util import copy_tree
from optparse import OptionParser
import os
from shutil import copy

from django.utils.importlib import import_module


def create_project():
    """
    Copies the contents of the project_template directory to the
    current directory.
    """
    parser = OptionParser(usage="usage: %prog")
    project_path = os.path.join(os.getcwd())

    # Create the list of packages to build from - at this stage it
    # should only be one or two names, tendenci plus an alternate
    # package.
    packages = ["tendenci"]
    for package_name in packages:
        try:
            __import__(package_name)
        except ImportError:
            parser.error("Could not import package '%s'" % package_name)

    # Build the project up copying over the project_template from
    # each of the packages.
    for package_name in packages:
        package_path = os.path.dirname(os.path.abspath(import_module(package_name).__file__))
        copy_tree(os.path.join(package_path, "project_template"), project_path)
        copy(os.path.join(project_path, ".env_example"),
             os.path.join(project_path, ".env"))

    # Clean up pyc files.
    for (root, dirs, files) in os.walk(project_path, False):
        for f in files:
            if f.endswith(".pyc"):
                os.remove(os.path.join(root, f))

if __name__ == "__main__":
    create_project()
