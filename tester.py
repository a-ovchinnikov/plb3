#!/bin/env python3
"""Initial code for processing test files

Test files format is described in tests/sample_test.py

sreader is lifted as is from
~/code/my_codes/python/project_octowizardry/sreader.py
It must be moved someplace safe first.

А вообще, конечно, надо продумать структуру интерпретеров и
тестов к ним, а то свинарник какой-то.
"""

import os
import sys
from sreader import *
import comp
from comp import compfile

from utils import TimeIt

# This is a C library
from spam import CBFI


def extract_context(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    return "\n".join(l[2:].rstrip() for l in lines if l and l.startswith("#>"))


compilation_timer = TimeIt("Compilation")
execution_timer = TimeIt("Execution")
total_timer = TimeIt("Total")
linescount = 0
code_len = 0
steps_taken = 0


def linectr(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [l for l in lines if l and l.lstrip() and l.lstrip()[0] != "#" and l.replace(")", "").replace(",", "").lstrip().rstrip()]
    global linescount
    linescount += len(lines)

def run_test(test_fname="tests/sample_prog.py", verbose=False):
    try:
        test_context = sreader(extract_context(test_fname))[0]
    except IndexError:
        return "", True, []
    tname = test_context[0]
    # Very bad! But this correction makes tests runs more than twice as fast!
    # 1.57 with correction
    # 3.54 without          -- x2.25
    # This also probably means that there is a memory leak.
    comp.memptr = 0
    comp.mmry = [None] * 2**12
    linectr(test_fname)
    code = compilation_timer(lambda: compfile(test_fname))
    global code_len
    global steps_taken
    code_len += len(code)
    test_context.append(["code", code])
    if os.getenv("BF_SLOW_MODE") == "1":
        t = BFTest(test_context)
    else:
        t = BFTest(test_context, CBFI)
    r, d = execution_timer(lambda: t.run())
    steps_taken += t.steps_taken
    if not r:
        print (f"{tname:<49.49}", "NO!\n", "".join(d))
    else:
        if verbose:
            print(f"{tname:<50.50}", "yes")
    return tname, r, d

def run_tests():
    failures = []
    count = 0
    failed_fnames = []
    try:
        with open("failed_tests_in_last_run.swp", "r") as f:
            ffnames = f.readlines()
    except FileNotFoundError:
        ffnames = []
    if ffnames:
        fnames = [fn.rstrip("\n") for fn in ffnames]
    else:
        fnames = sorted(os.listdir("tests"))
    print("--Tests" + "-"*47)
    for el in fnames:
        if el != "sample_test.py" and el.endswith("py"):
            tn, r, d = run_test("tests/"+el, True)
            count += 1
            if not r:
                failures.append((tn, "".join(d)))
                failed_fnames.append(el)
    if failures:
        print ("==Failures" + "="*44)
        for _id, (tn, d) in enumerate(failures, start=1):
            print (f"{_id}) {tn}\n{d}")

    with open("failed_tests_in_last_run.swp", "w") as f:
        for fn in failed_fnames:
            f.write(fn)
            f.write("\n")
    print("-"*54)
    print (f"All done! Ran {count} tests of which {len(failures)} failed.")


def print_run_stats():
    print("=")
    #print(f"Compilation: {compilation_timer.runtime}")
    #print(f"Execution  : {execution_timer.runtime}")
    #print(f"Total      : {total_timer.runtime}")
    compilation_timer.print_report()
    execution_timer.print_report()
    total_timer.print_report()
    print(f"Line count : {linescount}")
    print(f"Code length: {code_len}; steps taken: {steps_taken}")
    # This does not workl for short tests.
    print(f"Execution speed: "
          f"{steps_taken/(1000*execution_timer.runtime.total_seconds()):.1f} Kstep/s")

if __name__ == "__main__":
    if len(sys.argv) <=1:
        total_timer(lambda: run_tests())
    elif len(sys.argv) == 2:
        tn, r, d = total_timer(lambda: run_test(sys.argv[1], True))
    print_run_stats()
