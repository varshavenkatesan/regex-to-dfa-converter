# Regular Expression to DFA Converter

This project provides a Python script that converts a given regular expression (RE) into its equivalent Deterministic Finite Automaton (DFA). It implements standard compiler design algorithms, including the Shunting-yard algorithm for postfix conversion, Thompson's Construction for NFA creation, and the Subset Construction algorithm for the final NFA to DFA conversion.

This program was created as a solution for the "Special Assignment for Fast Learners" in the course **CSE23CT302 - Theory of Computation and Compiler Design** at **Sri Ramachandra Faculty of Engineering and Technology**.

---
## Features

* **RE to Postfix**: Converts standard infix regular expressions to postfix notation.
* **Thompson's Construction**: Builds a Nondeterministic Finite Automaton (NFA) from the postfix expression.
* **Subset Construction**: Converts the NFA into an equivalent DFA, eliminating ε-transitions and nondeterminism.
* **DFA Simulation**: Validates input strings against the generated DFA to determine if they are accepted by the language.
* **Clear Output**: Displays a clean, formatted transition table for the resulting DFA.

---
## How to Run
### **Requirements**
* Python 3.x

### **Execution**
No external libraries are needed. Simply save the code as a Python file (e.g., `converter.py`) and run it from your terminal:
python converter.py

### **Assignment Problems Solved**
The script is designed to solve the specific problems outlined in the assignment.
**Question 1**
* **Task:** Write a program to convert a given regular expression into its equivalent DFA.
* **Input RE:** (a/b)*abb 
* **Output:** A formatted DFA transition table.

**Question 2**
* **Task:** Write a program that converts the RE (0|1)*01 into a DFA and validates a given set of strings.
* **Input RE:** (0|1)*01 
* **Strings to test:** 1101, 111, 0001 
* **Output:** An "Accepted" / "Rejected" status for each string.

### **Script Output**
When executed, the script will produce the following output, solving both problems sequentially.
