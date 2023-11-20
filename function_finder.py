import os
import ast
from utils import get_git_root, find_function_definitions

class FunctionCallFinder:
    def __init__(self, changed_file_path, function_name):
        self.folder_path = get_git_root(changed_file_path)
        self.changed_file_path = changed_file_path
        self.function_name = function_name
        self.parent_function_name = None

    def _find_affected_files(self, affected_files):

        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    parent_function = self._function_called_in_file(file_path)
                    old1 = self.changed_file_path
                    old2 = self.function_name
                    if parent_function is not None:
                        if file_path not in affected_files:
                            affected_files.append(file_path)
                            self.changed_file_path = file_path
                            self.function_name = parent_function
                            self._find_affected_files(affected_files)
                    self.changed_file_path = old1
                    self.function_name = old2
        
        return affected_files

    def _function_called_in_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            try:
                tree = ast.parse(code)
            except SyntaxError:
                # If file itself is wrong return False by default
                return False

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.parent_function_name = node.name
                    if self.parent_function_name == self.function_name:
                        # Skip the function definition itself
                        continue

                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == self.function_name:
                        return self.parent_function_name

        return None

    def get_affected_files(self):
        all_file_functions = find_function_definitions(self.changed_file_path)

        if self.function_name in all_file_functions:
            affected_files = []
            affected_files = self._find_affected_files(affected_files)

            print("Affected files:")
            print('\n'.join(affected_files))
        else:
            print(f"The function '{self.function_name}' is not defined in '{self.changed_file_path}'")


if __name__ == '__main__':
    changed_file = r'C:\Users\rafal.michalkevic\Documents\trainings\regression_analysis_tool\test\someutils.py'
    function_name = 'call_this_func'

    FunctionCallFinder(changed_file, function_name).get_affected_files()
    