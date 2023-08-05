import os
import glob
import pprint


def hlp_source_under(folder):
    """
    this function finds all the python packages under a folder and
    write the 'packages' and 'package_dir' entries for a python setup.py
    script
    """
    # walk the folder and find the __init__.py entries for packages.
    packages = []
    package_dir = {}
    for root, _, files in os.walk(folder):
        for file in files:
            if file != '__init__.py':
                continue
            full = os.path.dirname(os.path.join(root, file))
            relative = os.path.relpath(full, folder)
            packages.append(relative)
            package_dir[relative] = full
    # we use pprint because we want the order to always remain the same
    return f"packages={sorted(packages)},\npackage_dir={pprint.pformat(package_dir)}"


def hlp_files_under(destination_folder, pat):
    file_list = [x for x in glob.glob(pat) if os.path.isfile(x)]
    return f"('{destination_folder}', {file_list})"


def make_hlp_project_keywords(d):
    def hlp_project_keywords():
        return f"{d.project_keywords.split()}"

    return hlp_project_keywords


def make_hlp_project_platforms(d):
    def hlp_project_platforms():
        return f"{d.project_platforms.split()}"

    return hlp_project_platforms


def make_hlp_project_classifiers(d):
    def hlp_project_classifiers():
        classifiers = d.project_classifiers.split('\n')
        classifiers = [x.strip()[1:-1] for x in classifiers]
        return f"{classifiers}"

    return hlp_project_classifiers


def make_hlp_wrap(level):
    def hlp_wrap(t):
        return t.replace('\n', '\n' + '\t' * level)

    return hlp_wrap
