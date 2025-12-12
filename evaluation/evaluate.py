import os
import sys
import time
import argparse
import psutil
from rouge_score import rouge_scorer

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_processing.extract_text import extract_text_pymupdf
from pdf_processing.clean_text import clean_text
from pdf_processing.chunking import chunk_text
from summarization.extractive import extractive_summary
from summarization.abstractive import hierarchical_summarization
from summarization.hybrid import merge_summaries, final_cleanup
from models.llm_client import GeminiClient
from utils.language import detect_language

def calculate_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB

def evaluate_summary(file_path, reference_summary=None, summary_type='hybrid'):
    print(f"--- Starting Evaluation for {file_path} ---")
    print(f"Type: {summary_type}")
    
    start_time = time.time()
    start_memory = calculate_memory_usage()
    
    # 1. Pipeline Execution
    try:
        # Extract
        text = extract_text_pymupdf(file_path)
        original_length = len(text)
        
        # Clean
        cleaned_text = clean_text(text)
        
        # Detect Language
        language = detect_language(cleaned_text)
        
        # Chunk
        chunks = chunk_text(cleaned_text, max_tokens=1000)
        
        # Generate Summary
        final_summary = ""
        client = GeminiClient()
        
        if summary_type == "extractive":
            final_summary = extractive_summary(cleaned_text, language=language)
        elif summary_type == "abstractive":
            final_summary = hierarchical_summarization(chunks, client, language=language)
        elif summary_type == "hybrid":
            ext = extractive_summary(cleaned_text, language=language)
            abst = hierarchical_summarization(chunks, client, language=language)
            final_summary = merge_summaries(ext, abst, client, language=language)
            final_summary = final_cleanup(final_summary)
            
        end_time = time.time()
        end_memory = calculate_memory_usage()
        
        summary_length = len(final_summary)
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        compression_ratio = summary_length / original_length if original_length > 0 else 0
        
        print("\n--- Performance Metrics ---")
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Memory Usage Increase: {memory_used:.2f} MB")
        print(f"Original Length: {original_length} chars")
        print(f"Summary Length: {summary_length} chars")
        print(f"Compression Ratio: {compression_ratio:.2%}")
        
        if reference_summary:
            print("\n--- Quality Metrics (ROUGE) ---")
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
            scores = scorer.score(reference_summary, final_summary)
            
            for key, score in scores.items():
                print(f"{key}: Precision={score.precision:.4f}, Recall={score.recall:.4f}, F1={score.fmeasure:.4f}")
        
        return final_summary
        
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Summarization Pipeline")
    parser.add_argument("--file", required=True, help="Path to PDF file")
    parser.add_argument("--ref", help="Reference summary text (optional) or path to text file")
    parser.add_argument("--type", default="hybrid", choices=['extractive', 'abstractive', 'hybrid'], help="Type of summary")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.")
        sys.exit(1)
        
    reference = None
    if args.ref:
        if os.path.exists(args.ref):
             with open(args.ref, 'r', encoding='utf-8') as f:
                 reference = f.read()
        else:
            reference = args.ref
            
    extract_folder = os.path.dirname(os.path.abspath(__file__))
    # Ensure intermediate directories if needed, though usually evaluating existing files
    
    print(f"Evaluating: {args.file}...")
    evaluate_summary(args.file, reference, args.type)
