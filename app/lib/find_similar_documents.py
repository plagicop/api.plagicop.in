import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_documents(files, extrafiles):
    preprocessed_content = preprocess(files)
    tfidf = TfidfVectorizer().fit_transform([preprocessed_content] + list(extrafiles.values()))
    similarity_scores = cosine_similarity(tfidf)[0][1:]
    similar_documents = sorted(zip(extrafiles.keys(), similarity_scores), key=lambda x: x[1], reverse=True)
    print(similar_documents)
    return similar_documents

def preprocess(text):
    text = text.lower()

    text = re.sub(r'[^a-z]', ' ', text)

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    text = ' '.join(tokens)

    return text
