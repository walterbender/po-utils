# po-utils
Some utils I use to manage PO files for my JavaScript apps

js2pot.py scrapes strings from the js/ and plugins/ subdirectorys to update the project POT file.
Usage is:
<pre>
python js2pot.py TopLevelProjectDirectory ProjectPOTPath
</pre>

pot2po.py updates the strings found in an individual PO file from the project POT file.
Usage is:
<pre>
python pot2po.py ProjectPOTPath POFilePath
</pre>

There is an optional 3rd argument that can be used to specify a second PO file from which to extract TRANS messages.
For example, if you wanted to add Spanish hints to the Aymara PO file:
<pre>
python pot2po.py MusicBlocks/po/MusicBlocks.pot MusicBlocks/po/ayc.po MusicBlocks/po/es.po
</pre>
