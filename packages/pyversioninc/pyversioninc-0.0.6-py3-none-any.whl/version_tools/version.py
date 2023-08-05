import os
import errno
from pathlib import Path
import re
import logging as log


def get_releases(project_dir, verbose=False):
    """

    :param verbose: show logs or not
    :param project_dir:
    :return:
    """

    # defining the distributions path
    dist_path = os.path.join(project_dir, 'dist')
    if verbose:
        log.info('INFO: \n In get_releases \n The path is: ', dist_path)

    try:
        # getting distibution by date order
        releases = sorted(Path(dist_path).iterdir(), key=os.path.getmtime)
        if verbose:
            log.info('INFO: \n In get_releases \n The releases is: ', releases)
    except:
        # Raising an exception if the path is not found
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), dist_path)

    return [str(release) for release in releases]


def get_current_version(project_dir: str, verbose=False):
    """
    Function to get the current version of the package.

    :param verbose: show logs or not
    :param project_dir: The project directory path.
    :return:

    #Note that at the begining ther may not be a dist folder containing the releases.
    """
    try:
        current_release = re.search(r'\d+(\.\d+)+', get_releases(project_dir, verbose)[-1]).group()
        if verbose:
            log.info('INFO: \n In get_current_version \n The release is: ', current_release)
    except:
        log.info('There is no version of the package in the dist folder.')
        current_release = input("Please specify a release version: ")

    return current_release


def get_previous_version(project_dir: str, verbose=False):
    """
    Function to get the previous version of the package.
    :param verbose: show logs or not
    :param project_dir: The project directory path.
    :return:
    #Note that at the begining ther may not be a dist folder containing the releases.
    """
    len_releases = len(get_releases(project_dir, verbose))
    return get_releases(project_dir)[len_releases - 2].split('-')[1]


def increment_version(version: str, level: str = 'patch', verbose=False):
    """
    Function to increment the valeur of the package version
    :param verbose: show logs or not
    :param level:
    :param version: The current version
    :return:

    """
    if verbose:
        log.info('INFO: \n In increment_version \n The version is: ', version)
    major, minor, patch = version.split(".")

    if level == 'patch':
        patch = int(patch) + 1
    elif level == 'minor':
        minor = int(minor) + 1
        patch = 0
    else:
        major = int(major) + 1
        minor = 0
        patch = 0
    return '{}.{}.{}'.format(major, minor, patch)
