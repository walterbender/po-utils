#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2016 - Walter Bender <walter@sugarlabs.org>
# Create or update pot file based on js files.
# How to use: script.py js-path pot-file
# Outputs to pot-file_

import os
import re
import sys
import glob
import string


def mine_js_files(js_pathname, pot_filename):

    # Read data from the existing POT file
    pot_fd = open(pot_filename, "r")
    pot_list = []

    trans_note = []
    pot_trans_dict = {}  # //.TRANS

    pot_line_numbers = []
    pot_line_numbers_dict = {}

    pot_header = ''
    end_of_header = False;

    for line in pot_fd:
        if line[0:2] == '#:':
            pot_line_numbers.append(line)
            end_of_header = True
        elif line[0:2] == '#.':
            trans_note.append(line)
            end_of_header = True
        elif line[0:5] == 'msgid':
            key = line[7:-2]
            pot_list.append(key)

            if not key == '':
                end_of_header = True

            if len(trans_note) > 0:
                pot_trans_dict[key] = trans_note
                trans_note = []

            if len(pot_line_numbers) > 0:
                pot_line_numbers_dict[key] = pot_line_numbers
                pot_line_numbers = []

        if not end_of_header:
            pot_header += line
    
    # Mine strings for l23n from js files.
    js_files = glob.glob(os.path.join(js_pathname, 'js', '*js'))
    print js_files

    js_list = []

    trans_note = []
    js_trans_dict = {}  # //.TRANS

    js_line_numbers = []
    js_line_numbers_dict = {}

    for path in js_files:
        basename = os.path.basename(path)
        js_fd = open(path, "r")

        count = 1
        for line in js_fd:
            tmp = line.split('//.TRANS')
            if len(tmp) > 1:
                trans_note.append(tmp[1])

            tmp = line.split('_("')            
            if len(tmp) > 1:
                for i in range(len(tmp)):
                    if i == 0:
                        continue
                    phrase = tmp[i].split('")')[0];

                    if phrase in js_list:
                        js_line_numbers_dict[phrase].append('js/%s:%d' % (basename, count))
                    else:
                        js_list.append(phrase)
                        js_line_numbers_dict[phrase] = ['js/%s:%d' % (basename, count)]

                    if len(trans_note) > 0:
                        if phrase in js_trans_dict:
                            for note in trans_note:
                                js_trans_dict[phrase].append(note)
                        else:
                            js_trans_dict[phrase] = trans_note
                        trans_note = []

            tmp = line.split("_('")            
            if len(tmp) > 1:
                for i in range(len(tmp)):
                    if i == 0:
                        continue
                    phrase = tmp[i].split("')")[0];

                    if phrase in js_list:
                        js_line_numbers_dict[phrase].append('js/%s:%d' % (basename, count))
                    else:
                        js_list.append(phrase)
                        js_line_numbers_dict[phrase] = ['js/%s:%d' % (basename, count)]

                    if len(trans_note) > 0:
                        if phrase in js_trans_dict:
                            for note in trans_note:
                                js_trans_dict[phrase].append(note)
                        else:
                            js_trans_dict[phrase] = trans_note
                        trans_note = []

            count += 1

    rtp_files = glob.glob(os.path.join(js_pathname, 'plugins', '*rtp'))
    print rtp_files

    for path in rtp_files:
        basename = os.path.basename(path)
        js_fd = open(path, "r")

        count = 1
        for line in js_fd:
            tmp = line.split('//.TRANS')
            if len(tmp) > 1:
                trans_note.append(tmp[1])

            tmp = line.split('_("')            
            if len(tmp) > 1:
                for i in range(len(tmp)):
                    if i == 0:
                        continue
                    phrase = tmp[i].split('")')[0];

                    if phrase in js_list:
                        js_line_numbers_dict[phrase].append('plugins/%s:%d' % (basename, count))
                    else:
                        js_list.append(phrase)
                        js_line_numbers_dict[phrase] = ['plugins/%s:%d' % (basename, count)]

                    if len(trans_note) > 0:
                        if phrase in js_trans_dict:
                            for note in trans_note:
                                js_trans_dict[phrase].append(note)
                        else:
                            js_trans_dict[phrase] = trans_note
                        trans_note = []

            tmp = line.split("_('")            
            if len(tmp) > 1:
                for i in range(len(tmp)):
                    if i == 0:
                        continue
                    phrase = tmp[i].split("')")[0];

                    if phrase in js_list:
                        js_line_numbers_dict[phrase].append('plugins/%s:%d' % (basename, count))
                    else:
                        js_list.append(phrase)
                        js_line_numbers_dict[phrase] = ['plugins/%s:%d' % (basename, count)]

                    if len(trans_note) > 0:
                        if phrase in js_trans_dict:
                            for note in trans_note:
                                js_trans_dict[phrase].append(note)
                        else:
                            js_trans_dict[phrase] = trans_note
                        trans_note = []

            count += 1

    output = open(pot_filename + '_', 'w')
    output.write(pot_header)
    
    for i in range(len(js_list)):
        for j in range(len(js_line_numbers_dict[js_list[i]])):
            output.write('#: %s\n' % (js_line_numbers_dict[js_list[i]][j]))

        if js_list[i] in js_trans_dict:
            for j in range(len(js_trans_dict[js_list[i]])):
                output.write('#.TRANS: %s' % (js_trans_dict[js_list[i]][j]))

        new_phrase = string.replace(js_list[i], '"', '\\"')
        output.write('msgid "%s"\nmsgstr ""\n\n' % (new_phrase))

    for i in range(len(pot_list)):
        if pot_list[i] in js_list:
            continue;

        if pot_list[i] in pot_line_numbers_dict:
            for j in range(len(pot_line_numbers_dict[pot_list[i]])):
                output.write('%s' % (pot_line_numbers_dict[pot_list[i]][j]))

        if pot_list[i] in pot_trans_dict:
            for j in range(len(pot_trans_dict[pot_list[i]])):
                output.write('%s' % (pot_trans_dict[pot_list[i]][j]))

        output.write('#~msgid "%s"\n#~msgstr ""\n\n' % (pot_list[i]))

    output.close()


if __name__ == '__main__':
    print sys.argv[2]
    ini = mine_js_files(sys.argv[1], sys.argv[2])
