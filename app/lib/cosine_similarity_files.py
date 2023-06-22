import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))

def cosine_similarity_files(doc1_text, doc2_text):
    
    doc1_tokens = word_tokenize(doc1_text)
    doc1_tokens = [word.lower() for word in doc1_tokens if word.isalpha() and word.lower() not in stop_words]
    doc2_tokens = word_tokenize(doc2_text)
    doc2_tokens = [word.lower() for word in doc2_tokens if word.isalpha() and word.lower() not in stop_words]

    vectorizer = TfidfVectorizer(tokenizer=lambda text: text, preprocessor=lambda text: text)

    tfidf = vectorizer.fit_transform([doc1_tokens, doc2_tokens])

    similarity = cosine_similarity(tfidf)[0][1]

    return similarity