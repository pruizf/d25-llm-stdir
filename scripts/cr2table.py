import os
import sys
import re


outf = sys.argv[1].replace(".txt", ".tsv")
with open(sys.argv[1], "r") as f:
    txt = f.read()
    txt = re.sub(re.compile(r"^\s+", re.M), "", txt)
    txt = re.sub("^precision", "\tprecision", txt)
    tabbed = re.sub(r" {2,}", "\t", txt)

with open(outf, "w") as of:
    of.write(tabbed)
