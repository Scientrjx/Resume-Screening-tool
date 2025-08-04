from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_texts, job_description):
    documents = resume_texts + [job_description]
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform(documents)
    similarity_scores = cosine_similarity(vectors[:-1], vectors[-1:])
    return similarity_scores.flatten()