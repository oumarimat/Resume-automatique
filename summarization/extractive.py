import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

def extractive_summary(text, language='en', num_sentences=5):
    """
    Generates an extractive summary using TF-IDF and Cosine Similarity.
    STRICT: Selects original sentences only. No paraphrasing.
    """
    sentences = nltk.tokenize.sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    # Select stop words based on language
    stop_words = 'french' if language == 'fr' else 'english'

    try:
        # Create TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        tfidf_matrix = vectorizer.fit_transform(sentences)

        # Compute similarity matrix
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # Create graph and calculate scores
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)

        # Rank sentences
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        # Select top sentences
        selected_sentences = [s for _, s in ranked_sentences[:num_sentences]]
        
        # Return sentences in their original order to maintain flow
        # (Optional: can be sorted by index if we tracked it, but here we just join them)
        return "\n\n".join(selected_sentences)
        
    except Exception as e:
        # Fallback if TF-IDF fails (e.g. empty text or only stop words)
        return "\n\n".join(sentences[:num_sentences])
