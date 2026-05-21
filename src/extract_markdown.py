import re

def extract_markdown_images(input_text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",
                         input_text)
    return matches

def extract_markdown_links(input_text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",
                         input_text)
    return matches
