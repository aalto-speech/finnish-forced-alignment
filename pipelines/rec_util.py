#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The sed operation, this code returns the file name to, is not handled here
# due to python2 utf-8, ascii, and unicode encoding risks

import sys

def main(arguments):
    try:
        txt_index = arguments.index("--txt")
        print arguments[txt_index + 1]
    except ValueError:
        print "-1"


if __name__ == "__main__":
    main(sys.argv[1:])
