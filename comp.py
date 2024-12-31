#!/bin/env python3
"""This is a PoC, not a real compiler at this point.

The concept of piggy-backing on existing infrastructure is thoroughly
investigated. Some experiments are done to see how to test things better.
The code is mostly crude hacks to test the general idea and is absolutely
not how anything production-oriented should look. Various styles are
tried out throughout the code which is covered in remains of unsuccessful
attempts.
Beyond this line proceed on your own risk.

A temporary variable will be allocated with name TMP:/functionname/:/idx/ or
TMP:/functionname/:/name/ /name/ could be used to distinguish between
different auxiliary variables.
Entering a function will result in an allocation of temporaries.
Exiting a function will result in deallocation of all temporaries allocated
with a function A function call returns a tuple of code to execute the
function and a temporary variable that is allocated
"""
import ast
import inspect
import os
import random
import re
import sys

from collections import namedtuple
from functools import wraps
from types import FunctionType

from utils import TimeIt



# manage_temporary_vasrs?
def uses_temporary_vars(vars_to_inject):
    vars_to_inject = [v.strip() for v in vars_to_inject.split(",")]
    if "retval" in vars_to_inject and vars_to_inject.index("retval") != 0:
        raise ValueError("When present retval must be the first!")
    def wrapper(f):
        old_code_obj = f.__code__
        # SMART ALLOCATOR WON"T WORK! YOU ARE MESSING WITH THE CODE HERE!
        preamble = [f"    {vn} = _allocate_temp('{f.__name__}::{vn}')" for vn in vars_to_inject] + [
             "    locvars = " + ", ".join(vars_to_inject) + ",",
             "    out += _clear(*locvars).code"
        ]
        cleanup_range = "[1:]" if "retval" in vars_to_inject else ""
        cleanup_code = [
              f"    out += _clear(*locvars{cleanup_range}).code",
              f"    _deallocate_temp(*locvars{cleanup_range})"
        ]
        f_code = inspect.getsource(f).splitlines()[1:]
        new_code = f_code[:2] + preamble + f_code[2:-1] + cleanup_code + [f_code[-1]]
        # This code is problematic for a number of reasons:
        #  1. it is very fragile, it will fail when `out =""` is not on the first line (e.g. when there is a docstring)
        #  2. it does not properly propagate default values after creating a new function object
        #  3. it does not work with sources properly and gets confused when there is more than one physical line
        #     of arguments.
        new_code_parsed = ast.parse("\n".join(new_code))
        new_code_compiled = compile(new_code_parsed, old_code_obj.co_filename, "exec")
        #codeconst = next(c for c in new_code_compiled.co_consts if type(c) == type(f.__code__))
        #f = FunctionType(codeconst, f.__globals__)
        f = FunctionType(new_code_compiled.co_consts[0], f.__globals__)
        @wraps(f)
        def inner(*a, **k):
            res = f(*a, **k)
            return res
        return inner
    return wrapper


# To tidily wrap up return value
_IRV = namedtuple("InternalReturnValue", "code retval")


# -- Decorators ------------------------------------------------------

# I'll overindulge in using global namespace to store procedures counter.
proc_ctr = 0
# Global, ever-growing (never shrinking) list of tuples like this:
# (proc_ctr, "funcname /arg1 ...", ((0, X), (1, Y), (2, OR:tmp1::10), ...))
# And also global memory snapshot at the time of a call!
trace = []


def memrepr():
    return [(addr, str(mel)) for addr, mel in enumerate(mmry) if mel is not None]


def pprint_ent(x):
    if isinstance(x, int):
        return str(x)
    if isinstance(x, str):
        return x
    if isinstance(x, tuple):
        return pprint_ent(x[1])
    if x is None:
        return "None"
    if callable(x):
        return x.__name__
    if isinstance(x, Array):
        return x.allocname()
    return x.allocname() + f"@{x.addr}"


def annotate_proc_expansion(f):
    @wraps(f)
    def wrapper(*a, **k):
        # Let's short-cut for now to speed things up. The code works fine, but
        # significantly slows down compilation. No point in slowing down something
        # that is already slow.
        return f(*a, **k)
        # Let these be s-exp-like entities, I'll make a proper generator later.
        def build_mmap():
            c = [f"({aa} {bb})" for aa, bb in memrepr()]
            return f"({' '.join(c)})"
        def reconstruct_proc_call():
            return f"({f.__name__} {' '.join(pprint_ent(arg) for arg in a)})"
        global proc_ctr
        global trace
        proc_ctr += 1  # This stuff somehow manages to get duplicated.
        foo = proc_ctr
        res = f(*a, **k)
        if res is None:
            raise Exception(f"You forgot to add a return value to {f.__name__}")
        code, var = res
        code = "{" + f"{foo:09}" + code  + "}"
        toapp = f"({foo} {reconstruct_proc_call()} {build_mmap()})"
        trace.append(toapp)
        return _IRV(code, var)
    return wrapper


# -- End decorators --------------------------------------


class NamedCell:
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr

    def __repr__(self):
        return f"<{__class__.__name__}(\"{self.name}\", {self.addr})>"

    def allocname(self):
        return self.name

    def __str__(self):
        return self.allocname()


class NamedTempCell:
    def __init__(self, name, size, addr, allocctr):
        self.name = name
        self.size = size
        self.addr = addr
        self.allocctr = allocctr
    def allocname(self):
        return self.name + "::" + str(self.allocctr)

    def __str__(self):
        return self.allocname()


# Do I need temporary arrays?
class Array:
    def __init__(self, name, num_el, addr, represented_type = None):
        self.name = name
        self.num_el = num_el
        self.first_addr = addr
        self.represented_type = represented_type

    # Some fool-proofing.
    @property
    def addr(self):
        raise Exception("Attempted to access array as a variable")

    def allocname(self):
        return self.name + f"(Array of {self.num_el} at {self.first_addr})"

    def __str__(self):
        return self.allocname()


# -- Internal functions, constants and global variables ---------

allocctr = 0  # Linear counter for allocations
mmry = [None] * 2**12 # ????
#
BYTE = object()
FXP = INT = object()  # FiXedPoint and INTeger are the same under the hood.
                      # No type-checking atm.

INTARRAYLEN = 10
INTRIGHTINDEX = INTARRAYLEN - 1
INTDIGITSNUM = INTARRAYLEN - 1
INTMAX = 10**(INTARRAYLEN - 1) - 1
INTMIN = -(10**(INTARRAYLEN - 1) - 1)


def extract_caller_name(frame):
    return frame.function


move_me_into_a_better_scope = {}
def extract_allocations(frame):
    if frame.function in move_me_into_a_better_scope:
        return move_me_into_a_better_scope[frame.function]
    code = frame.code_context[0].rstrip()
    allocs = [x.lstrip().rstrip() for x in code.split("=")[0].split(",")]
    move_me_into_a_better_scope[frame.function] = allocs
    return allocs


def get_caller_frame():
    # This takes 75% of the time. It calls sys._getframe() under the hood,
    # let's see if I could do better by calling it directly and wrapping it
    # up
    # Now sys._getframe() is very efficient low-level function which deals mostly
    # with trversing some ptrs.
    # See L1714 in sysmodule.c
    return inspect.stack()[2]
    #return sys._getframe(2)


def _allocate_temps2_od():
    frame = get_caller_frame()
    funcname = extract_caller_name(frame)
    _vars = extract_allocations(frame)
    ret = [_allocate_temp(funcname + "::" + var) for var in _vars]
    return ret[0] if len(ret) == 1 else ret


class SmartAllocator:

    def __init__(self):
        self.cache = {}

    def __call__(self):
        frame = sys._getframe(1)  # Keep good track of these!
        funcname = frame.f_code.co_name
        fname = frame.f_code.co_filename
        cache_entry = funcname + "::" + fname
        if cache_entry in self.cache:
            _vars = self.cache[cache_entry]
        else:
            lineno = frame.f_lineno
            with open(fname, "r") as f:
                lines = f.readlines()
            line = lines[lineno - 1]  # Line numbers start with 1!
            # TODO: add better handling of possible () here
            _vars = [x.lstrip().rstrip() for x in line.split("=")[0].split(",")]
            self.cache[cache_entry] = _vars
        ret = [_allocate_temp(funcname + "::" + var) for var in _vars]
        return ret[0] if len(ret) == 1 else ret


_allocate_temps2 = SmartAllocator()


def is_an_integer(x):
    return isinstance(x, Array) and x.represented_type is INT


def is_a_direct_constant(x):
    return isinstance(x, int)


def is_a_result_of_expression_evaluation(x):
     # This is needed for SET(X, EQ(Y, 1))
    return isinstance(x, tuple)


def is_a_temporarily_allocated_cell(x):
    return isinstance(x, NamedTempCell)


def is_a_global_variable(x):
    return isinstance(x, NamedCell)


# Second must become first to remain second (due to allocation order)
# This is important: doing otherwise _sometimes_ results in fun bugs in
# innocuously looking code.
def prepend_code_if_expression_evaluation_result(code, *_vars):
    retvars = []
    for var in _vars[::-1]:
        if is_a_result_of_expression_evaluation(var):  # i.e. a temp cell
             get_there_code, var = var
             var.needs_dealloc_now = True
             retvars.append(var)
             code = get_there_code + code
        else:
             retvars.append(var)
    return code, *retvars[::-1]


def _clean_and_deallocate_temps_if_needed_and_still_present(*_vars):
    is_eligbl = lambda v: getattr(v, "needs_dealloc_now", False) and v.allocname() in mmry
    # Sometimes it is possible to get same variable twice, e.g. in AND.
    # In that case it is enough to deallocate it just once.
    # AND(NOT(X), ...) will expand into
    # NOT(OR(NOT(OR( NOT(X).retval, NOT(X).retval), ...)
    # and will try to garbage collect on each pass
    _eligible_vars = set(v for v in _vars if is_eligbl(v))
    out = ""
    for var in _eligible_vars:
         out += _clear(var).code
         _deallocate_temp(var)
    return _IRV(out, None)


def to_addr(x):
    # TODO: should be NamedCell.__rmul__
    if isinstance(x, NamedCell) or isinstance(x, NamedTempCell):
        return x.addr
    return x


def _allocate_temp(name, size=1):
    global allocctr
    global mmry
    mempos = mmry.index(None)  # Will fail with ValueError if mmry is full
    out = NamedTempCell(name, size, mempos, allocctr)
    mmry[mempos] = out.allocname()
    allocctr += 1
    return out


# DO NOT REMOVE! This speeds IF up significantly.
def _allocate_temps(prefix, _vars):
    return [_allocate_temp(prefix + "::" + v) for v in _vars.split(", ")]


def _deallocate_temp(*cells):
    # This simple arrangement will work _if_ I don't intertwine
    # allocations and deallocations. Which I will probably do.
    global mmry
    var = cells[0]
    for cell in cells:
        if cell is None:
            continue
        if isinstance(cell, NamedTempCell):
            try:
                mempos = mmry.index(cell.allocname())
                mmry[mempos] = None  # TODO: log max mmry pos
            except ValueError:
                print(cell.allocname(), cell.allocname() in mmry)
                stack = inspect.stack()
                frame1 = stack[1]
                frame2 = stack[2]
                frame3 = stack[4]
                print(frame1.function, frame1.lineno, frame1.code_context[0].rstrip() if frame1.code_context is not None else "")
                print(frame3.function, frame3.lineno, frame3.code_context[0].rstrip() if frame2.code_context is not None else "")
                print(frame2.function, frame2.lineno, frame2.code_context[0].rstrip() if frame2.code_context is not None else "")
                print("oops, you have a deallocation error", cell.allocname())


def inject_global_variable(name):
    global mmry
    idx = mmry.index(None)
    quuxmeep = NamedCell(name, idx)
    globals()[name] = quuxmeep
    # Store variables carefully to be able to trace them back
    mmry[idx] = quuxmeep
    return quuxmeep


def remove_global_variable(var):
    idx = mmry.index(var)
    mmry[idx] =None
    del var.name

#   Inner functions which produce BF code

def _clean_current():
    return _IRV("[-]", None)


def _move_to(addr):
    addr = to_addr(addr)
    return _IRV(">" * addr, None)


def _return_from(addr):
    addr = to_addr(addr)
    return _IRV("<" * addr, None)


def _clear(*a):
    a = [to_addr(x) for x in a]
    out = _move_to(a[0]).code
    out += _clean_current().code
    for prev, nxt in zip(a[:-1], a[1:]):
        out += _move_relative(prev, nxt).code
        out += _clean_current().code
    out += _return_from(a[-1]).code
    return _IRV(out, None)


def _clear_int(x):
    out = _move_to(x.first_addr).code
    for j in range(23):
        out +="[-]>"
    out += "<" * 23
    out += _return_from(x.first_addr).code
    return _IRV(out, None)


def _set_minus(x):
    out = _move_to(x.first_addr + 3).code
    out += "[-]+"
    out += "<<<"
    out += _return_from(x.first_addr).code
    return _IRV(out, None)


def _generate_temp_number(num):
    # This is a very low-level function, thus the name is explicitly hardcoded:
    tmp = _allocate_temp(f"_generate_temp_number::tmp({num})" )
    tmp.can_clear = True
    out = _clear(tmp).code
    out += _move_to(tmp).code
    out += "+" * num
    out += _return_from(tmp).code
    return _IRV(out, tmp)


def _set_to_known_number(addr, num):
    out = _move_to(addr).code
    out += "[-]"
    out += num * "+"
    out += _return_from(addr).code
    return _IRV(out, None)


def _move_relative(addr1, addr2):
    addr1 = to_addr(addr1)
    addr2 = to_addr(addr2)
    if addr1 > addr2:
        return _IRV('<' * (addr1 - addr2), None)
    elif addr2 > addr1:
        return _IRV('>' * (addr2 - addr1), None)
    else:
        return _IRV("", None)


def _destructive_copy(addr1, addr2):
    addr1 = to_addr(addr1)
    addr2 = to_addr(addr2)
    out = ""
    out += _move_to(addr1).code
    out += '[' + '-' + _move_relative(addr1, addr2) .code+ '+' +_move_relative(addr2, addr1) .code+ ']'
    out += _return_from(addr1).code
    return _IRV(out, None)


def _non_destructive_copy(addr1, addr2):
    addr1 = to_addr(addr1)
    addr2 = to_addr(addr2)
    out = ""
    # Low-level function. Hardcoding the name saves time
    tmp = _allocate_temp("_non_destructive_copy::tmp")
    out += _move_to(addr1).code
    out += ('[' + '-' + _move_relative(addr1, tmp).code +
            '+' + _move_relative(tmp, addr2).code +
            '+' +_move_relative(addr2, addr1).code + ']')
    out += _return_from(addr1).code
    out += _destructive_copy(tmp, addr1).code
    _deallocate_temp(tmp)
    return _IRV(out, None)
# -- Internal functions over ------------------------------


# -- User function ----------------------------
# The "language" consist of them.

def BF(code):
    """A wrapper to simplify inclusion of direct BF snippets"""
    return _IRV(code, None)


# Soft agreement: this must appear only in the top-level.
# Not enforced, but will likely result in !!fun!!
def VAR(variables, _type=BYTE):
    """VAR("X, Y, Z", BYTE)"""
    variables = variables.replace(" ", "").split(",")
    if _type is BYTE:
        for var in variables:
            # It is not immediately clear if something has to be done when
            # the variable already exists at this point. I could check if it is of
            # the right type. If it is a NamedCell, then I could overwrite it
            # (i.e. ignore clashes for now), report an error otherwise.
            # Or do not report and just ignore since the code is still raw
            # and experimental.
            inject_global_variable(var)
    elif _type is INT:
        for var in variables:
            ARRAY((var, 10), _type=INT)


def find_proper_position_for(size, mmry):
    offset = 0
    while True:
        # Will raise ValueError when missing after offset.
        idx = mmry.index(None, offset)
        if all(x is None for x in mmry[idx:idx+size]):
            return idx
        offset = idx + [i for i, x in enumerate(mmry[idx:idx+size]) if x is not None][0]


# TODO: arrays of arrays!
def ARRAY(*size_groups, _type=None):
    """ARRAY(("X", 10), ("Y, Z", 5))"""
    global mmry
    foo = len(mmry)
    #if _type is None or _type is BYTE:
    if True:
        for _vars, size in size_groups:
            # Needs x2 space for dynamic ptrs + 3 auxiliary elements.
            size = 3 + size * 2
            _vars = _vars.replace(" ", "").split(",")
            for arrvar in _vars:
                addr = find_proper_position_for(size, mmry)
                quuxmeep = Array(arrvar, size, addr, _type)
                globals()[arrvar] = quuxmeep
                mmry[addr:addr+size] = [quuxmeep] * size
                if len(mmry) != foo:
                    raise Exception("Память раздуло!")


def DEC(var):
    return PROG(
                _move_to(var),
                BF("-"),
                _return_from(var)
               )


def INC(var):
    return PROG(
                _move_to(var),
                BF("+"),
                _return_from(var)
               )


def WHILE(var, subprog):
    """WHILE(X, PROG(DEC(X), PRINT("!")))"""
    return PROG(
                _move_to(var),
                BF("["),
                _return_from(var),
                subprog,
                _move_to(var),
                BF("]"),
                _return_from(var),
            )


def PRINT(val):
    out = ""
    if isinstance(val, str):
        val = list(val)
        for ch in val:
            code, tmp = _generate_temp_number(ord(ch))
            out += code
            out += _move_to(tmp.addr).code
            out += "."
            out += _clean_current().code
            out += _return_from(tmp.addr).code
            _deallocate_temp(tmp)
    elif isinstance(val, NamedCell) or isinstance(val, NamedTempCell):
        tmp1, tmp2, div_res, ones, tens = _locvars = _allocate_temps2()

        out += _clear(*_locvars).code
        out += _non_destructive_copy(val, tmp1).code
        out += DIVMOD(tmp1, 10, div_res, ones).code
        out += SET(tmp2, GT(div_res, 0)).code
        out += IF(tmp2, lambda: PROG(
            SET(tmp1, div_res),
            _clear(div_res),
            DIVMOD(tmp1, 10, div_res, tens)), lambda: NOP()).code
        out += SET(tmp2, div_res).code

        # Hundreds go first (if present).
        out += IF(div_res, lambda: PROG(
            DEC(div_res), IF(div_res,
                lambda: PROG(DEC(div_res),
                             IF(div_res, lambda: PRINT("ERROR"), lambda: PRINT("2"))),
               lambda: PRINT("1")),
            ), lambda: NOP()).code

        # Then tens:
        out += IF(tens,
           lambda: PROG(
            DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("1")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("2")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("3")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("4")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("5")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("6")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("7")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("8")), DEC(tens),
            IF(tens, lambda: NOP(), lambda: PRINT("9"))),
           # Emit 0 only if val > 100.
           lambda: IF(tmp2, lambda: PRINT("0"), lambda: NOP())).code

        # And, finally, the last digit:
        out += IF(ones,
           lambda: PROG(
            IF(ones, lambda: NOP(), lambda: PRINT("0")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("1")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("2")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("3")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("4")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("5")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("6")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("7")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("8")), DEC(ones),
            IF(ones, lambda: NOP(), lambda: PRINT("9"))),
           lambda: PRINT("0")).code

        # This trick works well when retval is not allocated.
        # (actually it works well even when there is a retval, just place it first and
        # clear _locvars[1:]).
        out += _clear(*_locvars).code
        _deallocate_temp(*_locvars)
    else:
        raise NotImplementedError(f"Unknown type for division: {type(val)}")
    return _IRV(out, None)


def _print_digit(val):
    if isinstance(val, NamedCell) or isinstance(val, NamedTempCell):
        tmp = _locvars = _allocate_temps2()
        out = _clear(tmp).code
        out += _non_destructive_copy(val, tmp).code
        out += PROG(
            IF(tmp, lambda: NOP(), lambda: PRINT("0")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("1")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("2")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("3")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("4")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("5")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("6")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("7")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("8")), DEC(tmp),
            IF(tmp, lambda: NOP(), lambda: PRINT("9"))).code
        out += _clear(tmp).code
        _deallocate_temp(tmp)
    else:
        raise NotImplementedError(f"Unknown type for printing: {type(val)}")

    return _IRV(out, None)


def _print_temp_digit(val):
    if isinstance(val, tuple):
        out, res = val
        out += PROG(
            IF(res, lambda: NOP(), lambda: PRINT("0")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("1")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("2")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("3")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("4")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("5")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("6")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("7")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("8")), DEC(res),
            IF(res, lambda: NOP(), lambda: PRINT("9"))).code
        out += _clear(res).code
        _deallocate_temp(res)
    else:
        raise NotImplementedError(f"Unknown type for printing: {type(val)}")

    return _IRV(out, None)


def _print_array_digit(arr, idx):
    location_addr = arr.first_addr + idx * 2 + 3
    out = _move_to(location_addr).code
    # This modifies the array in place a little, but quickly returns everything to its
    # proper state.
    out += "++++++++++++++++++++++++++++++++++++++++++++++++"
    out += "."
    out += "------------------------------------------------"
    out += _return_from(location_addr).code
    return _IRV(out, None)


# Rework for always a variable in COND. This will be a little harder, but will
# allow to resolve uncertainty between COND: X which allocates nothing, but uses
# X contents for making decisions and COND: EQ(X, 6), which allocates a temporary and
# makes a decision basing on it.
# For now I'll express this like:
#  SET(SELECTION_CONDITION1, EQ(X, P))
#  IF(SELECTION_CONDITION1,
#     THEN: PROG(...),
#     ELSE: PROG(...))
#@annotate_proc_expansion
@uses_temporary_vars("tmp0, tmp1")
def IF(var, then_thunk, else_thunk):
    out = ""
    out += _move_to(var).code
    out += "["
    out += _move_relative(var, tmp0).code
    out += "+"
    out += _move_relative(tmp0, tmp1).code
    out += "+"
    out += _move_relative(tmp1, var).code
    out += "-"
    out += "]"
    out += _return_from(var).code
    out += _move_to(tmp0).code
    out += "["
    out += _move_relative(tmp0, var).code
    out += "+"
    out += _move_relative(var, tmp0).code
    out += "-"
    out += "]"
    out += "+"
    out += _return_from(tmp0).code
    out += _move_to(tmp1).code
    out += "["
    out += _return_from(tmp1).code
    then_code, then_ret = then_thunk()
    out += then_code
    out += "  "
    out += _move_to(tmp0).code
    out += "-"
    out += _return_from(tmp0).code
    out += _move_to(tmp1).code
    out += _clean_current().code
    out += "]"
    out += _return_from(tmp1).code
    out += _move_to(tmp0).code
    out += "["
    out += _return_from(tmp0).code
    else_code, else_ret = else_thunk()
    out += else_code
    out += "  "
    out += _move_to(tmp0).code
    out += "-"
    out += "]"
    out += _return_from(tmp0).code

    _deallocate_temp(then_ret, else_ret)
    return _IRV(out, None)


def PROG(*bits):
    out = ""
    retv = None
    for codebit, retv in bits:
        out += codebit
        out +="\n"
    return _IRV(out, retv)


def SET(var, val, no_dealloc=False):
    """SET(var, val): sets variable to value

    SET(X, 1) -- directly sets cell referred to as X to 1;
    SET(X, Y) -- directly sets cell referred to as X to value in Y;
    SET(X, ADD(X, 1)) -- sets X to the result of computing an expression.
    """
    out = ""
    if is_a_direct_constant(val):
        out += _move_to(var).code
        out += "[-]" + "+" * val
        out += _return_from(var).code
    elif is_a_temporarily_allocated_cell(val):  # Could be a temp cell living in a loop
        out += _clear(var).code
        if getattr(val, "can_clear", False):
            out += _destructive_copy(val, var).code
            _deallocate_temp(val)
        else:
            out += _non_destructive_copy(val, var).code
    elif is_a_result_of_expression_evaluation(val):
        get_there_code, val = val
        out = get_there_code + out
        out += _clear(var).code
        out += _destructive_copy(val, var).code
        _deallocate_temp(val)
    elif is_a_global_variable(val):
        out += _clear(var).code
        out += _non_destructive_copy(val, var).code
    return _IRV(out, None)  # consider returning retv


@annotate_proc_expansion
def AND(var1, var2):
    # TODO: replace with proper implementation (a faster one like in OR)
    return NOT(OR(NOT(OR(var1, var1)), NOT(OR(var2, var2))))


@uses_temporary_vars("retval, tmp1, tmp2")
def OR(var1, var2):
    out = ""
    retval.can_clear = True

    if is_a_direct_constant(var2):
        out += SET(tmp2, 1 if var2 != 0 else 0).code
        var2 = tmp2
    if is_a_direct_constant(var1):
        out += SET(tmp1, 1 if var1 != 0 else 0).code
        var1 = tmp1

    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)

    out += IF(var1, lambda: SET(retval, 1),
                    lambda: IF(var2,
                            lambda: SET(retval, 1),
                            lambda: SET(retval, 0)),
                    ).code
    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, retval)


@annotate_proc_expansion
def NOT(var):  # I bet this could be simplified.
    out = ""
    retval = _allocate_temps2()
    retval.can_clear = True
    if is_a_direct_constant(var):
        if var:
            out, _ = SET(retval, 0)
        else:
            out, _ = SET(retval, 1)
    elif is_a_result_of_expression_evaluation(var):
        get_there_code, var = var
        out = get_there_code + out
        code, _ = IF(var, lambda: SET(retval, 0),
                          lambda: SET(retval, 1))
        out += code
        out += _clear(var).code
        # It will create funny loops otherwise
        _deallocate_temp(var) if getattr(var, "can_clear", False) else ...
    elif is_a_global_variable(var) or is_a_temporarily_allocated_cell(var):
        out, _ = IF(var, lambda: SET(retval, 0),
                          lambda: SET(retval, 1))
    return _IRV(out, retval)


@annotate_proc_expansion
def NOP(*a, **k):
    return _IRV("", None)


# SET call deals with any(!) combo of constants and variables.
# And does this in a costly manner.
@uses_temporary_vars("retval, tmp1, tmp2")
def EQ(var1, var2):
    out = ""
    retval.can_clear = True
    # This is necessary even given that SET is the first procedure.
    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)
    # TODO: this is an overkill if var1 or var2 is a temp -- it will be copied over.
    out += PROG(
                SET(tmp2, var2),
                SET(tmp1, var1),
                WHILE(tmp1, PROG(DEC(tmp1), DEC(tmp2))),
                IF(tmp2, lambda: NOP(), # retval already clear#SET(retval, 0),
                         lambda: INC(retval), #SET(retval, 1),
                  ),
                _clear(tmp1, tmp2)
            ).code
    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, retval)


# var1 > var2
@uses_temporary_vars("retval, tvar1, tvar2, tmp1, tmp2")
def GT(var1, var2):
    out, mr = "", lambda *a: _move_relative(*a).code
    retval.can_clear = True

    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)
    out += SET(tvar1, var1).code
    out += SET(tvar2, var2).code

    out += _move_to(tvar1).code + "["  + mr(tvar1, tmp1)  + "+"
    out += mr(tmp1, tvar2)      + "[-" + mr(tvar2, tmp1)  + "[-]"
    out += mr(tmp1, tmp2)       + "+"  + mr(tmp2, tvar2)  + "]"
    out += mr(tvar2, tmp1)      + "[-" + mr(tmp1, retval) + "+"   + mr(retval, tmp1) + "]"
    out += mr(tmp1, tmp2)       + "[-" + mr(tmp2, tvar2)  + "+"   + mr(tvar2, tmp2)  + "]"
    out += mr(tmp2, tvar2)      + "-"  + mr(tvar2, tvar1) + "-]"
    out += _return_from(tvar1).code

    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, retval)


# retval = var1 + var2
@uses_temporary_vars("retval, tmp1, tmp2")
def ADD(var1, var2):
    out = ""
    retval.can_clear = True
    # TODO: this is a great candidate to go into a smart decorator
    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)
    out += PROG(
                SET(tmp1, var1),
                SET(tmp2, var2),
                WHILE(tmp2, PROG(INC(retval), DEC(tmp2))),
                WHILE(tmp1, PROG(INC(retval), DEC(tmp1))),
                _clear(tmp1, tmp2)).code
    # TODO: and this as well.
    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, retval)


# retval = var2 - var1
#@uses_temporary_vars("retval, tmp1, tmp2")  -- this messes up with pre-set arguments
def SUB(var1, var2, no_dealloc=False):  # var2 - var1
    out = ""
    retval, tmp1, tmp2 = _allocate_temps2()
    retval.can_clear = True

    out = _clear(tmp1, tmp2, retval).code

    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)

    out += PROG(
                SET(tmp1, var1),
                SET(tmp2, var2),
                WHILE(tmp2, PROG(INC(retval), DEC(tmp2))),
                WHILE(tmp1, PROG(DEC(retval), DEC(tmp1))),
                _clear(tmp2, tmp1)).code

    _deallocate_temp(tmp1, tmp2)
    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, retval)


@annotate_proc_expansion
def _sub1(var1, no_dealloc=False):  # var2 - var1
    """retval = var1 - 1"""

    retval = _allocate_temps2()
    retval.can_clear = True

    out = _clear(retval).code

    out, var1 = prepend_code_if_expression_evaluation_result(out, var1)

    out += PROG(
                SET(retval, var1),
                DEC(retval),
                ).code

    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1).code
    return _IRV(out, retval)


# No retval! div_res and mod_res are modified to store the results.
@uses_temporary_vars("tmp1, tmp2, tmp3, VAR2, run")
def DIVMOD(var1, var2, div_res, mod_res):
    out = ""

    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)

    out += PROG(
                SET(div_res, 0),
                SET(mod_res, var1),
                SET(VAR2, var2),
                SET(tmp3, OR(EQ(mod_res, VAR2), GT(mod_res, VAR2))),
                SET(run, 1),
                IF(tmp3,
                   lambda:  # main code here
                      WHILE(run, PROG(
                                      INC(div_res),
                                      SET(mod_res, SUB(VAR2, mod_res)),
                                      SET(run, OR(EQ(mod_res, VAR2),
                                                  GT(mod_res, VAR2))),
                                     )),
                   lambda: NOP())).code

    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, None)  # NO RETVAL BECAUSE OF A SIDE EFFECT!


def SUBPROG(name, subprog_thunk):
    """SUBPROG("FOO", BODY: PROG(...))
    FOO()
    """
    # TODO: deal  with SUBPROG("FOO", BODY(X, Y, Z): PROG(...))
    globals()[name] = subprog_thunk


def LOADLIB(libname):
    """A library is a collection of SUBPROGs.

    And also of VAR definitions, however those create problems when
    used with (mem ...) since the ordering is not really known.
    Also note that proper path handling must be added.
    """
    with open(libname, "r") as f:
        data = f.read()
    data = unmask_lambdas(data)
    result = exec(data)


@annotate_proc_expansion
def ARRSET(arrvar, idx, val):
    if isinstance(arrvar, Array):
        # DO NOT do boundary checks here, it will be fried in runtime anyway.
        out = ""
        if is_a_direct_constant(idx):
            location_addr = arrvar.first_addr + idx * 2 + 3
            out += SET(location_addr, val).code
        elif is_a_global_variable(idx):
            if is_a_direct_constant(val):
                code, val = _generate_temp_number(val)
                val.needs_dealloc_now = True
                out += code
            mr = lambda *a: _move_relative(*a).code
            x = arrvar.first_addr  # x, temp0 and temp1 are preallocated per array
            temp0 = x + 1
            temp1 = x + 2
            temp2 = _allocate_temps2()
            out += _clear(x, temp0, temp1, temp2).code

            out += _move_to(idx).code
            out += "[" + mr(idx, temp1) + "+" + mr(temp1, temp2) + "+"
            out += mr(temp2, idx) + "-]"
            out += mr(idx, temp2) + "[" + mr(temp2, idx) + "+" + mr(idx, temp2) + "-]"
            out += mr(temp2, val)
            out += "[" + mr(val, temp0) + "+" + mr(temp0, temp2) + "+"
            out += mr(temp2, val) + "-]"
            out += mr(val, temp2) + "[" + mr(temp2, val) + "+" + mr(val, temp2) + "-]"
            out += mr(temp2, arrvar.first_addr)
            # We are in the beginning of an array
            # A: Move to temp1, then search for the first ptr cell with a zero, increment it,
            # return back to the beginning stepping over two cells at a time (they contain 0s),
            # then go to temp1 and decrement it by 1. Go to A: and repeat until temp1 > 0.
            # When temp1 is 0 increment it by 1.
            out += ">>[[>>]+[<<]>>-]+"
            # We are at temp1.
            # We find first ptr equal to 0, and zero out a cell to the left of it,
            # then move to ptr cell to the laft and find left boundary.
            out += "[>>]<[-]<[<<]"
            # We are on the left border.
            # Move to temp0 (contains value copy)
            # then in a loop we find the target cell and copy temp0 over to it.
            # temp0 equlas 0 now.
            out += ">[>[>>]<+<[<<]>-]"
            out += ">[>>]<<[-<<]"

            out += _return_from(x).code

            out += _clear(temp0, temp1, temp2).code
            _deallocate_temp(temp2)
            out += _clean_and_deallocate_temps_if_needed_and_still_present(val).code
        else:
            raise Exception(f"Cannot set to indirect index!")
        return _IRV(out, None)
    raise Exception(f"Cannot ARRSET {type(arrvar)}")


@annotate_proc_expansion
def ARRGET(arrvar, idx):
    if isinstance(arrvar, Array):
        out = ""
        retval = _allocate_temps2()
        retval.can_clear = True
        out += _clear(retval).code
        if is_a_direct_constant(idx):
            location_addr = arrvar.first_addr + idx * 2 + 3
            # Let's pretend that a memory cell is an actual variable.
            # This will simplify SET a little.
            out += SET(retval, NamedCell("Ephemeral", location_addr)).code
        elif is_a_global_variable(idx):
            mr = lambda *a: _move_relative(*a).code
            y = arrvar.first_addr  # x, temp0 and temp1 are preallocated per array
            temp0 = y + 1
            temp1 = y + 2
            temp2 = _allocate_temps2()
            out += _clear(y, temp0, temp1, temp2).code

            out += _move_to(idx).code + "["
            out += mr(idx, temp1) + "+" + mr(temp1, temp0) + "+" + mr(temp0, idx) + "-]"
            out += mr(idx, temp0) + "[" + mr(temp0, idx) + "+" + mr(idx, temp0) + "-]"
            out += mr(temp0, y)
            out += ">>[[>>]+[<<]>>-]+[>>]<[<[<<]>+<"
            out += mr(y, retval) + "+" + mr(retval, y)
            out += ">>[>>]<-]<[<<]>[>[>>]<+<[<<]>-]>[>>]<<[-<<]"

            out += _return_from(y).code

            out += _clear(temp0, temp1, temp2).code
            _deallocate_temp(temp2)
        else:
            raise Exception(f"Cannot set to indirect index!")
        return _IRV(out, retval)
    raise Exception(f"Cannot ARRSET {type(arrvar)}")


#@expected_types(var in (INT,), val in (transient, const in range(-..., ...), BYTE, INT))
@annotate_proc_expansion
def INTSET(var, val):
    """ var <- val"""
    out = ""
    out += _clear_int(var).code
    if is_a_direct_constant(val):
        def num_to_list(x):
            out = []
            while x:
                x, r = divmod(x, 10)
                out.append(r)
            return out
        val, must_set_minus = (-val, True) if val < 0 else (val, False)
        nl = zip(range(9, -1, -1), num_to_list(val))
        for offset, num in nl:
            out += _set_to_known_number(var.first_addr + 3 + offset*2, num).code
        out += _set_minus(var).code if must_set_minus else NOP().code
    elif (is_a_global_variable(val) or is_a_result_of_expression_evaluation(val) or
            is_a_temporarily_allocated_cell(val)):
        tmp1, tmp2, div_res, ones, tens = _locvars = _allocate_temps2()

        out += _clear(*_locvars).code
        out, val = prepend_code_if_expression_evaluation_result(out, val)
        out += _non_destructive_copy(val, tmp1).code
        out += DIVMOD(tmp1, 10, div_res, ones).code
        out += SET(tmp2, GT(div_res, 0)).code
        out += IF(tmp2, lambda: PROG(
            SET(tmp1, div_res),
            _clear(div_res),
            DIVMOD(tmp1, 10, div_res, tens)), lambda: NOP()).code
        out += SET(tmp2, div_res).code

        # TODO: use destructive copy here.
        out += IF(ones, lambda: SET(var.first_addr + 3 + 18, ones), lambda: NOP()).code
        out += IF(tens, lambda: SET(var.first_addr + 3 + 16, tens), lambda: NOP()).code
        out += IF(div_res, lambda: SET(var.first_addr + 3 + 14, div_res),
                          lambda: NOP()).code
        out += _clear(*_locvars).code
        _deallocate_temp(*_locvars)
        out += _clean_and_deallocate_temps_if_needed_and_still_present(val).code
    elif is_an_integer(val):
        for offset in range(0, 10):

            destination = var.first_addr + 3 + offset*2
            source = val.first_addr + 3 + offset*2
            out += _non_destructive_copy(source, destination).code
    return _IRV(out, None)


# TODO: INTNEGATE
@annotate_proc_expansion
def INTNEG(var1, var2):
    """ var2 <- -var1"""
    out = ""
    out += _clear_int(var2).code
    out += INTSET(var2, var1).code
    tmp = _allocate_temps2()
    # TODO: add .sign_cell() method to Array
    out += SET(tmp, NamedCell("SignVitualVar", var1.first_addr + 3)).code
    out += SET(NamedCell("ArrayElement", var2.first_addr + 3), NOT(tmp)).code
    out += _clear(tmp).code
    _deallocate_temp(tmp)
    return _IRV(out, None)


@annotate_proc_expansion
def INTNEGSELF(var1):
    """ var1 <- -var1"""
    out = ""
    tmp = _allocate_temps2()
    out += SET(tmp, NamedCell("SignVitualVar", var1.first_addr + 3)).code
    out += SET(NamedCell("ArrayElement", var1.first_addr + 3), NOT(tmp)).code
    out += _clear(tmp).code
    _deallocate_temp(tmp)
    return _IRV(out, None)


@annotate_proc_expansion
def INTPOSITIVE(var):
    retval = _allocate_temps2()
    retval.can_clear = True
    out = _clear(retval).code
    out += SET(retval, NOT(NamedCell("ArrayElement", var.first_addr + 3))).code
    return _IRV(out, retval)


@uses_temporary_vars("tmp, prn_0, tmp2")
def INTPRINT(var):
    out = ""
    out += SET(tmp, EQ(NamedCell("ArrayElement", var.first_addr + 3), 0)).code
    out += IF(tmp, lambda: NOP(), lambda: PRINT("-")).code
    for offset in range(5, 23, 2): # Magic number warning. Future me, please refactor!
        out += SET(tmp, NamedCell("ArrayElement", var.first_addr + offset)).code
        out += SET(tmp2, NOT(prn_0)).code
        out += IF(tmp2, lambda: SET(prn_0, GT(tmp, 0)), lambda: NOP()).code
        out += IF(prn_0, lambda: PRINT(tmp), lambda: NOP()).code
    return _IRV(out, None)


def _xor_two_bytes(var1, var2):
    out = ""
    retval = _allocate_temps2()
    retval.can_clear = True
    out += _clear(retval).code
    out, var1, var2 = prepend_code_if_expression_evaluation_result(out, var1, var2)
    out += PROG(
            IF(var1,
                lambda: IF(var2,
                    lambda: NOP(),
                    lambda: INC(retval),),
                lambda: IF(var2,
                    lambda: INC(retval),
                    lambda: NOP(),))
            ).code
    out += _clean_and_deallocate_temps_if_needed_and_still_present(var1, var2).code
    return _IRV(out, retval)


@uses_temporary_vars("retval, current, loop, current_eq")
def _inteq_both_positive(var1, var2):
    out = ""
    retval.can_clear = True
    out += PROG(
                INC(current),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(loop),
                INC(retval),  # This actually broke sine a little!
                # last digit became 6 instead of 5
                WHILE(loop, PROG(
                    # Exit the loop if Y has bigger size than X
                    SET(current_eq,
                        # A very dirty hack with virtual global variable.
                        EQ(ARRGET(var2, _nc(current)),
                           ARRGET(var1, _nc(current)))),
                    IF(current_eq,
                       # THEN can continue
                       lambda: PROG(
                           INC(current),
                           DEC(loop),
                                ),
                       # ELSE: they are not eq, bye
                       lambda: PROG(_clear(loop), _clear(retval),),
                                    )))).code
    return _IRV(out, retval)


@uses_temporary_vars("retval, signs_diff, current, loop, current_eq")
def INTEQ(var1, var2):
    out = ""
    retval.can_clear = True
    out += SET(signs_diff, _xor_two_bytes(NamedCell("ArrayElement", var1.first_addr + 3),
                        NamedCell("ArrayElement", var2.first_addr + 3))).code
    out += IF(signs_diff, lambda: NOP(),  # retval is already clean
            lambda: PROG(
                SET(retval, _inteq_both_positive(var1, var2)),
            )).code
    return _IRV(out, retval)


# This one is actually greater or eq?
# DO NOT TOUCH THIS UNTIL YOU HAVE GREATER OR EQ IMPLEMENTED!
# THIS ONE IS FINE!!!!
@uses_temporary_vars("retval, current, loop, v1dig, v2dig, var2_has_greater_digit, var1_has_greater_digit")
def _int_gt_both_positive(var1, var2):
    out = ""
    retval.can_clear = True
    out += PROG(
                    INC(current), #SET(current, 1),
                    PROG(*[INC(loop) for _ in range(INTDIGITSNUM)]),
                    WHILE(loop, PROG(
                        # Exit the loop if Y is greater than X
                        SET(v1dig, ARRGET(var1, _nc(current))),
                        SET(v2dig, ARRGET(var2, _nc(current))),
                        SET(var2_has_greater_digit, GT(v2dig, v1dig)),
                        SET(var1_has_greater_digit, GT(v1dig, v2dig)),
                        IF(var2_has_greater_digit,
                           #THEN
                           lambda: PROG(_clear(loop), _clear(retval),),
                           #ELSE
                           lambda: PROG(
                                IF(var1_has_greater_digit,
                                    lambda: PROG(_clear(loop), INC(retval),),
                                    lambda: PROG( INC(current),
                                        DEC(loop),
                                        ))))))).code
    return _IRV(out, retval)


_int_gtoreq_both_positive = _int_gt_both_positive


@annotate_proc_expansion
def _int_gtoreq_both_positive_future(var1, var2):
    out = ""
    retval, current, loop, var2_has_greater_digit, var1_has_greater_digit  = locvars = _allocate_temps2()
    out += _clear(*locvars).code
    retval.can_clear = True
    # ... some very smart code here. Must use low-level GE
    out += _clear(*locvars[1:]).code
    _deallocate_temp(*locvars[1:])

    return _IRV(out, retval)


# var1 > var2
# Possible cases:
#   is_negative(var1) is_positive(var2):  False
#   is_positive(var1) is_negative(var2):  True
#   is_negative(var1) is_negative(var2):  INTGT(negate(var1)), negate(var2))
#   else: long symbol-by-symbol comparison.
@uses_temporary_vars("retval, both_pos, both_neg, signs_diff, var1_pos, var1_neg, var2_pos, var2_neg, current, loop, var2_has_greater_digit, var1_has_greater_digit")
def INTGT(var1, var2):
    out = ""
    retval.can_clear = True
    out += SET(var1_pos, INTPOSITIVE(var1)).code
    out += SET(var1_neg, NOT(var1_pos)).code
    out += SET(var2_pos, INTPOSITIVE(var2)).code
    out += SET(var2_neg, NOT(var2_pos)).code
    out += SET(both_pos, AND(var1_pos, var2_pos)).code
    out += SET(both_neg, AND(var1_neg, var2_neg)).code
    out += SET(signs_diff, AND(NOT(both_pos), NOT(both_neg))).code
    out += IF(signs_diff,
        #THEN
        lambda: PROG(
            IF(var1_neg,
                lambda: SET(retval, 0),
                lambda: SET(retval, 1))),
        #ELSE
        lambda: IF(both_neg,
            #THEN
            lambda: PROG(
              # Way cheaper than making a temp copy!
              INTNEGSELF(var1), INTNEGSELF(var2),
              SET(current, 1),
              SET(loop, 1),
              WHILE(loop, PROG(
                  # Must break the loop if at some position there is a greater value in Y
                  SET(var2_has_greater_digit,
                      GT(ARRGET(var1, _nc(current)),
                         ARRGET(var2, _nc(current)))),
                  SET(var1_has_greater_digit,
                      GT(ARRGET(var2, _nc(current)),
                         ARRGET(var1, _nc(current)))),
                  IF(var2_has_greater_digit,
                     #THEN
                     lambda: PROG(SET(loop, 0), SET(retval, 0),),
                     #ELSE
                     lambda: PROG(
                          IF(var1_has_greater_digit,
                              lambda: PROG( SET(loop, 0), SET(retval, 1),),
                              lambda: PROG( INC(current),
                                  SET(loop, NOT(GT(current, INTARRAYLEN))),
              )))))),
              INTNEGSELF(var1), INTNEGSELF(var2),
              ),
            #ELSE: both are positive
            lambda: PROG(
                    SET(current, 1),
                    SET(loop, 1),
                    WHILE(loop, PROG(
                        SET(var2_has_greater_digit,
                            GT(ARRGET(var2, _nc(current)),
                               ARRGET(var1, _nc(current)))),
                        SET(var1_has_greater_digit,
                            GT(ARRGET(var1, _nc(current)),
                               ARRGET(var2, _nc(current)))),
                        IF(var2_has_greater_digit,
                           #THEN
                           lambda: PROG(SET(loop, 0), SET(retval, 0),),
                           #ELSE
                           lambda: PROG(
                                IF(var1_has_greater_digit,
                                    lambda: PROG( SET(loop, 0), SET(retval, 1),),
                                    lambda: PROG( INC(current),
                                        SET(loop, NOT(GT(current, INTARRAYLEN))),
    ))))))))).code
    return _IRV(out, retval)


@annotate_proc_expansion
def READTO(var):
    """Reads a single byte from stdin into var"""
    out = ""
    out += _move_to(var).code
    out += "[-],"
    out += _return_from(var).code
    return _IRV(out, None)


# dest <- int(stdio)
@uses_temporary_vars("loop, tmp, tmp2")
def INTREAD(dest):
    out = ""
    out += PROG(
            SET(loop, 1),
            WHILE(loop, PROG(
                READTO(tmp),
                SET(tmp2, EQ(tmp, 10)),
                IF(tmp2, lambda: _clear(loop),
                    lambda: PROG(
                        _int_shift_left_in_place(dest),
                        ARRSET(dest, INTRIGHTINDEX, SUB(48, tmp)),
                        ))
                )),
            ).code
    return _IRV(out, None)


@uses_temporary_vars("retval, loop, ones, tens, hundreds")
def INTTOBYTE(var):
    out = ""
    out += PROG(
            SET(ones, ARRGET(var, INTRIGHTINDEX)),
            SET(retval, ARRGET(var, INTRIGHTINDEX)),
            SET(tens, ARRGET(var, INTRIGHTINDEX-1)),
            SET(hundreds, ARRGET(var, INTRIGHTINDEX-2)),
            WHILE(tens, PROG(
                DEC(tens),
                SET(retval, ADD(retval, 10)),
                )),
            WHILE(hundreds, PROG(
                DEC(hundreds),
                SET(retval, ADD(retval, 100)),
                )),
            ).code
    # SET will try to scrub it in the middle of the function otherwise.
    retval.can_clear = True
    return _IRV(out, retval)


# res <- var1 + var2
@uses_temporary_vars("var1_pos, var2_pos, var1_neg, var2_neg, both_pos, both_neg, signs_differ, inner_carry, loop, tmp")
def INTADD(var1, var2, res):
    out = ""
    out += PROG(
        SET(var1_pos, INTPOSITIVE(var1)),
        SET(var2_pos, INTPOSITIVE(var2)),
        SET(var1_neg, NOT(var1_pos)),
        SET(var2_neg, NOT(var2_pos)),
        SET(both_pos, AND(var1_pos, var2_pos)),
        SET(loop, INTARRAYLEN),
        SET(signs_differ, OR(AND(var1_pos, var2_neg), AND(var1_neg, var2_pos))),
        IF(signs_differ,
          #THEN
          lambda: IF(var1_pos,
              #THEN  var2 < 0 => var1 + var2 == var1 - (-var2)
              lambda: PROG(
                  INTNEGSELF(var2),
                  _int_sub_both_positive(var2, var1, res),
                  INTNEGSELF(var2)),
              #ELSE  var2 > 0 => var1 + var2 == var2 - (-var1)
              lambda: PROG(
                  INTNEGSELF(var1),
                  _int_sub_both_positive(var1, var2, res),
                  INTNEGSELF(var1)),
              ),
          #ELSE (signs are the same)
          lambda: IF(both_pos,
              #THEN
              lambda:
              _int_add_both_positive(var1, var2, res),
              #ELSE: both are negative
              lambda: PROG(
                  INTNEGSELF(var1), INTNEGSELF(var2),
                   _int_add_both_positive(var1, var2, res),
                  INTNEGSELF(var1), INTNEGSELF(var2), INTNEGSELF(res),
                  )))

    ).code
    return _IRV(out, None)


@uses_temporary_vars("inner_carry, tmp, loop")
def _int_add_both_positive(var1, var2, res):
    out = ""
    out += PROG(
                  _clear_int(res),
                  SET(loop, INTRIGHTINDEX),
                  WHILE(loop, PROG(
                      SET(tmp, ADD(ARRGET(var1, _nc(loop)),
                                   ARRGET(var2, _nc(loop)))),
                      IF(inner_carry, lambda: INC(tmp), lambda: NOP()),
                      SET(inner_carry, GT(tmp, 9)),
                      IF(inner_carry,
                          lambda: PROG(
                              # This is marginally slower and just 4 bytes shorter
                              # than manual roll-out
                              # _move_to(tmp),
                              # BF("----------"), # -10
                              # _return_from(tmp),
                              DEC(tmp), DEC(tmp), DEC(tmp),
                              DEC(tmp), DEC(tmp), DEC(tmp),
                              DEC(tmp), DEC(tmp), DEC(tmp), DEC(tmp),
                              ),
                          lambda: NOP()),
                      ARRSET(res, _nc(loop), tmp),
                      DEC(loop),
                      )),
                  ).code
    return _IRV(out, None)


@uses_temporary_vars("inner_carry, loop, tmp, tmp2")
def _int_sub_both_positive_inner(var1, var2, res):
    out = ""
    out += PROG(
        _clear_int(res),
        SET(loop, INTRIGHTINDEX),
        WHILE(loop, PROG(
            _clear(tmp),
            # +250k steps in sine
            #SET(tmp, SUB(inner_carry, tmp)),
            IF(inner_carry, lambda: DEC(tmp), lambda: NOP()),
            SET(tmp, ADD(tmp, ARRGET(var2, _nc(loop)))),
            SET(tmp, SUB(ARRGET(var1, _nc(loop)), tmp)),
            SET(tmp2, GT(tmp, 9)),  # Did carry overflow happen?
            IF(tmp2,
                lambda: PROG(SET(inner_carry, 1),
                            INC(tmp), INC(tmp), INC(tmp),
                            INC(tmp), INC(tmp), INC(tmp),
                            INC(tmp), INC(tmp), INC(tmp), INC(tmp),
                            ),
                lambda: SET(inner_carry, 0)),
            ARRSET(res, _nc(loop), tmp),
            DEC(loop))),
        ).code
    return _IRV(out, None)



@uses_temporary_vars("tmp, both_eq")
def _int_sub_both_positive(var1, var2, res):
    out = ""
    out += PROG(
               # When integers are equal I could skip the computation.
               # I would need to compute equality separately
               SET(both_eq, _inteq_both_positive(var2, var1)),
               SET(tmp, OR(_int_gt_both_positive(var2, var1), both_eq)),
               IF(both_eq, lambda: _clear_int(res),
                   lambda:
                        IF(tmp,
                           lambda: _int_sub_both_positive_inner(var1, var2, res),
                           lambda: PROG(
                               _int_sub_both_positive_inner(var2, var1, res),
                               INTNEGSELF(res)),
                           ))
               ).code
    return _IRV(out, None)


# res <- var2 -  var1
@uses_temporary_vars("var1_pos, sgns_diff")
def INTSUB(var1, var2, res):
    out = ""
    out += PROG(
        SET(var1_pos, INTPOSITIVE(var1)),
        SET(sgns_diff, _xor_two_bytes(NamedCell("ArrayElement", var1.first_addr + 3),
                        NamedCell("ArrayElement", var2.first_addr + 3))),

        IF(sgns_diff,
          #THEN
          lambda:
                PROG(
                    IF(var1_pos,
                        #THEN x > 0, y < 0 --> -(y + x)
                        lambda: PROG(
                            INTNEGSELF(var2),),
                        #ELSE x < 0, y > 0 --> (y + x)
                        lambda: PROG(
                            INTNEGSELF(var1),)),
                    _int_add_both_positive(var1, var2, res),
                    IF(var1_pos,
                        #THEN x > 0, y < 0 --> -(y + x)
                        lambda: PROG(
                            INTNEGSELF(var2),
                            INTNEGSELF(res)),
                        #ELSE x < 0, y > 0 --> (y + x)
                        lambda: PROG(
                            INTNEGSELF(var1))),),
          #ELSE signs are the same
          lambda: PROG(
              IF(var1_pos,  # this means that both are positive
                #THEN
                lambda: PROG(
                    ),
                #ELSE both are negative. res = (negate(var1) - negate(var2))
                lambda: PROG(
                    INTNEGSELF(var1), INTNEGSELF(var2),
                    )),
              _int_sub_both_positive(var1, var2, res),
              IF(var1_pos,  # this means that both are positive
                #THEN
                lambda: PROG(
                    ),
                #ELSE both are negative. res = (negate(var1) - negate(var2))
                lambda: PROG(
                    INTNEGSELF(var1), INTNEGSELF(var2), INTNEGSELF(res),
                    ))
            ))
    ).code
    return _IRV(out, None)


# Division and multiplication section
# TODO: remove helpers and compiler state manipulators to corresponding sections.

def _allocate_temp_int(name):
    global mmry
    foo = len(mmry)
    size = 3 + INTARRAYLEN * 2  # or the global INTMEMORYSIZE
    addr = find_proper_position_for(size, mmry)
    quuxmeep = Array(name, size, addr, INT)
    mmry[addr:addr+size] = [quuxmeep] * size
    if len(mmry) != foo:
        raise Exception("Memory has just bulged!")
    return quuxmeep

def _deallocate_temp_ints(*ints):
    global mmry
    size = 3 + INTARRAYLEN * 2
    for _int in ints:
        if isinstance(_int, Array) and _int.represented_type is INT:
            addr = _int.first_addr
            # mmry[_int.memory_range] = [None] * size
            # or! free(_int.memory_range)
            # def free(rnge): global mmry; mmry[slice(rnge)] = [None] * len(rnge)
            mmry[addr:addr+size] = [None] * size
        else:
            raise TypeError(f"Deallocation error: expected an INT, got {type(_int)}")


# retval <- number of digits in  var after dropping leftmost 0s
@uses_temporary_vars("retval, loop, pos, tmp")
def _int_num_of_digits(var):
    out = ""
    retval.can_clear = True
    out += PROG(
            SET(retval, INTRIGHTINDEX),
            INC(pos),
            PROG(*[INC(loop) for _ in range(INTRIGHTINDEX-1)]),
            WHILE(loop, PROG(
                SET(tmp, ARRGET(var, _nc(pos))),
                IF(tmp, lambda: _clear(loop),
                    lambda: PROG(INC(pos), DEC(retval), DEC(loop))),
                )),
    ).code
    return _IRV(out, retval)


# Increments a known positive integer in place
@uses_temporary_vars("loop, tmp, digit_overflow, inner_carry, tmp2, prev")
def _pos_int_inc(var):
    out = ""
    out += PROG(
            SET(loop, INTRIGHTINDEX),
            SET(tmp, ARRGET(var, _nc(loop))),
            INC(tmp),

            WHILE(loop, PROG(
            SET(digit_overflow, GT(tmp, 9)),
            IF(digit_overflow,
                #THEN
                lambda: PROG(
                    SET(tmp, SUB(10, tmp)),
                    ARRSET(var, _nc(loop), tmp),
                    SET(prev, SUB(1, loop)),

                    SET(tmp, ARRGET(var, _nc(prev))),
                    SET(tmp, ADD(tmp, 1)),
                    ARRSET(var, _nc(prev), tmp),
                    DEC(loop),
                    ),
                #ELSE
                lambda: PROG(
                    ARRSET(var, _nc(loop), tmp),
                    _clear(loop),
                    )),
                )),
    ).code
    return _IRV(out, None)


def _nc(var):
    """A stupid wrapper for a stupid problem

    ARRGET/SET does not recognize non-named cells, but works fine with a simple
    wrapper. TODO: fix ARRGET/SET and remove this wrapper"""
    return NamedCell("Yuk", var.addr)


# res <- var1*var2
# Currently is limited to len(var1) + len(var2) ≤ INTRIGHTINDEX. Overflows are
# not reported and are not corrected.
@uses_temporary_vars("var2_diglen, signs_differ, tmp, ppos")
def INTMUL(var1, var2, res):
    out = ""
    interm_res = _allocate_temp_int("INTMUL::interm_res")
    out += PROG(
        _clear_int(interm_res),
        _clear_int(res),

        SET(signs_differ, _xor_two_bytes(INTPOSITIVE(var1), INTPOSITIVE(var2))),
        SET(ppos, SUB(_int_num_of_digits(var2), INTARRAYLEN)),
        SET(var2_diglen, _int_num_of_digits(var2)),

        WHILE(var2_diglen, PROG(
            SET(tmp, ARRGET(var2, _nc(ppos))),
            WHILE(tmp, PROG(
                _int_add_both_positive(res, var1, interm_res),
                INTSET(res, interm_res),
                DEC(tmp),
            )),
            INC(ppos),
            DEC(var2_diglen),
            IF(var2_diglen, lambda: _int_shift_left_in_place(res), lambda: NOP()),
        )),
        IF(signs_differ, lambda: INTNEGSELF(res), lambda: NOP()),
    ).code

    _deallocate_temp_ints(interm_res)

    return _IRV(out, None)


@uses_temporary_vars("tmp3, run, signs_differ")
def _intdivmod_both_positive(var1, var2, div_res, mod_res):
    out = ""
    VAR2 = _allocate_temp_int("INTDIVMOD::VAR2")
    interm = _allocate_temp_int("INTDIVMOD::interm")

    out += PROG(
            _clear_int(VAR2),
            _clear_int(interm),
            _clear_int(div_res),

            INTSET(mod_res, var1),
            INTSET(VAR2, var2),
            # TODO: replace INTGT with _int_gt_both_positive
            SET(tmp3, OR(INTEQ(mod_res, VAR2), INTGT(mod_res, VAR2))),
            SET(run, 1),
            IF(tmp3,
              lambda:  # main code here
                    WHILE(run, PROG(
                                    _pos_int_inc(div_res),
                                    _int_sub_both_positive(VAR2, mod_res, interm),
                                    INTSET(mod_res, interm),
                                    SET(run, OR(INTEQ(mod_res, VAR2),
                                                INTGT(mod_res, VAR2))),
                                   )),
              lambda: NOP()),
    ).code

    _deallocate_temp_ints(interm)
    _deallocate_temp_ints(VAR2)

    return _IRV(out, None)


@uses_temporary_vars("var1_pos, var1_neg, var2_pos, var2_neg, signs_differ")
def INTDIVMOD(var1, var2, div_res, mod_res):
    out = ""
    # div_res = var1/var2
    # mod_res = var1%var2
    interm = _allocate_temp_int("INTDIVMOD::interm")
    out += PROG(
        _clear_int(interm),
        SET(var1_pos, INTPOSITIVE(var1)),
        SET(var2_pos, INTPOSITIVE(var2)),
        SET(var1_neg, NOT(var1_pos)),
        SET(var2_neg, NOT(var2_pos)),
        SET(signs_differ, OR(AND(var1_pos, var2_neg), AND(var1_neg, var2_pos))),
        IF(signs_differ,
          #THEN
          lambda:
              # Removing common code part resulted in just 654270 symbols!
              PROG(
                # Modulo is not well defined for negative numbers!
                # I am essentially replicating Python behavior here.
                IF(var1_pos,
                  #THEN var2 is negative   var1/-var2
                  lambda: PROG(INTNEGSELF(var2),),
                  #ELSE var2 is posititve  -var1/var2
                  lambda: PROG( INTNEGSELF(var1),)),
                _intdivmod_both_positive(var1, var2, div_res, mod_res),
                _pos_int_inc(div_res),
                _int_sub_both_positive(mod_res, var2, interm),
                INTSET(mod_res, interm),
                INTNEGSELF(div_res),
                IF(var1_pos,
                   #THEN var2 is negative, must restore it and also update results.
                   lambda: PROG(INTNEGSELF(var2), INTNEGSELF(mod_res),),
                   lambda: PROG(INTNEGSELF(var1),)),),
          #ELSE signs are the same
          lambda: PROG(
              # Cleaning this up reduces code further to 475633 symbols
              IF(var1_pos, #THEN both are positive
                 lambda: NOP(),
                 #ELSE both are negative
                 lambda: PROG( INTNEGSELF(var1), INTNEGSELF(var2),)),
              _intdivmod_both_positive(var1, var2, div_res, mod_res),
              IF(var1_pos, #THEN both are positive
                lambda: NOP(),
                lambda: PROG(INTNEGSELF(var1), INTNEGSELF(var2), INTNEGSELF(mod_res),)),
              ),),
    ).code

    _deallocate_temp_ints(interm)

    return _IRV(out, None)


@uses_temporary_vars("loop, tmp, tmp2")
def _int_shift_left_in_place(var):
    out = ""
    out += PROG(
            SET(loop, 2),
            WHILE(loop, PROG(
                SET(tmp, ARRGET(var, _nc(loop))),
                DEC(loop),
                _clear(tmp2),
                _non_destructive_copy(loop, tmp2),
                INC(loop),
                ARRSET(var, _nc(tmp2), tmp),
                INC(loop),
                SET(tmp, GT(loop, INTRIGHTINDEX)),
                IF(tmp, lambda: _clear(loop), lambda: NOP()),
                )),
            ARRSET(var, INTRIGHTINDEX, 0),
            ).code
    return _IRV(out, None)


@uses_temporary_vars("loop, tmp, tmp2")
def _int_shift_right_in_place(var):
    out = ""
    out += PROG(
            SET(loop, INTRIGHTINDEX),
            WHILE(loop, PROG(
                DEC(loop), _clear(tmp2), _non_destructive_copy(loop, tmp2), INC(loop),

                SET(tmp, ARRGET(var, _nc(tmp2))),
                ARRSET(var, _nc(loop), tmp),
                DEC(loop),
                SET(tmp, EQ(loop, 1)),  # Important! Do not optimize out!
                IF(tmp, lambda: _clear(loop), lambda: NOP()),
                )),
            ARRSET(var, 1, 0),
            ).code
    return _IRV(out, None)



# res <- var1*var2
# res, var1, var2 are of INT, they represent fixed point of 1.8 decimal
# 
# First variable must be normalized to sixth digit by shifting right.
# second one must be normalized to three digits.
# Result will be right-shifted by one digit.
@uses_temporary_vars("var1_rshift, var2_rshift")
def FXPMUL(var1, var2, res):
    out = ""
    var1_t = _allocate_temp_int("FXPMUL::var1_t")
    var2_t = _allocate_temp_int("FXPMUL::var2_t")
    out += PROG(
        INTSET(var1_t, var1),
        INTSET(var2_t, var2),
        # Too smart! You must always normalize to the same size. A better approach
        # would be to balance right shifts of variables and tie it together
        # with result's rightshift, however that is too smart.
        # I get error in 6th symbol when computing x^5 for 0.524 which is not too bad.
        SET(var1_rshift, 2),
        SET(var2_rshift, 5),
        WHILE(var1_rshift, PROG(
            _int_shift_right_in_place(var1_t), DEC(var1_rshift))),
        WHILE(var2_rshift, PROG(
            _int_shift_right_in_place(var2_t), DEC(var2_rshift))),
        INTMUL(var1_t, var2_t, res),
        _int_shift_right_in_place(res),
    ).code
    out += _clear_int(var1_t).code  # IMPORTANT!
    out += _clear_int(var2_t).code
    _deallocate_temp_ints(var1_t)
    _deallocate_temp_ints(var2_t)
    return _IRV(out, None)


# res <- var1/var2
#
# res, var1, var2 are of INT, they represent fixed point of 1.8 decimal
@uses_temporary_vars("tmp, inner_loop, outer_loop, fd, count, outer_condition, first_digit_zero")
def FXPDIV(var1, var2, res):
    out = ""
    remainder_t = _allocate_temp_int("FXPDIV::remainder_t")
    divisor_t = _allocate_temp_int("FXPDIV::divisor_t")
    int_tmp = _allocate_temp_int("FXPDIV::int_tmp")
    out += PROG(
        _clear_int(remainder_t), _clear_int(int_tmp),
        INTSET(remainder_t, var1),
        INTSET(divisor_t, var2),
        SET(outer_loop, 1),
        PROG(*[INC(outer_condition) for _ in range(INTDIGITSNUM)]),
        # NOTE: sign is not supported atm
        WHILE(outer_condition, PROG(
            # TODO: _int_gt_or_eq_both_positive
            #SET(inner_loop, OR(_int_gt_both_positive(remainder_t, divisor_t),
            #                   #INTEQ(remainder_t, divisor_t))),
            #                   _inteq_both_positive(remainder_t, divisor_t))),
            SET(inner_loop, _int_gtoreq_both_positive(remainder_t, divisor_t)),
            IF(inner_loop,
                #THEN can divide now.
                lambda: PROG(
                    _clear(count),  # in outer WHILE, don't touch it!
                    WHILE(inner_loop, PROG(
                        INC(count),
                        _int_sub_both_positive(divisor_t, remainder_t, int_tmp),
                        INTSET(remainder_t, int_tmp),
                        SET(tmp, OR(_int_gt_both_positive(remainder_t, divisor_t),
                                    #INTEQ(remainder_t, divisor_t))),
                                    _inteq_both_positive(remainder_t, divisor_t))),
                        # TODO: WARNING!
                        # This messes up the last digit
                        #SET(tmp, _int_gtoreq_both_positive(remainder_t, divisor_t)),
                        IF(tmp,
                            #Then we can continue
                            lambda: NOP(),
                            #ELSE break the inner loop
                            lambda: _clear(inner_loop),
                            ),
                        ),
                    ),
                    ARRSET(res, _nc(outer_loop), count),
                    _int_shift_left_in_place(remainder_t),
                    ),
                #ELSE have to shift remainder and result
                lambda: PROG(
                    SET(fd, ARRGET(remainder_t, 1)),
                    IF(fd,
                        #THEN (not zero)
                        lambda: PROG( _int_shift_right_in_place(divisor_t),),
                        #ELSE
                        lambda: PROG( _int_shift_left_in_place(remainder_t),),),
                    ARRSET(res, _nc(outer_loop), 0),
                    )),

            INC(outer_loop),
            DEC(outer_condition),
            )),
    ).code
    out += _clear_int(remainder_t).code
    out += _clear_int(int_tmp).code
    out += _clear_int(divisor_t).code
    _deallocate_temp_ints(remainder_t)
    _deallocate_temp_ints(int_tmp)
    _deallocate_temp_ints(divisor_t)
    return _IRV(out, None)


@uses_temporary_vars("tmp")
def FXPPRINT(var):
    out = ""
    out += PROG(
            SET(tmp, ARRGET(var, 0)),
            IF(tmp, lambda: PRINT("-"), lambda: NOP()),
             _print_array_digit(var, 1),
             PRINT("."),
             _print_array_digit(var, 2),
             _print_array_digit(var, 3),
             _print_array_digit(var, 4),
             _print_array_digit(var, 5),
             _print_array_digit(var, 6),
             _print_array_digit(var, 7),
             _print_array_digit(var, 8),
             _print_array_digit(var, 9),
            ).code
    return _IRV(out, None)

# Aliases for fixed point operations. Needed to make them more visible
# and not so confusing.
FXPDIVBY10 = INTDIV10 = _int_shift_right_in_place
FXPSUB = INTSUB
FXPADD = INTADD


def FXPSET(var, val):
    if isinstance(val, float):
        val = int(val * 10**8)
    return INTSET(var, val)


#-----------------------------------------------
# Assorted helpers
#-----------------------------------------------
def rle(s):
    out, s, ctr = [], list(s), 0
    while s:
        nxt = s.pop(0)
        if out:
            if out[-1] == nxt:
                ctr += 1
            else:
                # Super slow, compresses 600k symbols for 1.5 minutes.
                # <> compresses 608k do 114396
                # <>+- compresses 608k do 114396
                if out[-1] in ("<", ">", "+", "-"):
                    if ctr > 1:
                        out.append(str(ctr))
                else:
                    out.append(out[-1] * (ctr - 1))
                out.append(nxt)
                ctr = 1
        else:
            out.append(nxt)
            ctr += 1
    if ctr > 1:
        out.append(str(ctr))

    return "".join(out)

# Dumb, computationally expensive, but easy to implement:
def simple_compressor(code):
    while code.find("<>") > -1:  # iterates 9 times! with the unwind -- two times
        # Now this adds ~ as long as the compilation itself
        # For fxpmul_001.py compilation is about 250ms and optimization is
        # also about 250ms. Which is a fine tradeoff ATM.
        # The code below does maximal optimization
        code = code.replace("<<<<<<<<<<>>>>>>>>>>", "")
        code = code.replace("<<<<<<<<<<>>>>>>>>>>", "")
        code = code.replace("<<<<<<<<<>>>>>>>>>", "")
        code = code.replace("<<<<<<<<<>>>>>>>>>", "")
        code = code.replace("<<<<<<<<>>>>>>>>", "")
        code = code.replace("<<<<<<<<>>>>>>>>", "")
        code = code.replace("<<<<<<<>>>>>>>", "")
        code = code.replace("<<<<<<<>>>>>>>", "")
        code = code.replace("<<<<<<>>>>>>", "")
        code = code.replace("<<<<<>>>>>", "")
        code = code.replace("<<<<>>>>", "")
        code = code.replace("<<<>>>", "")
        code = code.replace("<<>>", "")
        code = code.replace("<>", "")
    while code.find("><") > -1:  # iterates just once
        code = code.replace(">>>>>>>>>>>>>>><<<<<<<<<<<<<<<", "")
        code = code.replace(">>>>>>>>>><<<<<<<<<<", "")
        code = code.replace(">>>>>><<<<<<", "")
        code = code.replace("><", "")
    while code.find("+-") > -1:  # Does not affect my test  -- never found
        code = code.replace("+-", "")
    while code.find("-+") > -1:  # does not affect my test -- never found
        code = code.replace("-+", "")
    return code

def posify(code):
    memptr = 0
    out = []
    for sym in code:
        if   sym == ">": memptr += 1; out.append(str(memptr))
        elif sym == "<": memptr -= 1; out.append(str(memptr))
        elif sym in "+-[].,": out.append(str(memptr))
        elif sym == "\n": out.append("\n")
        else: out.append(" ")
    out = "".join(out)
    return out, code

def prettify(code):
    res = rle(simple_compressor(code))
    r1, r2 = posify(res)
    r3 = zip(r1.split("\n"), r2.split("\n"))
    for r1, r2 in r3:
        print("".join(r2))
        print("".join(r1))
    return ""

def unmask_lambdas(data):
    data = data.replace("THEN:", "lambda:")
    data = data.replace("ELSE:", "lambda:")
    # TODO: here, make it a re.sub("BODY\((vars)\):", f"lambda {vars}:", data)
    data = data.replace("BODY:", "lambda:")  # For SUBPROG
    return data

comp_result = None
opt_timer = TimeIt("Optimization")
comp_timer = TimeIt("Compilation")
def compfile(fname="tests/while_1.py", verbose=False):
    with open(fname, "r") as f:
        data = f.read()
    data = unmask_lambdas(data)
    data = data.split("\n")
    data = "\n".join(l for l in data if l and l[0] != "#")
    data = re.sub("\nPROG\(", "\nglobal comp_result; comp_result = PROG(", data, count=1)
    fname, *basepath = fname.split("/")[::-1]
    basepath = basepath[::-1]
    outname = "/".join(basepath) + ".".join(fname.split(".")[:-1])
    outname_prog = outname + ".bf"
    outname_dbg = outname + ".dbg"
    result = exec(data)    # <-------
    rslt = comp_result[0]
    rslt = rslt.replace(" ", "").replace("\n", "")
    return opt_timer(lambda: (simple_compressor(rslt)))



def prof(fname="output"):
    fname = fname +".pyprofile"
    from cProfile import run
    from pstats import SortKey
    import pstats
    run("compfile('tests/fxpmul_001.py')", fname)
    p = pstats.Stats(fname)
    p.sort_stats(SortKey.TIME).print_stats(0.08)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please specify a file to compile")
    else:
        comp_timer = TimeIt("Compilation")
        res = comp_timer(lambda: compfile(sys.argv[1], True))
        comp_timer.print_report()
        print("Of it optimization took:")
        opt_timer.print_report()
        print(f"Code len: {len(res)}")
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w") as f:
            f.write(res)
