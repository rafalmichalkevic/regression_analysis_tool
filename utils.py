import git
import ast

def get_git_root(path):
        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        return git_root

def find_function_definitions(file_path):
        with open(file_path, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            function_names = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)
            return function_names