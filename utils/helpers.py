import os

def save_text(text, filepath):
    """Saves text to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def load_text(filepath):
    """Loads text from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()