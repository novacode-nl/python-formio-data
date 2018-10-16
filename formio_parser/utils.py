# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import os

def readfile(dir_path, filename):
    cwd = os.path.dirname(os.path.realpath(__file__))
    path = '%s/%s/%s' % (cwd, dir_path, filename)
    with open(path, "r") as fp:
        return fp.read()
