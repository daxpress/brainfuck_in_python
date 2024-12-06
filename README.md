# BrainfuckMachine

A simple `Brainfuck` interpreter written in Python.
This interpreter executes Brainfuck code by simulating a tape and pointer,
with built-in error handling and support for basic Brainfuck commands.

## Features

Simulates a Brainfuck machine with a customizable tape length.
Supports Brainfuck commands: `+`, `-`, `<`, `>`, `[`, `]`, `.`.  
Error handling for invalid commands and mismatched brackets.
Prints characters with the . command.

## Installation

Clone the repository or download the brainfuck_machine.py file.

```bash
git clone https://github.com/daxpress/brainfuck-machine.git
```

## Usage

* Create a `BrainfuckMachine` instance with a specified tape length.  
* Set the `code` attribute to your Brainfuck program as a string (input command `,` is not yet implemented).  
* Call the `run()` method to execute the code.

## Example

```py
from brainfuck_machine import BrainfuckMachine

# Create an interpreter with a tape of length 30000
bf_machine = BrainfuckMachine(len=30000)

# Set the Brainfuck code to run
bf_machine.code = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."

# Run the code
bf_machine.run()
```

### Output
```bash
Hello World!
```

## Notes

The `,` command (input) is not yet implemented.  
The interpreter currently prints the output using the `.` command.

## Testing

To test the BrainfuckMachine, the Python `unittest` module is used.  
Simply run the following command to execute the tests:

```bash
py .\aiv_brainfuck.py
```

## Future Improvements

* Implement the missing `,` command for input handling.  
* Transforming the interpreter into a standalone script with a CLI.  
* Optimize tape handling for larger programs.
