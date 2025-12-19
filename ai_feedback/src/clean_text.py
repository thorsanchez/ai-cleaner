import re

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^[\w\s]", "", text)
    text = re.sub(r"\s+"," ", text)
    return text.strip()
    