import sys
import ast
import os
import collections
from nltk import pos_tag

PROJECTS = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]


def get_all_projects(addon_projects):
    all_projects = []
    for project in addon_projects:
        if project.lower() not in PROJECTS:
            all_projects.append(project.lower())
    return all_projects+PROJECTS


def get_existing_projects(all_projects):
    existing_projects = []
    for project in all_projects:
        dirpath = os.path.join('.', project)
        if os.path.exists(dirpath):
            existing_projects.append(dirpath)
    return existing_projects


def get_filepaths(dirpath):
    filepaths = []
    for root, dirs, files in os.walk(dirpath, topdown=True):
        python_files_list = [f for f in files if f.endswith(".py")]
        for file in python_files_list:
            filepaths.append(os.path.join(root, file))
    return filepaths


def get_file_content_list(filepaths):
    files_content_list = []
    for filename in filepaths:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
            files_content_list.append(main_file_content)
    return files_content_list


def get_trees(files_content_list):
    trees = []
    for file_content in files_content_list:
        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            tree = None
        trees.append(tree)
    return trees


def get_func_names(trees):
    func_names_list = []
    for tree in trees:
        func_name = [node.name.lower() for node in ast.walk(tree)
                     if isinstance(node, ast.FunctionDef)]
        func_names_list.append(func_name)
    return func_names_list


def filtering_funcs(func_names_list):
    clear_funcs_list = [f for f in func_names_list
                        if not (f.startswith('__') and f.endswith('__'))]
    return clear_funcs_list


def verb_check(word):
    pos_info = pos_tag([word])
    word_type = pos_info[0][1]
    return word_type == 'VB'


def get_verbs(verbs):
    return collections.Counter(verbs)


if __name__ == '__main__':
    addon_projects = sys.argv[1:]
    all_projects = get_all_projects(addon_projects)
    top_verbs = []
    existing_projects = get_existing_projects(all_projects)
    for project in existing_projects:
        print('dirpath: {dirpath}:'.format(dirpath=project))
        filepaths = get_filepaths(project)
        print('total ".py" files count: {count}'.format(count=len(filepaths)))
        files_content_list = get_file_content_list(filepaths)
        trees = get_trees(files_content_list)
        print('trees generated')
        func_names = get_func_names(trees)
        clear_func_names_list = filtering_funcs(sum(func_names, []))
        print('functions extracted')
        verbs = []
        for function_name in clear_func_names_list:
            verbs.append([word for word in function_name.split('_')
                          if verb_check(word)])
        verbs_counter = get_verbs(sum(verbs, []))
        for verb in verbs_counter:
            print('verb "{verb}" count: {count}'.format(
                verb=verb, count=verbs_counter[verb]))
        top_verbs += verbs_counter
        print('\n')

    print('total {words} words, unique {unique}'.format(
        words=len(top_verbs), unique=len(set(top_verbs))))
    for word, occurence in collections.Counter(
            top_verbs).most_common():
        print('"{verb}" in {occurence} projects'.format(verb=word,
                                                        occurence=occurence))
