import textwrap
from functions.get_files_info import get_files_info

def indent_result(result):
    return textwrap.indent(result, '  ')

print("Result for current directory:")
indented_result = indent_result(get_files_info("calculator", "."))
print(indented_result)

print("Result for 'pkg' directory:")
indented_result = indent_result(get_files_info("calculator", "pkg"))
print(indented_result)

print("Result for '/bin' directory:")
indented_result = indent_result(get_files_info("calculator", "/bin"))
print(indented_result)

print("Result for '../' directory:")
indented_result = indent_result(get_files_info("calculator", "../"))
print(indented_result)