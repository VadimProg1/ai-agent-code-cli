from functions.run_python_file import run_python_file

def print_separator():
    print("-------------------------------------------------------------")

print(run_python_file("calculator", "main.py"))
print_separator()
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print_separator()
print(run_python_file("calculator", "tests.py"))
print_separator()
print(run_python_file("calculator", "../main.py"))
print_separator()
print(run_python_file("calculator", "nonexistent.py"))
print_separator()
print(run_python_file("calculator", "lorem.txt"))
