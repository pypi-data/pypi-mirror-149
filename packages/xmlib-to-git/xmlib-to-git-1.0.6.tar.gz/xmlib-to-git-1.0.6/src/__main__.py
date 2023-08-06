#!/usr/bin/python3

import getopt
import os
import sys

from .processor import parse_xml
from .utils.validator import check_xml
from sys import exit
from .__version__ import __version__, show_version
from . import settings
from . import usage

this_dir, this_filename = os.path.split(__file__)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    inputfile = ""
    opts = ""
    git_repo = ""

    try:
        opts, args = getopt.getopt(
            argv,
            "hV:f:o:n:g:c",
            [
                "help",
                "version",
                "file=",
                "name=",
                "git-repository-ssh=",
                "out-folder=",
                "customer=",
            ],
        )
    except getopt.GetoptError:
        usage.usage()
        exit(2)

    settings.init()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit()
        elif opt in ("-V", "--version"):
            show_version()
            exit()
        elif opt in ("-f", "--file"):
            inputfile = arg
        elif opt in ("-c", "--customer-id"):
            settings.CUSTOMER = arg
        elif opt in ("-o", "--out-folder"):
            settings.FOLDER = arg
        elif opt in ("-n", "--name"):
            settings.APP_NAME = arg
        elif opt in ("-g", "--git-repository-ssh"):
            settings.GIT_REPO = arg
    settings.SRC_DIR = this_dir

    if inputfile == "":
        print("le paramètre -f est obligatoire")
        usage.usage()
        exit(2)
    if settings.APP_NAME == "":
        print("le paramètre -n est obligatoire")
        usage.usage()
        exit(2)

    settings.APP_DIR = "{}/{}".format(settings.FOLDER, settings.APP_NAME)
    check_xml(inputfile)
    parse_xml(inputfile)


if __name__ == "__main__":
    main()
