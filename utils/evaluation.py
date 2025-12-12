# evaluation.py
# ----------------------------------
# Module pour évaluer les résumés


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rouge_like_score(reference, summary):
"""
Calcul simplifié d'un score similaire à ROUGE basé sur TF-IDF.
"""
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform([reference, summary])
score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
return score