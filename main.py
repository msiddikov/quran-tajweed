from collections import deque, namedtuple
from tree import Exemplar, json2tree
import glob
import json
import multiprocessing
import os
import sys
import unicodedata
import tajweed_classifier as tc
    
# Load rules from incredibly high-tech datastore.
rule_trees = {}
rule_start_files = glob.glob("output/rule_trees/*.start.json")
for start_file in rule_start_files:
    rule_name = os.path.basename(start_file).partition(".")[0]
    end_file = start_file.replace(".start.", ".end.")
    rule_trees[rule_name] = {
        "start": json2tree(json.load(open(start_file))),
        "end": json2tree(json.load(open(end_file))),
    }

# Read in text to classify
tasks = ["بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"]
for line in sys.stdin:
    line = line.split("|")
    if len(line) != 3:
        continue
    tasks.append((int(line[0]), int(line[1]), line[2].strip(), rule_trees))

# Perform classification.
print(tasks)
with multiprocessing.Pool() as p:
    results = p.map(tc.label_ayah, tasks)

# Pretty-print output because disk space is cheap.
json.dump(results, sys.stdout, indent=2, sort_keys=True)
print("")