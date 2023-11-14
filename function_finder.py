import os
from utils import get_git_root, find_function_definitions


class FunctionCallFinder:
    def __init__(self, changed_file_path, function_name):
        self.folder_path = get_git_root(changed_file_path)
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
        all_file_functions = find_function_definitions(self.changed_file_path)

        if self.function_name in all_file_functions:
            affected_files = self._find_affected_files()

            print(affected_files)
        else:
            print(f"The function '{self.function_name}' is not defined in '{self.changed_file_path}'")


if __name__ == '__main__':
    changed_file = 'C:\\Users\\rafal.michalkevic\\Documents\\alcotest_things\\systemtest_impairmentchecks\\device\\a7000\\A7000SerialEnumerator.py'
    function_name = 'GetDraegerDevices'

    FunctionCallFinder(changed_file, function_name).get_affected_files()

    