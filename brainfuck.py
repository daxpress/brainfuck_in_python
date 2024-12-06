class BrainfuckMachine():
    """A Brainfuck Virtual Machine written by Daniel Corrieri"""
    # DISCLAIMER: I'm aware that some functions could have been avoided (subtract is add but with -1 etc...)
    # but I decided to implement them for better general code readability;
    # Print with "." is also implemented, just for fun

    def __init__(self, len):
        # creates a tape of length "len"
        # this will contain the values
        self.tape = []
        for i in range(len):
            self.tape.append(0)
        # head is the pointer to the current index in tape
        self.head = 0
        # current instruction pos is the pointer parsing the code
        self._current_instruction_pos = 0
        # code is where the code to run is stored
        self.code = ""

        self._current_instruction = ""
        # dictionary that contains the instructions
        self._instructions = {
            "+": self._add,
            "-": self._subtract,
            "<": self._reduce_head_index,
            ">": self._increment_head_index,
            "[": self._open_bracket,
            "]": self._close_bracket,
            ".": self._print_current,
        }
        # stores the loop cells indexes after the open square bracket
        self._loop_starts = []
        
    def run(self):
        """runs the code stored in self.code"""
        # if there is no code the execution doesn't start
        if not self.code: return
        self.head = self.tape[0]
        self._current_instruction_pos = 0
        self._loop()
        
    def _loop(self):
        """main loop"""
        while self._current_instruction_pos < len(self.code):
            self._current_instruction = self.code[self._current_instruction_pos]
            if self._current_instruction in self._instructions:
                #runs the corresponding method
                self._instructions[self._current_instruction]()
                self._current_instruction_pos += 1
            else:
                raise self.CommandNotFound(self._current_instruction + " is not a valid command")

        if self._loop_starts:
            raise self.BracketMismatch("There are one or more open brackets left")


    def _add(self):
        """Adds 1 to the currently pointed value simulating an 8bit overflow"""
        self.tape[self.head] = (self.tape[self.head] + 1) % 256

    def _subtract(self):
        """Subtracts 1 to the currently pointed value simulating an 8bit overflow"""
        self.tape[self.head] = (self.tape[self.head] - 1) % 256

    def _increment_head_index(self):
        """Moves the head forward once"""
        if self.head >= len(self.tape):
            raise self.HeadOverflow(f"Head position is greater than {len(self.tape)}: Head position = {self.head}")
        self.head = self.head + 1

    def _reduce_head_index(self):
        """Moves the head back once"""
        self.head = self.head - 1
        if self.head < 0:
            raise self.HeadOverflow(f"Head position is less than 0: Head position = {self.head}")

    def _open_bracket(self):
        """Opens a loop/if if the current node cell isn't 0"""
        self._loop_starts.append(self._current_instruction_pos)
        if self.tape[self.head] == 0:
            self._skip_loop()


    def _close_bracket(self):
        """Closes the current loop when the node cell acting as index gets to 0"""
        if self.tape[self.head] == 0:
            try:
                self._loop_starts.pop()
            except IndexError:
                raise self.BracketMismatch("There is a closing bracket before an opening one")
            return
        # all the other cases (well, positive value...) jumps back
        self._current_instruction_pos = self._loop_starts[-1]
            
            


    def _skip_loop(self):
        """Skips the whole loop if the head value is 0 BEFORE the first start of the loop"""
        # enters the loop
        self._current_instruction_pos += 1
        while self.tape[self.head] == 0 and self._current_instruction_pos < len(self.code) and self._loop_starts:
            # =========================================================================================
            # if the head pointed value is 0 AND
            # current_instruction_pos is not out of code range (basically 'till the last instruction) 
            # AND the loop stack is not empty ===>
            # ------------------------------------------------------------------------------------------
            # proceedes in the loop and runs the brackets instructions to change the bracket stack
            # and eventually stop skipping.
            # the brackets will only append or pop other brackets until they are finished in this scope
            # =========================================================================================
            self.instruction = self.code[self._current_instruction_pos]
            if  self.instruction == "[" or self.instruction == "]":
                    self._instructions[self.instruction]()
            
            # finally increments the code pointer to proceed till the end of the loop
            self._current_instruction_pos += 1
        
    def _print_current(self):
        """prints the value inside the tape cell as a char"""
        print(chr(self.tape[self.head]), end="")
        
    class HeadOverflow(Exception):
        """Raised when the head points to a value out of the [0, len] range"""
        def __init__(self, message = "Head index is out of tape range"):
            super().__init__(message)


    class BracketMismatch(Exception):
        """Raised when one or more loops are open after the end of the code"""
        def __init__(self, message = "The order or the number of brackets is incorrect"):
            super().__init__(message)


    class CommandNotFound(Exception):
        """Raised when the command is not valid"""
        def __init__(self, message = "Command is not valid"):
            super().__init__(message)
