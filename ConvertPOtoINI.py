#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2014 - Ignacio Rodríguez <ignacio@sugarlabs.org>
# This is for the .po file.
# How to use: script.py file.po, it will write a file.ini

import os
import re
import sys

def convert_po_to_ini(filename):
    text = open(filename, "r").read()
    lang = os.path.basename(filename)[:-3]
    # if lang = english don't add it to head
    finaltext = ""
    if lang != "en":
        finaltext += "[" + lang + "]\n"

    REPLACE = [
        ",",
        "(",
        ")",
        "?",
        "¿",
        "<",
        ">",
        ".",
        '"\n',
        '"',
        ":",
        "%s",
        "%d",
        "/",
        "'",
        ";",
        "×",
        "¡",
        "!"]

    for match in re.finditer(
            r'^msgid "([^"]+)"\n^msgstr "([^"]+)"', text, flags=re.M):
        msgid, msgstr = match.groups()

        for x in REPLACE:
            msgid = msgid.replace(x, "")

        msgid = msgid.replace(" ", "-")
        msgstr = msgstr.replace('\n', " ")
        txt = msgid + ' = %s\n' % (msgstr)
        if not txt.startswith(" = "):
            finaltext += txt

    return finaltext, lang

if __name__ == '__main__':
    ini = convert_po_to_ini(sys.argv[1])
    text_n = open(ini[1] + ".ini", "w")
    text_n.write(ini[0])
    text_n.close()
    print("Finished")
