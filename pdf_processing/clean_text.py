import re

def remove_headers_footers(text):
    """Removes potential headers and footers based on common patterns."""
    # This is a heuristic approach and might need tuning based on specific PDF layouts
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Example: Remove lines that look like page numbers or very short header/footer text
        if len(line.strip()) < 4 and line.strip().isdigit():
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def normalize_whitespace(text):
    """Replaces multiple spaces/newlines with single ones."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def remove_page_numbers(text):
    """Removes standalone page numbers."""
    # Regex to find standalone numbers at start or end of lines could be added here
    # For now, relying on remove_headers_footers logic
    return text

def clean_text(text):
    """Applies all cleaning functions."""
    text = remove_headers_footers(text)
    text = normalize_whitespace(text)
    return text