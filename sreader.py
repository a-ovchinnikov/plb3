"""Reader for S-expressions

It would be nice to store tests like this:
(simple-test (code +++++++++) (input 12345) (output 12345)
             (mem-after 1200100...) (steps-less-than 10**6))
To achieve this I need an S-expression reader. The reader will
return a list of strings or lists: anything atom-like will be
converted into a string, anything in parentheses will be converted
into a list.
"""
import os
from operator import add
from itertools import chain, repeat, zip_longest
from functools import namedtuple, reduce
from reprlib import Repr
from shutil import get_terminal_size

from bf import BFI


atom_separators = (" ", "\t", "\n")
comment_start_symbols = ("#", ";")
# Quick and dirty
def _sreader(s):
    def pop_until_newline(s):
        while s and s[0] != "\n":
            s.pop(0)
    s, out, current = list(s), [], []
    while s:
        ch = s.pop(0)
        if ch == '(':
            result, s = _sreader(s)
            if result:
                out.append(result)
        elif ch == ")":
            if current:
                out.append("".join(current))
            return out, s
        elif ch in atom_separators:
            if current:
                out.append("".join(current))
                current.clear()
        elif ch in comment_start_symbols:
            pop_until_newline(s)
        elif ch == "\"":  # an emdedded string
            current.append(ch)  # " is preserved to indicate that this is a string.
            while s and s[0] != "\"":
                current.append(s.pop(0))
            if s and s[0] == "\"":
                s.pop(0)
                current.append(ch)
            else:
                raise ValueError("Early termination of a string")
        else:
            current.append(ch)
    return out, s

# Use this for single lines.
# For reading multiline data use _sreader:
#  >>> _sreader("(foo\n(bar))\n\n\n(quux (meep))")
#  ([['foo', ['bar']], ['quux', ['meep']]], [])
def sreader(s):
    # Note r to make sure doctest works correctly with embedded \n
    r"""
    >>> sreader("(foo)")
    ['foo']
    >>> sreader("(foo bar)")
    ['foo', 'bar']
    >>> sreader("(foo (bar))")
    ['foo', ['bar']]
    >>> sreader("(foo      (bar))")
    ['foo', ['bar']]
    >>> sreader("(smoke-test1 (code +-))")
    ['smoke-test1', ['code', '+-']]
    >>> sreader("(smoke-test1 \n\t (code +-))")
    ['smoke-test1', ['code', '+-']]
    >>> sreader("(smoke-test1 \n\t (code +-)\n#(input 4)\n)")
    ['smoke-test1', ['code', '+-']]
    >>> sreader("(smoke-test1 \n\t (code +-)\n;(input 4)\n)")
    ['smoke-test1', ['code', '+-']]
    >>> sreader("(quux \n\t (f 0)\n(f 1) ;(f 4)\n(f 2))")
    ['quux', ['f', '0'], ['f', '1'], ['f', '2']]
    """
    out, s = _sreader(s)
    if s:
        print(f"W: some input was not processed -- {s}")
    # if out:  # If a line is not empty, i.e. not a comment.
    #     return out[0]
    return out  # This was a comment.

# Won't reallly work since this is _not_ a dict. This is not an assoc either
# This is a custom structure, deal with it as with a custom structure.
def stodict(sl):
    """Converts a test definition into a list"""

# A test can sit on two lines thus reading all data instead of by line.
def read_tests(fname="bfi.stests"):
    with open(fname, "r") as f:
        data = f.read()
    return data


class VerificationResult:
    def __init__(self, test_passed, failure_description=""):
        if test_passed:
            self.passed_verification = True
            self.failed_verification = False
        else:
            self.passed_verification = False
            self.failed_verification = True
        self.failure_description = failure_description

    def __repr__(self):
        ar = Repr()
        ar.maxstring = 10
        return (f"{__class__.__name__}(test_passed={self.passed_verification}, "
                f"failure_description={ar.repr(self.failure_description)})")


class BaseVerifier:
    is_verifier = True

    def verify_machine_state(self, bfi):
        raise Exception("Not Implemented")


class MaxStepsVerifier(BaseVerifier):
    def __init__(self, max_steps):
        self.max_steps = max_steps

    def verify_machine_state(self, bfi):
        ret_msg = f"BFI took too many steps: {bfi.steps_taken} vs {self.max_steps}"
        return VerificationResult(bfi.steps_taken <= self.max_steps, ret_msg)


class SequenceVerifier(BaseVerifier):
    # Zero is a poor choice for filling up output stream, however these tools are for
    # those who have some general understanding of what is going on, so not very foolproof.
    def verify_machine_state(self, bfi):
        def no(x):
            return len(x) == 0
        def mmsg(pos, expected, actual):
            return f"@{pos}: {expected=}, {actual=}"
        bfi_seq = getattr(bfi, self.bfi_attribute)
        aligned_seqs = (zip_longest(self.seq, bfi_seq, fillvalue=0))
        mismatches = [mmsg(pos, exptd, actl) for pos, (exptd, actl) in enumerate(aligned_seqs)
                      if self.must_compare(exptd) and actl != exptd]
        ret_msg = self.err_msg_prefix + "\n".join(mismatches) if mismatches else ""
        return VerificationResult(no(mismatches), ret_msg)

    def must_compare(self, sym):
        return True


class MemoryVerifier(SequenceVerifier):
    err_msg_prefix = "\n Memory verification error.\n"
    bfi_attribute = "memory"
    def __init__(self, mem_list, cell_size=8, mem_size=2**15):
        def cell_value(el):
            if el.isdigit():
                return int(el)
            elif el == "M":
                return 2**cell_size - 1
            elif el == "X":
                return "X"
        self.seq = []
        self.mem_list = mem_list  # Just in case.
        for el in mem_list:
            if el.isdigit() or el == "M" or el == "X":
                self.seq.append(cell_value(el))
            elif el[1:4] == "...":  # must be the last one.
                # no need to repeat indefinitely.
                self.seq = chain(self.seq, repeat(cell_value(el[0]), mem_size - len(self.seq)))
                break  # a dirty hack!

    def must_compare(self, sym):
        """X is used to denote any memory value and to effectively skip verification"""
        return sym != "X"


class StdoutVerifier(SequenceVerifier):
    err_msg_prefix = "\n Stdout verification error.\n"
    bfi_attribute = "stdout"
    def __init__(self, stdout):
        self.seq = []
        if stdout[0] == "just-capture":
            print("== Just capturing stdout! No verification here! ===")
            self.verify_machine_state = self.just_capture_verify_machine_state
        else:
            self.verify_machine_state = self.full_verify_machine_state
            for el in stdout:
                if el[0] == "\"":
                    el = el.rstrip("\"").lstrip("\"")
                    # For CBFI:
                    self.seq += [x for x in el]
                    #self.seq += [x for x in el]
                    # This is a string
                    pass
                else:  # This is a direct number
                    self.seq.append(int(el))

    def just_capture_verify_machine_state(self, bfi):
        print("Captured stdout:", "".join([chr(x) if isinstance(x, int) else x for x in bfi.stdout]))
        return VerificationResult(True, "")

    def full_verify_machine_state(self, bfi):
        res = super().verify_machine_state(bfi)
        if os.getenv("BFI_PRETTIFY_STDOUT") == "1":
            print("Expected stdout:", "".join([str(x) for x in self.seq]))
            print("Captured stdout:", "".join([chr(x) if isinstance(x, int) else x for x in bfi.stdout]))
            print(res)
        return res


class BFTest:
    builders = {
        "code": lambda code: code[0],
        "steps<": lambda max_steps: MaxStepsVerifier(int(max_steps[0])),
        "out": lambda stdout: StdoutVerifier(stdout),
        "in": lambda stdin: [int(x)  if x.isdigit() else ord(x.strip('"')) for x in stdin],  # WARNING! TEMPORARY WORKAROUND!
        "mem": lambda mem: MemoryVerifier(mem),
    }

    def __init__(self, test_list, bficlass=None):
        if not isinstance(test_list[0], str):
            raise ValueError(f"Expected test name string, got {test_list[0]}")
        self.bficlass = BFI if bficlass is None else bficlass
        self.name = test_list[0]
        self.verifiers = []
        for el in test_list[1:]:
            name, value = el[0], el[1:]
            if name in self.builders:
                stuff = (self.builders[name](value))
                if getattr(stuff, "is_verifier", False):
                    self.verifiers.append(stuff)
                else:
                    setattr(self, name, stuff)

    def run(self):
        #bfi = self.bficlass(mempwr=8, stdin=getattr(self, "in", ""))  # new_bfi
        bfi = self.bficlass(stdin=getattr(self, "in", []))  # new_bfi
        bfi.process_code(self.code)
        self.steps_taken = bfi.steps_taken
        return self.verify(bfi)

    def verify(self, bfi):
        result = [v.verify_machine_state(bfi) for v in self.verifiers]
        if all(r.passed_verification for r in result):
            return True, []
        if os.getenv("BFI_PRETTIFY_STDOUT") == "1":
            return False, []
        return False, [r.failure_description for r in result if r.failed_verification]




def extract_comp_test_definition(path):
    with open(path, "r") as f:
        data = f.readlines()
    test_definition = []
    for line in data:
        if line.startswith("#>"):
            test_definition.append(line[2:])
    return "\n".join(test_definition)



def dtest():
    import doctest
    f, t = doctest.testmod()
    print(f"All done. {f} tests out of {t} failed")


def car(l):
    return l[0]


def cdr(l):
    return l[1:]


# o = sreader(read_tests())
FBFI = namedtuple("FakeBFI", "memory")


def alltests(verbose=False):
    o = sreader(read_tests())
    failure_count = 0
    for oo in o:
        t = BFTest(oo)
        r, d = t.run()
        if not r:
            failure_count += 1
        if verbose:
            print(t.name, r, d)
        else:
            if not r:
                print(t.name, d)
    print(f"All done! Ran {len(o)} tests, {failure_count} tests failed")


def runtests():
    def find_longest_name(tests):
        return max(len(t.name) for t in tests)
    def shrtn(d):
        r = Repr()
        extra = len('FAILED') + len('   ') + len(' ')
        r.maxstring = get_terminal_size()[0] - max_name_width - extra
        # A dirty hack to work with narrow terminals. repr does not cut under three symbols, so
        # I have to do this.
        return r.repr(str(d)) if r.maxstring >= 3 else ""
    def laligned_(tname):
        return f"{t.name:<{max_name_width}}".format(max_name_width)
    # get_terminal_size effectively stores terminal size at it was at startup and
    # does not get updated when e.g. Vim window size changes. It is also worth noting
    # that it sits in shutil.
    o = sreader(read_tests())
    tests = [BFTest(oo) for oo in o]
    max_name_width = find_longest_name(tests)
    failures = []
    for t in tests:
        passed, d = t.run()
        if not passed:
            failures.append((t.name, d))
        print(f"{laligned_(t.name)}   {'OK' if passed else 'FAILED'} {'' if passed else shrtn(d)}")
    if failures:
        print("Failures" + "-"*(20-len("Failures")))
    for i, f in enumerate(failures, start=1):
        print(f"{i})", f[0], '::', "\n".join(f[1]))
    print("-"*20)
    print(f"All done! Ran {len(o)} tests, {len(failures)} tests failed")


if __name__ == "__main__":
    pass
    # runtests()
