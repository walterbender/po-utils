#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2015,16 - Walter Bender <walter@sugarlabs.org>
# This is for the .po file.
# How to use: script.py file-old.po file-new.po

# This script will mine an old po file for any untranslated strings in a new po file.

import os
import re
import sys


def mine_from_po_to_po(oldfilename, newfilename):
    oldfd = open(oldfilename, "r")
    newfd = open(newfilename, "r")
    output = open('tmp.po', "w")

    olddict = {}
    for line in oldfd:
        if line[0:5] == 'msgid':
            key = line[7:-2]
        if line[0:6] == 'msgstr':
            value = line[8:-2]
            olddict[key] = value;

    newdict = {}
    for line in newfd:
        msgstr_flag = False
        if line[0:5] == 'msgid':
            key = line[7:-2]
        if line[0:6] == 'msgstr':
            value = line[8:-2]
            msgstr_flag = True

        if msgstr_flag and value == '' and  key in olddict:
            output.write('msgstr "%s"\n' % (olddict[key]))
        else:
            output.write(line);

    output.close()


if __name__ == '__main__':
    ini = mine_from_po_to_po(sys.argv[1], sys.argv[2])
    print "Finished"
