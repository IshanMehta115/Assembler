# Assembler Project

This project is an assembler that converts assembly code into machine code. It takes two input files: `input.txt`, which contains the assembly code, and `opcode.txt`, which contains the opcode table.

## How to Use

1. Clone the repository: `git clone https://github.com/IshanMehta115/Assembler.git`
2. Place your assembly code in the `input.txt` file.
3. Create or update the `opcode.txt` file with the opcode table for your specific architecture.
4. Run the assembler: `python assembler.py`
5. The assembler will generate the output machine code in a file named `machineCode.txt`.
6. The symbol table, which contains information about variables and labels, will be saved in the `symbolTable.txt` file.


## Error Reporting

The assembler performs basic error checking and reports the following types of errors:

- Undefined variables
- Duplicate variable declarations
- Invalid instructions
- Missing operands

If any errors are found in the assembly code, the assembler will display error messages indicating the line number and the nature of the error.

## Contributing

Contributions to this project are welcome. If you encounter any bugs, issues, or have suggestions for improvements, please create a new issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).


