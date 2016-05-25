#!/usr/bin/env python3

import sys

def extract_failed(filename):
    """Extract which bmrb files are failed in nmrstarlib."""
    with open(filename, "r") as infile:
        text = infile.readlines()

    failed = []
    for line in text:
        if line.startswith("FAIL"):
            failed.append(line.split())

    return failed


if __name__ == "__main__":
    script = sys.argv.pop(0)
    filename = sys.argv.pop(0)

    failedbmrbs = extract_failed(filename)
    # print(failedbmrbs)
    # print(len(failedbmrbs))

    failedids = [item[1] for item in failedbmrbs]
    print(failedids)
    # for bmrbid in failedids:
    #     print(bmrbid)