#!/usr/bin/env python -*- coding: utf-8 -*- 2015, 16 - Walter Bender
#<walter@sugarlabs.org> Makes sure po files have all the strings found
#in a pot file.

# How to use: script.py pot-file po-file (optional second po file to be used
# for #TRANS help, e.g., add Spanish to Aymara strings.

# Outputs to po-file.po_

import os
import re
import sys
import codecs


def convert_pot_to_po(pot_filename, po_filename, trans_filename):

    # Read data from the existing POT file
    pot_fd = codecs.open(pot_filename, 'r', 'UTF-8')
    pot_list = []

    trans_note = []
    pot_trans_dict = {}  # //.TRANS

    line_numbers = []
    pot_line_numbers_dict = {}

    for line in pot_fd:
        if line[0:2] == '#:':
            line_numbers.append(line)
        elif line[0:2] == '#.':
            trans_note.append(line)
        elif line[0:5] == 'msgid':
            key = line[7:-2]
            pot_list.append(key)

            if len(trans_note) > 0:
                pot_trans_dict[key] = trans_note
                trans_note = []

            if len(line_numbers) > 0:
                pot_line_numbers_dict[key] = line_numbers
                line_numbers = []

    pot_fd.close()

    # Read data from the trans file
    if trans_filename == '':
        trans_dict = {}
    else:
        trans_fd = codecs.open(trans_filename, 'r', 'UTF-8')

        trans_dict = {}

        for line in trans_fd:
            if line[0:2] == '#:':
                continue
            elif line[0:2] == '#.':
                continue
            elif line[0:5] == 'msgid':
                key = line[7:-2]
            elif line[0:6] == 'msgstr':
                trans_dict[key] = line[8:-2]

        trans_fd.close()

    po_fd = codecs.open(po_filename, 'r', 'UTF-8')
    po_dict = {}
    po_header = ''

    trans_note = []
    po_trans_dict = {}  # //.TRANS

    line_numbers = []
    po_line_numbers_dict = {}

    end_of_header = False;

    for line in po_fd:
        if line[0:2] == '#:':
            line_numbers.append(line)
        elif line[0:2] == '#.':
            end_of_header = True
            trans_note = line
        elif line[0:5] == 'msgid':
            key = line[7:-2]
            if key != '':
                end_of_header = True
        elif line[0:7] == '#~msgid':
            key = line[9:-2]
            if key != '':
                end_of_header = True
        elif line[0:6] == 'msgstr':
            if key == '':
                continue

            value = line[8:-2]
            po_dict[key] = value

            if len(trans_note) > 0:
                po_trans_dict[key] = trans_note
                trans_note = []

            if len(line_numbers) > 0:
                po_line_numbers_dict[key] = line_numbers
                line_numbers = []
        elif line[0:8] == '#~msgstr':
            if key == '':
                continue

            value = line[10:-2]
            po_dict[key] = value

            if len(trans_note) > 0:
                po_trans_dict[key] = trans_note
                trans_note = []

            if len(line_numbers) > 0:
                po_line_numbers_dict[key] = line_numbers
                line_numbers = []

        if not (end_of_header or line[0:5] == 'msgid'):
            po_header += line

    po_fd.close()

    output = codecs.open(po_filename + '_', 'w', 'UTF-8')
    output.write(po_header)

    for i in range(len(pot_list)):
        if pot_list[i] == '':
            continue

        if pot_list[i] in pot_line_numbers_dict:
            for j in range(len(pot_line_numbers_dict[pot_list[i]])):
                output.write('%s' % (pot_line_numbers_dict[pot_list[i]][j]))

        if pot_list[i] in pot_trans_dict:
            for j in range(len(pot_trans_dict[pot_list[i]])):
                output.write('%s' % (pot_trans_dict[pot_list[i]][j]))

        if pot_list[i] in trans_dict:
            output.write('#.TRANS: %s\n' % (trans_dict[pot_list[i]]))

        if pot_list[i] in po_dict:
            output.write('msgid "%s"\nmsgstr "%s"\n\n' % (pot_list[i], po_dict[pot_list[i]]))
        else:
            output.write('msgid "%s"\nmsgstr ""\n\n' % (pot_list[i]))

    for phrase in po_dict:
        if not phrase in pot_list:
            if phrase in po_line_numbers_dict:
                for j in range(len(po_line_numbers_dict[phrase])):
                    output.write('%s\n' % (po_line_numbers_dict[phrase][j]))

            if phrase in pot_trans_dict:
                for j in range(len(pot_trans_dict[phrase])):
                    output.write('%s' % (pot_trans_dict[phrase][j]))

            if phrase in trans_dict:
                output.write('#.TRANS: %s\n' % (trans_dict[phrase]))

            output.write('#~msgid "%s"\n#~msgstr "%s"\n\n' % (phrase, po_dict[phrase]))

    output.close()


if __name__ == '__main__':
    if len(sys.argv) == 4:
        ini = convert_pot_to_po(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        ini = convert_pot_to_po(sys.argv[1], sys.argv[2], '')
