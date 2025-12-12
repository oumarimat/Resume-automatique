def merge_summaries(extractive, abstractive, client, language='en'):
    """
    Merges extractive and abstractive summaries using the LLM for a true hybrid result.
    """
    lang_instruction = "Réponds en Français." if language == 'fr' else "Answer in English."
    
    prompt = f"""
    You are a professional synthesizer.
    Task: Create a Hybrid Summary by combining 'Key Extracted Points' and an 'Abstractive Overview'.
    
    Rules:
    1. {lang_instruction}
    2. Use the 'Key Extracted Points' to ensure factual accuracy.
    3. Use the 'Abstractive Overview' for flow and context.
    4. The final result must be a single, cohesive text, not two separate parts.
    5. Do NOT invent information.
    
    Key Extracted Points (Factual Base):
    {extractive}
    
    Abstractive Overview (Context):
    {abstractive}
    """
    
    return client.generate_content(prompt)

def final_cleanup(summary):
    """Performs final cleanup on the generated summary."""
    return summary.strip()
