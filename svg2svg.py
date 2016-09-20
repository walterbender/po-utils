#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2016 - Walter Bender <walter@sugarlabs.org>
# Convert tspan strings in an SVG from one langauge to another using a PO file.
# How to use: script.py svg-path po-file
# Outputs to svg-file_

import os
import re
import sys
import glob
import string


def mine_svg_file(svg_filename, po_filename):

    # Read data from the existing PO file
    po_fd = open(po_filename, "r")
    po_dict = {}

    # Build a translation dictionary from the PO file
    for line in po_fd:
        if line[0:5] == 'msgid':
            key = line[7:-2]
        elif line[0:6] == 'msgstr':
            po_dict[key] = line[8:-2]

    # Mine strings for l23n from the svg.
    svg_list = []

    svg_fd = open(svg_filename, "r")
    tmp = svg_filename.split('.');
    output = open(tmp[0] + '_.svg', 'w')

    count = 1
    for line in svg_fd:
        tmp = line.split('</tspan>')
        if len(tmp) > 1:
            trans_line = ''
            tmp2 = tmp[0].split('>')
            for i in range(len(tmp2) - 1):
                trans_line += tmp2[i]
                trans_line += '>'
            if tmp2[-1] in po_dict:
                trans_line += po_dict[tmp2[-1]]
            else:
                trans_line += tmp2[-1]
            trans_line += '</tspan>'
            trans_line += tmp[1]
            output.write(trans_line)
        else:
            output.write(line)

    output.close()


if __name__ == '__main__':
    ini = mine_svg_file(sys.argv[1], sys.argv[2])
