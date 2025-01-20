from textnode import TextNode
import os
import shutil
import markdown
from inline_markdown import extract_title
from markdown_blocks import markdown_to_html_node

def copy_static_to_public(src, dest):
    # If the destination directory exists, delete it to ensure a clean copy
    if os.path.exists(dest):
        print(f"Deleting existing directory: {dest}")
        shutil.rmtree(dest)
    
    # Recreate the destination directory
    os.mkdir(dest)

    # Loop through all files and subdirectories in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            # If the item is a directory, recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_static_to_public(src_path, dest_path)
        else:
            # If the item is a file, copy it to the destination
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
              

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the Markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()
    html_content = html_content.replace("&lt;em&gt;", "<i>").replace("&lt;/em&gt;", "</i>")
    html_content = html_content.replace("<em>", "<i>").replace("</em>", "</i>")
    # Extract the title from the Markdown
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the generated HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(full_html)
        
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Recursively process all Markdown files in the content directory
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                content_path = os.path.join(root, file)

                # Generate the corresponding public file path
                relative_path = os.path.relpath(content_path, dir_path_content)
                html_output_path = os.path.join(dest_dir_path, relative_path.replace(".md", ".html"))

                # Generate the HTML page
                generate_page(content_path, template_path, html_output_path)



def main():
    # Define directories
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"  # Directory containing Markdown files
    content_file = "content/index.md"
    template_file = "template.html"
    output_file = "public/index.html"

    # Clean the public directory
    if os.path.exists(public_dir):
        print(f"Deleting existing directory: {public_dir}")
        shutil.rmtree(public_dir)

    # Copy static files
    copy_static_to_public(static_dir, public_dir)

    # Generate the index page
    generate_pages_recursive(content_dir, template_file, public_dir)
    print("Site generated successfully!")

if __name__ == "__main__":
    main()
    
    
