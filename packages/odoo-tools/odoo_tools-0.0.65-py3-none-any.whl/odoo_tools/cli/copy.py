from __future__ import print_function
from odoo_tools.compat import Path


def recursive_copy(source, destination, blacklist=None):
    if blacklist is None:
        blacklist = []

    path_to_create = []
    file_to_copy = []

    for path in source.iterdir():
        if path.name in blacklist:
            continue

        rel_path = path.relative_to(source)
        if path.is_dir():
            path_to_create.append(rel_path)
        else:
            file_to_copy.append(rel_path)

    for directory in path_to_create:
        src_path = source / directory
        dest_path = destination / directory
        dest_path.mkdir(exist_ok=True)
        recursive_copy(
            src_path, dest_path, blacklist=blacklist
        )

    for filename in file_to_copy:
        with (destination / filename).open('w') as fout:
            with (source / filename).open('r') as fin:
                fout.write(fin.read())


source = Path('./a')
dest = Path('./b')

dest.mkdir(exist_ok=True)

recursive_copy(source, dest, ['.git'])
