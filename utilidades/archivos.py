
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
