import tajweed_classifier as tc    # The code to test
import unittest   # The test framework
from collections import deque, namedtuple
from tree import Exemplar, json2tree
import glob
import json
import os

def getTree():
    # Load rules from incredibly high-tech datastore.
    rule_trees = {}
    rule_start_files = glob.glob("rule_trees/*.start.json")
    for start_file in rule_start_files:
        rule_name = os.path.basename(start_file).partition(".")[0]
        end_file = start_file.replace(".start.", ".end.")
        rule_trees[rule_name] = {
            "start": json2tree(json.load(open(start_file))),
            "end": json2tree(json.load(open(end_file))),
        }
    return rule_trees

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_output_basmala(self):
        rules = getTree()
        text =  "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
        result=tc.label_ayah((1, 1, text, rules))
        print(len(text))
        print(result)

if __name__ == '__main__':
    unittest.main()
