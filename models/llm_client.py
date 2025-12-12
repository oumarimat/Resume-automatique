import google.generativeai as genai
import os

class GeminiClient:
    def __init__(self, api_key=None):
        # Use provided key, then env var, then fallback (not recommended)
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("No Google API Key found. Please set the GOOGLE_API_KEY environment variable.")
        
        # Debug: Print the key being used (masked)
        masked_key = self.api_key[:5] + "..." + self.api_key[-5:]
        print(f"--> [DEBUG] Using Google API Key: {masked_key}")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_content(self, prompt):
        import time
        max_retries = 5
        base_delay = 10
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        sleep_time = base_delay * (2 ** attempt)
                        print(f"Quota exceeded (429). Retrying in {sleep_time}s... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(sleep_time)
                        continue
                return f"Error generating content: {e}"
        return "Error: Failed to generate content after multiple retries."
