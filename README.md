# CO-Project

## Team Members

- Mohammad Umar `2023324`
- Sakshat Sachdeva `2023474`
- Vidush Jindal `2023592`
- Sarthak Bhudolia `2023491`

## How to Run

 1. Download the repository and make sure that you have the Assembler.py opened.
 2. Go to the terminal and run `python assembler.py input.txt output.txt`.
 3. To check if the test cases are correct or not, use the automated framework by running it in command prompt or the terminal.
 4. The output will show how many test cases are correct!
 

## Simple-Assembler
#### The [Simple-Assembler](https://github.com/6Umar9/CO-Project/tree/main/SimpleAssembler) is the first part of the program.

The Assembler is based on the `RISC V32I` system.

The above directory contains the key assembler that was finalised by the group. It translates the input in `Assembly language` to `Binary` and allows us to check the correctness of it by checking against test cases.

It checks for the type of instructions (`B-Type, R-Type and so on`), verifies if it is an **op-code** runs a check on the input and whether it is a register, immediate or label.

The labels as well as the immediates were taken into account and verified for each line. The Assembler follows the project details and produces an error if it detects an invalid `opcode`, `register`, `label` or out of bound `immediate` value.

## Simple-Simulator
#### linkhere

Takes binary input

This is done through the construction of *dictionaries* which contain all the registers, functions which check *labels* and *immediates*, and finally, *functions* which contains the instructions based on the *op-code*.

## Automated Testing Cases

The directory [**automatedTesting**](https://github.com/6Umar9/CO-Project/tree/main/automatedTesting) contains the `src` file for the automated running. The `bin` folder contains the binary and simplebin test cases.

Running the main.py will enable you to run the check!

## Back-up files
The directory [**backupfiles**](https://github.com/6Umar9/CO-Project/tree/main/backupfiles) contains all the progress made by the team over the period of time to build the `Assembler`.

It was a **team effort** and we are glad it pulled through!

Each file contains a certain amount of code for the assembler, and how it was made over the period of time. All the indenting, code changes, and comments from the *start* to the *end* are present here!

## Misc.
The PDF attached contains all the information on how a `RISC V32I` Assembler works and how the ouput is supposed to be.

> The format while displaying the Assembler's output is smae as the mentioned in the file.

The `readme.txt` contains information on how the testing framework works, and how the assembler and simulator are to be built and differentiated.



## End
On the behalf of the team, we thank you for going through the repo and reviewing it! 
