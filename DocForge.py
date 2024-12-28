import os
import ast
import time

VERSION = "0.1.2-beta"

def ParsePythonCode(file_path):
    """
    Parse a Python file and extract functions, classes, and their docstrings.

    :param file_path: Path to the Python file.
    :return: Dictionary with parsed data.
    """
    with open(file_path, 'r') as f:
        code = f.read()

    tree = ast.parse(code)

    parsed_data = {
        "functions": [],
        "classes": []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            parsed_data["functions"].append({
                "name": node.name,
                "doc": ast.get_docstring(node)
            })
        elif isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "doc": ast.get_docstring(node),
                "methods": []
            }
            for sub_node in node.body:
                if isinstance(sub_node, ast.FunctionDef):
                    class_info["methods"].append({
                        "name": sub_node.name,
                        "doc": ast.get_docstring(sub_node)
                    })
            parsed_data["classes"].append(class_info)

    return parsed_data

def GetLastModifiedDate(file_path):
    """
    Get the last modification date of the file.

    :param file_path: Path to the file.
    :return: Last modification date as a string.
    """
    timestamp = os.path.getmtime(file_path)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def GenerateMarkdown(parsed_data, input_file):
    """
    Generate a Markdown string from parsed data.

    :param parsed_data: Dictionary with parsed data.
    :param input_file: The Python file path to get last modified date.
    :return: Markdown string.
    """
    markdown = "# Documentation\n\n"

    # Add functions
    if parsed_data["functions"]:
        markdown += "## Functions\n\n"
        for func in parsed_data["functions"]:
            markdown += f"### {func['name']}\n"
            markdown += f"{func['doc'] or 'No documentation available.'}\n\n"

    # Add classes
    if parsed_data["classes"]:
        markdown += "## Classes\n\n"
        for cls in parsed_data["classes"]:
            markdown += f"### {cls['name']}\n"
            markdown += f"{cls['doc'] or 'No documentation available.'}\n\n"
            if cls["methods"]:
                markdown += "#### Methods\n"
                for method in cls["methods"]:
                    markdown += f"- **{method['name']}**: {method['doc'] or 'No documentation available.'}\n"
                markdown += "\n"
    
    # Add credits section
    last_modified = GetLastModifiedDate(input_file)
    markdown += "\n## Credits\n"
    markdown += "This README was generated using **DocForge** (created by Tristan-BS).\n"
    markdown += f"DocForge version: {VERSION}\n"
    markdown += f"Last modified on: {last_modified}\n"

    return markdown

def SaveMarkDown(output_path, markdown):
    """
    Save the generated Markdown to a file.

    :param output_path: Path to save the Markdown file.
    :param markdown: The Markdown string.
    """
    with open(output_path, 'w') as f:
        f.write(markdown)

if __name__ == "__main__":
    Input_File = "Template.py"
    Output_File = "Generated_Readmes/README.md"

    if not os.path.exists(Input_File):
        print(f"Error: {Input_File} not found")
        sys.exit(1)

    Parsed_Data = ParsePythonCode(Input_File)
    Markdown_Content = GenerateMarkdown(Parsed_Data, Input_File)

    SaveMarkDown(Output_File, Markdown_Content)
    print(f"Markdown file generated: {Output_File}")
