"""
Functions for provisioning environments with fabtools (eat shit puppet!)
"""
# standard library
import sys
import copy
import os
from distutils.util import strtobool

# 3rd party
import fabric
from fabric.api import env, task, local, run, settings, cd, sudo, lcd

# local
import decorators
import utils


@task(default=True)
@decorators.needs_environment
def default():
    with cd('/vagrant/'):
        run('python runappserver.py')
                
