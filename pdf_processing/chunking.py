import nltk

# Ensure nltk data is downloaded (can be moved to a setup script)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def chunk_text(text, max_tokens=1000):
    """Chunks text into segments of approximately max_tokens."""
    sentences = nltk.tokenize.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        # Rough estimation of tokens (words)
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def split_by_sections(text):
    """Splits text by double newlines or other section markers."""
    # Basic implementation assuming double newlines separate sections
    return text.split('\n\n')
