import os
import ast
from git_parser import GitParser

class FunctionNameFinder:
    def __init__(self, file_path):
        self.file_path = file_path

    def find_function_definitions(self):
        with open(self.file_path, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            function_names = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)
            return function_names

class FunctionCallFinder:
    def __init__(self, changed_file_path, function_name):
        self.folder_path = GitParser.get_git_root(changed_file_path)
        self.changed_file_path = changed_file_path
        self.function_name = function_name

    def _find_affected_files(self):
        affected_files = []

        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        if self.function_name in code:
                            affected_files.append(file_path)

        return affected_files
    
    def get_affected_files(self):
        all_file_functions = FunctionNameFinder(self.changed_file_path).find_function_definitions()

        if self.function_name in all_file_functions:
            affected_files = self._find_affected_files()

            print(affected_files)
        else:
            print(f"The function '{self.function_name}' is not defined in '{self.changed_file_path}'")


if __name__ == '__main__':
    changed_file = 'C:\\Users\\rafal.michalkevic\\Documents\\alcotest_things\\systemtest_impairmentchecks\\device\\a7000\\A7000SerialEnumerator.py'
    function_name = 'GetDraegerDevices'

    FunctionCallFinder(changed_file, function_name).get_affected_files()

    