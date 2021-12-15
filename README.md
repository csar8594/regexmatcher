# Automata and Logic Project I -- Regex Matcher

In this project the goal is to implement a regex matcher that supports:
- Union
- Concatenation
- Kleene Star

In this case since I understood the + as the occurence of 1 to n instead of the union my program also supports the + and not only *.

## Programming Language:
- Python

## Prerequisites:
### Installed system packages:
Make sure your **Linux**-System has the following packages installed:
- *python3*

## Syntax:
| Operator      	| Usage  	|
|---------------	|--------	|
| Kleene Star   	| a*     	|
| Plus          	| a+     	|
| Union         	| (a\|b) 	|
| Concatenation 	| ab     	|

> **_NOTE:_**  It is recommended to always use brackets **()** in case of Union (see table above) to ensure correct functionality


## Running the Regex-Matcher:

To start the program one can run the command in a terminal:

> python3 PENZ_project_I.py

or

> python PENZ_project_I.py

depending on the Linux Distro you are running.

There is also a standalone runnable in the folder which can be simply executed in a terminal by:

> ./PENZ_project_I

### Important Notes during the execution:

Further information can be read when the program is running.
