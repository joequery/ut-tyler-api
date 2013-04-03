# Convenient functions for testing
import os
def testfile(path):
    return open(os.path.join("tests", "testfiles", path))

