import shutil
from transform import markdown_to_html_node
import os

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if line.strip().startswith("# "):  # H1 only
            return line.strip()[2:].strip()
    raise Exception("No H1 header (#) found in the markdown.")


def apply_template(template: str, title: str, content: str) -> str:
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", content)
    return result


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    result = apply_template(template, title, html_content)
    os.makedirs(dest_path, exist_ok=True)
    with open(os.path.join(dest_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(result)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        # If someone accidentally passes a file as the starting path — reject it early
        raise ValueError(f"Expected a directory, got a file: {dir_path_content}")

    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(source_path):
            dest_subdir = os.path.join(dest_dir_path, entry)
            os.makedirs(dest_subdir, exist_ok=True)
            print(f"Entering directory: {source_path}")
            generate_pages_recursive(source_path, template_path, dest_subdir)

        elif os.path.isfile(source_path) and entry.endswith(".md"):
            page_name = os.path.splitext(entry)[0]
            if page_name == "index":
                # Write to the directory directly
                page_output_dir = dest_dir_path
            else:
                # Create subdirectory for this page
                page_output_dir = os.path.join(dest_dir_path, page_name)
                os.makedirs(page_output_dir, exist_ok=True)

            generate_page(source_path, template_path, page_output_dir)

            print(f"Generated page from {source_path} → {page_output_dir}/index.html")

