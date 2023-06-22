import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_documents(files, extrafiles):
    preprocessed_content = preprocess(files)
    try:
        tfidf = TfidfVectorizer().fit_transform([preprocessed_content] + list(extrafiles.values()))
    except Exception as e:
        print(e)
        return False
    similarity_scores = cosine_similarity(tfidf)[0][1:]
    similar_documents = sorted(zip(extrafiles.keys(), similarity_scores), key=lambda x: x[1], reverse=True)
    print("Similar Documents:")
    print(similar_documents)
    for i in range(len(similar_documents)):
        lameresult = lamecheck(files, extrafiles[similar_documents[i][0]])
        if lameresult > similarity_scores[i]:
            print(similar_documents)
            similar_documents[i] = (similar_documents[i][0], lameresult)
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

def lamecheck(text1, text2):
    if text1 == text2:
        return 1
    else:
        return 0