import re


def extract_tags(text: str):
    return re.findall(r"#(\w+)", text)
