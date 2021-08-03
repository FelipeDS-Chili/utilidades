
import argparse
import os
import shutil
import sys
from os.path import expanduser
# Import from the standard library
from shutil import copytree, ignore_patterns
# from six.moves import input
from subprocess import call



def search_replace(path, filename, word, newword):
    """ Open file search/replace and save inplace
    busca archivo y reemplaza word por otra
    """
    res = []
    with open('{}/{}'.format(path, filename), 'r') as myfile:
        for line in myfile.readlines():
            if line.count(word):
                # line = sub('\b{}\b'.format(word), newword, line)
                line = line.replace(word, newword)
            res.append(line)
    with open('{}/{}'.format(path, filename), 'w') as myfile:
        myfile.writelines(res)


def get_parser():
    usage = ('%(prog)s PKG_NAME [-d DESC] [-g GROUP] [-T TOKEN] '
             '[-c NAME -- EMAIL] [-r NAME  ]\n'
             '')
    description = 'Create a python package'

    default_msg = 'Project Description'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument(dest='pkg_name', action='store',
                        help=('Package name '
                              ' e.g. %(prog)s --package-name lpmchurn'))
    parser.add_argument('-d', '--description', dest='description', nargs='?',
                        action='store', default=default_msg,
                        help=('Package description'
                              ' e.g. %(prog)s lpm_churn -d'
                              ' "lpm churn score engine"'))
    parser.add_argument('--gitlab', '-gl',
                        action='store_true',
                        help=('Package description'
                              ' e.g. %(prog)s lpm_churn -d'
                              ' "lpm churn score engine"'))

    return parser

    # Way to use
    # parser = get_parser()
    # args = parser.parse_args()
    # pkg_name = args.pkg_name
    # description = args.description

    # gitconfig = expanduser('~/.gitconfig')

    # # create sample files in a folder
    # dirname = os.path.dirname
    # source = dirname(os.path.abspath(packmlproject.__file__)) + '/data/skeleton'
    # if os.path.isdir(pkg_name):
    #     sys.exit('{} already exist'.format(pkg_name))
    # copytree(source, pkg_name, ignore=ignore_patterns('*.pyc', '__pycache__'))
    # # search replace in skeletion files
    # print('  => New python package {} created'.format(pkg_name))
    # pkgn = pkg_name
    # search_replace(pkgn, 'setup.py', 'proyecto_description', description)
    # search_replace(pkgn, 'setup.py', "'proyecto'", "'{}'".format(pkg_name))
    # search_replace(pkgn, 'setup.py', "'proyecto/", "'{}/".format(pkg_name))
