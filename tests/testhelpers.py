# Convenient functions for testing
import os
def testfile(path):
    return open(os.path.join("tests", "testfiles", path))

def header(s):
    print("=" * 80)
    print(s)
    print("=" * 80)
