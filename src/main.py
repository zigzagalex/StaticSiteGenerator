import shutil
import os
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
    path_static = "/Users/alexeyzagorulko/PycharmProjects/StaticSiteGenerator/static"
    path_public = "/Users/alexeyzagorulko/PycharmProjects/StaticSiteGenerator/public"
    path_template = "/Users/alexeyzagorulko/PycharmProjects/StaticSiteGenerator/template.html"
    content_path = "/Users/alexeyzagorulko/PycharmProjects/StaticSiteGenerator/content"
    copy_static_files(path_static, path_public)
    if os.path.isfile(content_path):
        generate_page(content_path, path_template, path_public)
    else:
        generate_pages_recursive(content_path, path_template, path_public)
