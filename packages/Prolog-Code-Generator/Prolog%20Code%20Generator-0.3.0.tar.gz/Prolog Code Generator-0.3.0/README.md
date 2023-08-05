# Prolog Expert system code generator

Library generate prolog code for expert system from CSV file.

## Installation

`pip install -i pip install Prolog-Code-Generator`

## How to use:
- Create csv file like this:  
| Name | param1 | param2 | param3 |
|------- |-------- |-------- |-------- |
| name1 | good | good | good |
| name3 | bad | bad | bad |

- Go on:
```python
import prolog_code_generator as cg
data = cg.get_template(path = "file_path.csv",delimer = ";")
example = cg.CodeGenerator(data="data")
example.csv_to_code(output_path="output/filename")
```
See more in examples.

## Contribution 
If you wanna contribute just create issue with tag [eq. bug, feture].
If you wanna change something in code create your own branch from dev branch and next create pull request to this branch. 
