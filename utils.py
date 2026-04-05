# utils.py
import re

def clean_text(text: str) -> str:
    # Strip HTML/XML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse multiple whitespace / newlines
    text = re.sub(r"\s+", " ", text)
    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()
