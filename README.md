Instructions for Running MathScript
1. Setting Up the Project
Create the Project Directory

bash

mkdir mathscript_project
cd mathscript_project
Create the Python Files

Save each of the provided code snippets into their respective files within the mathscript_project directory.

Create the Examples Directory

bash

mkdir examples
And save the example1.ms file into the examples/ directory.

2. Running the REPL
To start the MathScript interactive shell:

bash

python repl.py
Example Usage:

python

Welcome to MathScript REPL
>>> x = 5
>>> y = ∑(i=1, x, i^2)
>>> y
55.0
>>> area = ∫(x=0, π, sin(x))
>>> area
2.0
3. Running a MathScript File
To run a MathScript program from a file:

bash

python cli.py examples/example1.ms
Expected Output:

css

Variables: {'x': 10, 'y': 55.0, 'z': 120.0, 'area': 2.0, 'result': 187.0}
4. Understanding the Example Program
The example1.ms file contains the following code:

plaintext

x = 10
y = ∑(i=1, x, i)
z = ∏(i=1, 5, i)
area = ∫(x=0, π, sin(x))
result = x + y + z + area
x = 10: Assigns the value 10 to the variable x.
y = ∑(i=1, x, i): Calculates the sum of i from i=1 to i=x (which is 10). This is the sum of the first 10 natural numbers.
z = ∏(i=1, 5, i): Calculates the product of i from i=1 to i=5. This is the factorial of 5.
area = ∫(x=0, π, sin(x)): Calculates the definite integral of sin(x) from x=0 to π.
result = x + y + z + area: Sums up all the previous results.
