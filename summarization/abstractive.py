def summarize_chunk(chunk, client, language='en'):
    """Summarizes a single chunk of text using the LLM with strict anti-hallucination prompts."""
    
    lang_instruction = "Réponds en Français." if language == 'fr' else "Answer in English."
    
    prompt = f"""
    You are a precise summarization assistant.
    Task: Summarize the following text concisely.
    Rules:
    1. {lang_instruction}
    2. Do NOT invent information. Only use facts from the text.
    3. If the text is technical, keep the technical terms.
    
    Text to summarize:
    {chunk}
    """
    return client.generate_content(prompt)

def hierarchical_summarization(chunks, client, language='en'):
    """Performs hierarchical summarization (Map/Reduce)."""
    chunk_summaries = []
    import time
    for i, chunk in enumerate(chunks):
        # Add delay to respect rate limits (15 RPM usually for free tier = 1 req every 4s)
        if i > 0:
            time.sleep(4)
        summary = summarize_chunk(chunk, client, language)
        chunk_summaries.append(summary)
    
    # Combine chunk summaries
    combined_summary = "\n".join(chunk_summaries)
    
    if len(chunk_summaries) > 1:
        lang_instruction = "Réponds en Français." if language == 'fr' else "Answer in English."
        
        final_prompt = f"""
        You are an expert editor.
        Task: Create a final, coherent summary from the following notes.
        Rules:
        1. {lang_instruction}
        2. The output must be fluid and easy to read.
        3. Do NOT add outside information.
        4. Structure the summary with clear paragraphs.
        
        Notes:
        {combined_summary}
        """
        return client.generate_content(final_prompt)
    else:
        return combined_summary
