from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def cosine_similarity_files(doc1, doc2):
    with open(doc1, 'r') as f:
        doc1_text = f.read()
    with open(doc2, 'r') as f:
        doc2_text = f.read()

    doc1_tokens = word_tokenize(doc1_text)
    doc1_tokens = [word.lower() for word in doc1_tokens if word.isalpha() and word.lower() not in stop_words]
    doc2_tokens = word_tokenize(doc2_text)
    doc2_tokens = [word.lower() for word in doc2_tokens if word.isalpha() and word.lower() not in stop_words]

    vectorizer = TfidfVectorizer(tokenizer=lambda text: text, preprocessor=lambda text: text)

    tfidf = vectorizer.fit_transform([doc1_tokens, doc2_tokens])

    similarity = cosine_similarity(tfidf)[0][1]

    return similarity

@app.route('/similarity', methods=['POST'])
def get_similarity():
    document1_file_path = request.form['document1']
    document2_file_path = request.form['document2']

    similarity = cosine_similarity_files(document1_file_path, document2_file_path)

    threshold = 0.8

    if similarity > threshold:
        message = "The two documents are similar."
    else:
        message = "The two documents are not similar."
    
    response = {'similarity_score': similarity, 'message': message}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)