from langdetect import detect, LangDetectException

def detect_language(text):
    """
    Detects the language of the text.
    Returns 'fr' for French, 'en' for English, or 'en' as default.
    """
    try:
        # Detect language of the first 500 characters to be fast
        lang = detect(text[:500])
        if lang == 'fr':
            return 'fr'
        return 'en'
    except LangDetectException:
        return 'en'
