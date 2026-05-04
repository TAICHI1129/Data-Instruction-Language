#DIL (Data Instruction Language) Specification

1. Overview

DIL (Data Instruction Language) is a human-readable, machine-interpretable language for defining data and lightweight instructions.
It is designed to be executed by an external runtime (e.g., Python) and is not executable on its own.


---

2. Design Principles

Symbol-based syntax (no indentation dependency)

Clear and unambiguous grammar

Combination of data definition and instruction flow

Execution handled externally (e.g., Python)



---

3. Core Syntax

3.1 Definition (Assignment)

key < value

Assigns a value to a key.

Example:

user.name < "Taichi"
user.age < 13


---

3.2 Output (Flow)

value > target

Transfers a value to a target.

Example:

user.name > output.username


---

3.3 Comparison Operators

a <? b   # less than
a >? b   # greater than
a =? b   # equal to


---

3.4 Conditional Statement

if condition {
  statements
}

Example:

if user.age >? 12 {
  user.name > result.name
}


---

4. Data Types

Type	Example

Number	100, 3.14
String	"text"
Boolean	true, false
Array	[1, 2, 3]
Object	{ name: "Taichi" }



---

5. Path Syntax

Nested data structures are accessed using dot notation:

user.profile.name < "Taichi"


---

6. Execution Model

Statements are executed from top to bottom

Referencing an undefined variable results in an error

Types are automatically inferred



---

7. Integration with Python

7.1 Load Data

import dil

data = dil.get("config.dil")


---

7.2 Execute Instructions

env = {}
dil.run("config.dil", env)


---

7.3 Direct Access

dil.get("config.dil", "user.name")


---

8. Error Handling

8.1 Syntax Errors

DIL Syntax Error:
  Line X: description


---

8.2 Runtime Errors

Undefined variables

Type mismatches

Invalid operators



---

9. Constraints

DIL is not executable by itself

External system (e.g., Python) is required

Side effects and external execution are not part of the core specification



---

10. Future Extensions (Planned)

Additional operators

Improved type system

Enhanced control structures
