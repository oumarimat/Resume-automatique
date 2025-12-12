import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_processing.extract_text import extract_text_pymupdf
from pdf_processing.clean_text import clean_text
from pdf_processing.chunking import chunk_text
from summarization.extractive import extractive_summary
from summarization.abstractive import hierarchical_summarization
from summarization.hybrid import merge_summaries, final_cleanup
from models.llm_client import GeminiClient
from utils.language import detect_language

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            summary_type = request.form.get('summary_type', 'hybrid')
            chunk_size = int(request.form.get('chunk_size', 1000))
            
            # 1. Extract
            text = extract_text_pymupdf(filepath)
            
            # 2. Clean
            cleaned_text = clean_text(text)
            
            # 3. Detect Language
            language = detect_language(cleaned_text)
            
            # 4. Chunk
            chunks = chunk_text(cleaned_text, max_tokens=chunk_size)
            
            # Initialize Client
            client = GeminiClient()
            
            final_summary = ""
            
            if summary_type == "extractive":
                final_summary = extractive_summary(cleaned_text, language=language)
            elif summary_type == "abstractive":
                final_summary = hierarchical_summarization(chunks, client, language=language)
            elif summary_type == "hybrid":
                ext = extractive_summary(cleaned_text, language=language)
                abst = hierarchical_summarization(chunks, client, language=language)
                final_summary = merge_summaries(ext, abst, client, language=language)
                final_summary = final_cleanup(final_summary)
            
            # Cleanup
            os.remove(filepath)
            
            return jsonify({
                'summary': final_summary,
                'language': language
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
