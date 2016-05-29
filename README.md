# po-utils
Some utils I use to manage PO files for my JavaScript apps

js2pot.py scrapes strings from the js/ and plugins/ subdirectorys to
update the project POT file.  Usage is:

<pre>
python js2pot.py TopLevelProjectDirectory ProjectPOTPath
</pre>

pot2po.py updates the strings found in an individual PO file from the
project POT file.  Usage is:

<pre>
python pot2po.py ProjectPOTPath POFilePath
</pre>

There is an optional 3rd argument that can be used to specify a second
PO file from which to extract TRANS messages.  For example, if you
wanted to add Spanish hints to the Aymara PO file:

<pre>
python pot2po.py MusicBlocks/po/MusicBlocks.pot MusicBlocks/po/ayc.po MusicBlocks/po/es.po
</pre>

po2po.py will mine a PO file for msgstrs that are missing in a second
po file.  Usage is:

<pre>
python po2po.py SourcePOFilePath TargetPOFilePath [-i, --ignorecase]
</pre>

The SourcePOFile is a PO file that contains potentially useful
strings. The TagetPOFile is the PO file in need of additional
translations. Note that the result is placed in a third file, tmp.po

If the --ignorecase argument is given, the case of the msgid in Source
is ignored.

Note: I am using a simple schema for TRANS notes in my code:
<pre>
    //.TRANS: a message to the translator goes here
</pre>
