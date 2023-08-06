from os.path import join, relpath, isfile, isdir
from os import walk
from fnmatch import fnmatch
from typing import Iterable, Optional
from PIL import Image

from .class_diagram import render_namespaces, merge_similar_namespaces
from .csharp_analyser import extract_namespaces

def is_file_included(filename: str, included: list[str], excluded: list[str]) -> bool:
    if not any(fnmatch(filename, pattern) for pattern in included):
        return False

    if any(fnmatch(filename, pattern) for pattern in excluded):
        return False

    return True

def list_files(folder_path: str, included: list[str], excluded: list[str]) -> Iterable[str]:
    for (root, _, files) in walk(folder_path, topdown=True):
        for name in files:
            full_path = join(root, name)
            if is_file_included(relpath(full_path, folder_path), included, excluded):
                yield full_path

def render_from_paths(*paths: str, font_file: str, font_size: int) -> Optional[Image.Image]:
    included_files = ["*.cs"]
    excluded_files = ["*.designer.cs", "**/obj/**", "obj/**", "**/bin/**", "bin/**", "Properties/**", "**/Properties/**", "**/AssemblyInfo.cs"]
    namespaces = []

    for path in paths:
        if isfile(path):
            if is_file_included(path, included_files, excluded_files):
                for diagram in extract_namespaces(path):
                    namespaces.append(diagram)
        elif isdir(path):
            for filename in list_files(path, included_files, excluded_files):
                for diagram in extract_namespaces(filename):
                    namespaces.append(diagram)


    merge_similar_namespaces(namespaces)

    if len(namespaces) > 0:
        return render_namespaces(namespaces, font_file, font_size)
    else:
        return None
