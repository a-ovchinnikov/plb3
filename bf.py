"""3-bit BF machine"""
from itertools import chain


# Это вспомогательные функции для читаемости кода. Можно было бы оставить их
# просто синонимами к None, однако я заметил, что психологически проще читать
# код где повелительное наклонение содержит вызов функции.
break_the_bracket_loop = lambda: None
enter_the_bracket_loop = lambda: None
ignore_any_other_symbol = lambda: None


# No specific repr since this is a base class with specific width
class NumberKbit(int):
    # Would be nice to have validating decorators here
    def __new__(cls, value, bitwidth):
        maxval = 2**bitwidth
        if isinstance(value, int):
            if value >= maxval or value < 0:
                raise ValueError(f"{__class__}: init {value=} must be >0 and <={maxval}")
            obj = int.__new__(cls, value)
            obj.bitwidth = bitwidth
            return obj
        raise ValueError(f"{__class__}: cannot instantiate from non-int")

    # __radd__ not defined atm, probably don't need it.
    def __add__(self, other):
        other = __class__(other, self.bitwidth)
        result = super().__add__(other) % 2**self.bitwidth
        return __class__(result, self.bitwidth)

    def __sub__(self, other):
        other = __class__(other, self.bitwidth)
        result = super().__sub__(other) % 2**self.bitwidth
        return __class__(result, self.bitwidth)

    def __str__(self):
        # This is very dumb, please fix.
        return str(self.numerator)





class Number8bit(NumberKbit):
    def __new__(cls, value):
        return NumberKbit.__new__(cls, value, 8)

    # These magics have to be defined to explicitly wrap the result into correct type.
    def __add__(self, other):
         return self.__class__(super().__add__(other))

    def __sub__(self, other):
        return self.__class__(super().__sub__(other))

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self):
        return super().__str__()


LBRACKET = "["
RBRACKET = "]"
LEFT = object()
RIGHT = object()
HALT = object()

class AllottedStepsOverflow(ValueError):
    pass

class BracketStackUnderflow(ValueError):
    pass

# Values are hardcoded, don't want  to mess with too much volatility.
class BFI:
    """An interpreter with hooks for all steps"""
    # Register callbacks for all objects in a rable? Too complicated for indirect
    # objects _probably_
    def __init__(self, mempwr=10, maxsteps=9*10**10, stdin=None):
        self.max_steps = maxsteps  # To prevent runaway programs.
        self.mempwr =  mempwr
        self.memsize = 2**self.mempwr
        self.stdin = [] if stdin is None else stdin[:]


        self.stdout = []
        self.reset()

    def pre_dec_hook(self):
        pass

    def post_dec_hook(self):
        pass

    # Should it even be in the class?
    @staticmethod
    def brackets_are_balanced(code):
        """Ensures that brackets match

        >>> BFI.brackets_are_balanced("[]")
        True
        >>> BFI.brackets_are_balanced("[[++[<>-.]--+]][]")
        True
        >>> BFI.brackets_are_balanced("[[++[<>-.]--+]][]]")
        False
        >>> BFI.brackets_are_balanced("][")
        False
        >>> BFI.brackets_are_balanced("[][")
        False
        >>> BFI.brackets_are_balanced("[")
        False
        >>> BFI.brackets_are_balanced("]")
        False
        """
        # Maybe make this a chain too? I.e. allow offset constructs like
        # ++] .... [--. This would add a concept of a second belt to
        # the game.
        lbracket_stack = 0
        for sym in code:
            if sym == LBRACKET:
                lbracket_stack += 1
            elif sym == RBRACKET:
                if lbracket_stack > 0:
                    lbracket_stack -= 1
                else:
                    return False
            else:
                continue
        return lbracket_stack == 0


    def reset(self):
        self.steps_taken = 0
        self.bracket_depth = 0  # Should be a positive number always,
                                # and fail when underflows
        # Must stay the same between handling of individual symbols on the code tape
        # bc can change depending of their value _and_ previous state affects
        # meaning of the current symbol.
        self.bounce_direction = None
        self.memory = [Number8bit(0) for x in range(self.memsize)]
        self.memptr = NumberKbit(0, self.mempwr)

    def emit_current(self):
        self.stdout.append(self.memory[self.memptr])
        # pass  # do something with self.memory[self.ptr] and pre-registered IO

    def set_current(self):
        self.memory[self.memptr] = Number8bit(self.stdin.pop(0))
        pass  # do something with self.memory[self.ptr] and pre-registered IO

    def prime_fast_forward(self):  # tape_to_the_right_until_matching_bracket
        self.bounce_direction = RIGHT

    def prime_rewind(self): # tape_to_the_left_until_matching_bracket
        self.bounce_direction = LEFT

    def unset_any_skip(self):
        self.bounce_direction = None

    def found_matching_bracket(self):
        return self.bracket_depth == 0

    def decrease_bracket_depth(self):
        self.bracket_depth -= 1
        if self.bracket_depth < 0:
            raise BracketStackUnderflow()

    def current_cell_is_empty(self):
        return self.memory[self.memptr] == 0

    def process_symbol(self, sym):
        if sym == "$":
            self.bounce_direction = HALT  # Do I even need this symbol? 
            return
        if self.bounce_direction is None:
            if   sym == "+": self.memory[self.memptr] += 1
            elif sym == "-": self.pre_dec_hook(); self.memory[self.memptr] -= 1; self.post_dec_hook()
            elif sym == ">": self.memptr += 1
            elif sym == "<": self.memptr -= 1
            elif sym == ".": self.emit_current()
            elif sym == ",": self.set_current()
            elif sym == "]": break_the_bracket_loop() if self.current_cell_is_empty() else self.prime_rewind()
            elif sym == "[": self.prime_fast_forward() if self.current_cell_is_empty() else enter_the_bracket_loop()
            else: ignore_any_other_symbol()
        elif self.bounce_direction is LEFT:
            if   sym == "]": self.bracket_depth += 1
            elif sym == "[": self.unset_any_skip() if self.found_matching_bracket() else self.decrease_bracket_depth()
            else: ignore_any_other_symbol()
        elif self.bounce_direction is RIGHT:
            if   sym == "[": self.bracket_depth += 1
            elif sym == "]": self.unset_any_skip() if self.found_matching_bracket() else self.decrease_bracket_depth()
            else: ignore_any_other_symbol()

    def process_code(self, code):
        code_pos, self.steps_taken = 0, 0
        while self.steps_taken < self.max_steps and code_pos < len(code):
            self.steps_taken += 1
            self.process_symbol(code[code_pos])
            if   self.bounce_direction is  None: code_pos += 1
            elif self.bounce_direction is  LEFT: code_pos -= 1
            elif self.bounce_direction is RIGHT: code_pos += 1
            elif self.bounce_direction is  HALT: break
            else:
                raise TypeError(f"Unexpected bounce: {self.bounce_direction}")
        if self.steps_taken == self.max_steps:
            raise AllottedStepsOverflow("Code ran for too long")


class CompressedBFI(BFI):
    # TODO: finish it some day
    def process_code(self, code):
        self.offset = 0
        code_pos, self.steps_taken = 0, 0
        while self.steps_taken < self.max_steps and self.offset < len(code):
            self.steps_taken += 1
            old_offset = self.offset
            sym, reps = self.get_s_with_repetitions(code)
            self.process_symbol(sym, reps)
            if   self.bounce_direction is  None: pass
            elif self.bounce_direction is  LEFT:
                self.offset = old_offset - 1  #(...)
            elif self.bounce_direction is RIGHT: self.offset = old_offset +  1
            elif self.bounce_direction is  HALT: break
            else:
                raise TypeError(f"Unexpected bounce: {self.bounce_direction}")
        if self.steps_taken == self.max_steps:
            raise AllottedStepsOverflow("Code ran for too long")
    def get_s_with_repetitions(self, s):
        reps = 1
        sym = s[self.offset]
        new_offset = self.offset + 1
        while new_offset < len(s) and s[new_offset].isdigit():
            new_offset += 1
        if foo := s[self.offset+1:new_offset]:
            reps = int(foo)
        self.offset = new_offset
        return sym, reps

    def process_symbol(self, sym, reps):
        if sym == "$":
            self.bounce_direction = HALT
            return
        if self.bounce_direction is None:

            if   sym == "+": self.memory[self.memptr] += reps
            elif sym == "-": self.memory[self.memptr] -= reps
            elif sym == ">": self.memptr += reps
            elif sym == "<": self.memptr -= reps
            elif sym == ".": self.emit_current()
            elif sym == ",": self.set_current()
            elif sym == "]": break_the_bracket_loop() if self.current_cell_is_empty() else self.prime_rewind()
            elif sym == "[": self.prime_fast_forward() if self.current_cell_is_empty() else enter_the_bracket_loop()
            else: ignore_any_other_symbol()
        elif self.bounce_direction is LEFT:
            if   sym == "]": self.bracket_depth += 1
            elif sym == "[": self.unset_any_skip() if self.found_matching_bracket() else self.decrease_bracket_depth()
            else: ignore_any_other_symbol()
        elif self.bounce_direction is RIGHT:
            if   sym == "[": self.bracket_depth += 1
            elif sym == "]": self.unset_any_skip() if self.found_matching_bracket() else self.decrease_bracket_depth()
            else: ignore_any_other_symbol()

class FastBFI(BFI):
    def process_symbol(self, sym):
        if sym == "$":
            self.bounce_direction = HALT
            return
        if self.bounce_direction is None:
            if   sym == "+": self.memory[self.memptr] += 1
            elif sym == "-": self.pre_dec_hook(); self.memory[self.memptr] -= 1; self.post_dec_hook()
            elif sym == ">": self.memptr += 1
            elif sym == "<": self.memptr -= 1
            elif sym == ".": self.emit_current()
            elif sym == ",": self.set_current()
            elif sym == "]": break_the_bracket_loop() if self.current_cell_is_empty() else self.prime_rewind()
            elif sym == "[": self.prime_fast_forward() if self.current_cell_is_empty() else enter_the_bracket_loop()
            else: ignore_any_other_symbol()
        elif self.bounce_direction is LEFT:
            if   sym == "]": self.bracket_depth += 1
            elif sym == "[": self.unset_any_skip() if self.found_matching_bracket() else self.decrease_bracket_depth()
            else: ignore_any_other_symbol()
        elif self.bounce_direction is RIGHT:
            if   sym == "[": self.bracket_depth += 1
            elif sym == "]": self.unset_any_skip() if self.found_matching_bracket() else self.decrease_bracket_depth()
            else: ignore_any_other_symbol()

    def process_code(self, code):
        code_pos, self.steps_taken = 0, 0
        while self.steps_taken < self.max_steps and code_pos < len(code):
            self.steps_taken += 1
            self.process_symbol(code[code_pos])
            if self.bounce_direction is  HALT: break
            else:
                raise TypeError(f"Unexpected bounce: {self.bounce_direction}")
        if self.steps_taken == self.max_steps:
            raise AllottedStepsOverflow("Code ran for too long")

class BFItracing(BFI):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.call_stack = []

    # Todo: remove
    @staticmethod
    def loadc(fn):
        with open(fn, "r") as f:
            return f.read()

    def prepare_annotations(self, dbg_fname):
        from sreader import read_tests, sreader
        data = read_tests(dbg_fname)
        annotations = sreader(data)

        _id = lambda a: a[0]
        _call = lambda a: " ".join(e[:-2] if e.find('@')>-1 else e for e in a[1])
        _mmap = lambda a: a[2]

        self.pcalls = dict((_id(a), _call(a)) for a in annotations)
        self.memsta = dict((_id(a), _mmap(a)) for a in annotations)

    def annotate_call_stack(self):

        out = ("Call stack:\n")
        for pad, el in enumerate(self.call_stack):
            out += ("  "*pad + self.pcalls[el.lstrip('0')] + "\n")
        out += ("Allocations:\n")
        current_allocations = self.memsta[self.call_stack[-1].lstrip('0')] if self.call_stack else ''
        ca = " ".join(chain(*current_allocations))
        out += ca
        return out
        return annotations


    def process_code(self, code):
        code_pos, self.steps_taken = 0, 0
        out = ""
        self.prepare_annotations()
        while self.steps_taken < self.max_steps and code_pos < len(code):
            self.steps_taken += 1
            # Annotations likely work, all that is left is interactive interaction.
            # This probably is a very bad idea.
            if code[code_pos] == "{" and self.bounce_direction is None:
                self.call_stack.append(code[code_pos+1:code_pos+10])
                code_pos += 10
                continue
            elif code[code_pos] == "}" and self.bounce_direction is None:
                self.call_stack.pop(-1)
                code_pos += 1
                continue

            out += "---------------\n"
            out += self.annotate_call_stack()
            out +="\n   Memory:\n"
            out += (code[code_pos] + " " + " ".join(f"{x}" for x in self.memory[:20]) + "\n")
            out += "Ptr to " + str(self.memptr)+ "\n"
            if   self.bounce_direction is  None: out += "Execution\n"
            elif self.bounce_direction is  LEFT: out +=("Rewind to left\n")
            elif self.bounce_direction is RIGHT: out +=("Rewind to right\n")
            out += "\n"

            self.process_symbol(code[code_pos])

            if   self.bounce_direction is  None: code_pos += 1
            elif self.bounce_direction is  LEFT: code_pos -= 1
            elif self.bounce_direction is RIGHT: code_pos += 1
            elif self.bounce_direction is  HALT: break
            else:
                raise TypeError(f"Unexpected bounce: {self.bounce_direction}")
        if self.steps_taken == self.max_steps:
            raise AllottedStepsOverflow("Code ran for too long")

        with open("big_trace.log", "w") as f:
            f.write(out)
# Currently running annotated code looks like this:
#   Call stack:
#    IF Z <lambda> <lambda>
#      PRINT *
#   Allocations:
#   0 X 1 Z 2 IF:tmp0::6 3 IF:tmp1::7
#      Memory:
#   [   1 0 1 0 39 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#   Rewind to right
# I can just leave everything as is, but digging through a full trace
# is rather tiring. It ends up being rather long. Maybe this is not so bad?
# Extra visual marker for the change of specified entities?

def dtest():
    import doctest
    failures, tests = doctest.testmod()
    print(f"All done. There were {failures} failures of {tests} tests.")
