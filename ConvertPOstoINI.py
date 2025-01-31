#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2014 - Ignacio Rodríguez <ignacio@sugarlabs.org>
# Convert all *.po files to ini, and put all in one
# How to use: python script.py

import os

from ConvertPOtoINI import convert_po_to_ini

print("Saving to myini.ini")

try:
    os.remove("myini.ini")
except:
    pass

dirlist = os.listdir(".")
final_ini = ""
if "en.po" in dirlist:
    dirlist.remove("en.po")
    dirlist.insert(0, "en.po")

total = 0
for fil_e in dirlist:
    if fil_e[-3:] == ".po":
        try:
            txt = convert_po_to_ini(fil_e)
            total += 1
            print("Successfully converted %s." % fil_e)
        except:
            print("Error with %s." % fil_e)
            continue

        final_ini += txt[0] + "\n"
        print(fil_e)

if not total:
    print("No PO or POT files to convert.")
    exit()
text_n = open("myini.ini", "w")
text_n.write(final_ini)
text_n.close()
