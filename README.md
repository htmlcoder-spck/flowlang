# FlowLang

**FlowLang** is a custom programming language and zero-dependency compiler written in pure Python that translates FlowLang source code directly into raw **x86-64 machine code**.

## Features
* **Explicit Static Typing:** Variables require explicit type annotations (`int`, `bool`, `char`, `string`).
* **Readable Control Flow:** Python-style indentation paired with explicit `then:` blocks and clean comparison operators (`=` for equality, `!` for inequality).
* **Zero-Dependency Compiler:** Built using only Python's standard library (`re` and `bytearray`)—no external parser generators or third-party packages required.
* **Direct Machine Code Generation:** Compiles Abstract Syntax Tree (AST) nodes straight into x86-64 Linux instruction bytes (`MOV`, `CMP`, `SYSCALL`).

---

## Language Syntax

### Variables
Variables are declared using `var <type>:<name> = <value>`:
```text
var int:x = 1
var bool:isRunning = TRUE
var char:test = "A"
var string:a_string = "String."
```

### Conditionals
Conditionals use `=` for equality checks, `!` for inequality checks, and `then:` before indented blocks:
```text
if (x = 1) then:
   PrintLine("An if.")
elif (x ! 1) then:
   PrintLine("NOT")
else then:
   PrintLine("Else.")
```

### Loops & Output
```text
// Built-in console output
PrintLine("Something...")

// Range-based for loop
for i range:
   // Loop body

// Conditional while loop
while true:
   // Loop body
```

---

## Project Structure

```text
flowlang/
├── .github/
│   └── workflows/
│       └── test.yml      # GitHub Actions CI workflow
├── parser.py             # Lexer, parser, and x86-64 machine code generator
├── flowlang.txt          # Example FlowLang source file
└── README.md             # Language documentation
```

---

## Usage

### Run Locally
Ensure you have **Python 3.10+** installed, then run the compiler against `flowlang.txt`:

```bash
python parser.py
```

The compiler will tokenize and parse `flowlang.txt` and output the generated x86-64 machine code in hexadecimal format:
```text
Machine Code (Hex): b8 05 00 00 00 3d 05 00 00 00 ...
```

### Continuous Integration (GitHub Actions)
Every push to the repository automatically triggers `.github/workflows/test.yml`, which spins up an Ubuntu runner and verifies that `parser.py` compiles `flowlang.txt` without syntax or runtime errors.

---

## Roadmap
* [ ] Add ELF header generation to output standalone Linux executables
* [ ] Expand code generator to support `elif`, `else`, `for`, and `while` loops
* [ ] Support variable storage on the stack/registers beyond single-register evaluation
