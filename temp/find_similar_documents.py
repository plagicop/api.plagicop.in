from database import Database as DocumentDatabase
from preprocess import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_documents(threshold):
    db = DocumentDatabase()

    document_name = input("Enter the name of the document to find similar documents for: ")

    while True:
        try:
            num_similar = int(input("Enter the number of most similar documents to display: "))
            if num_similar < 1:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    document_content = db.get_document(document_name)
    preprocessed_content = preprocess(document_content)

    other_documents = {}
    for name, _, content in db.get_all_documents():
        print(content)
        if name != document_name:
            other_documents[name] = preprocess(content)

    tfidf = TfidfVectorizer().fit_transform([preprocessed_content] + list(other_documents.values()))
    similarity_scores = cosine_similarity(tfidf)[0][1:]

    similar_documents = sorted(zip(other_documents.keys(), similarity_scores), key=lambda x: x[1], reverse=True)[:num_similar]
    for name, score in similar_documents:
        print(f"{name} ({score:.2f})")