import shutil
import os
import sys
from pathlib import Path

from generate import generate_page, generate_pages_recursive

def recursive_copy(current_src: str, current_dest: str):
    for item in os.listdir(current_src):
        src_path = os.path.join(current_src, item)
        dest_path = os.path.join(current_dest, item)
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            recursive_copy(src_path, dest_path)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied file: {src_path} → {dest_path}")
def copy_static_files(src: str, dest: str):
    # 1. Remove the destination directory if it exists
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted existing directory: {dest}")

    # 2. Recreate the empty destination directory
    os.makedirs(dest)
    print(f"Created new directory: {dest}")

    return recursive_copy(src, dest)


if __name__ == '__main__':
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.endswith("/"):
        basepath += "/"

    print(basepath)
    project_root = Path(__file__).parent.parent

    dest_path = project_root / "docs"
    static_dir = project_root / "static"
    from_path = project_root / "content"
    template_path = project_root / "template.html"

    path_static = "static"
    path_public = "public"
    path_template = "/Users/alexeyzagorulko/PycharmProjects/StaticSiteGenerator/template.html"
    content_path = "/Users/alexeyzagorulko/PycharmProjects/StaticSiteGenerator/content"
    copy_static_files(str(static_dir), str(dest_path))
    if os.path.isfile(from_path):
        generate_page(basepath, from_path, template_path, dest_path)
    else:
        generate_pages_recursive(basepath, from_path, template_path, dest_path)
