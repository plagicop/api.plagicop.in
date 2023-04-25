from database import Database
from preprocess import preprocess
from find_similar_documents import find_similar_documents
from blobtotext import blobtotxt
import base64
import os

db = Database()

document_path = input("Enter the path of a document to add to the database: ")

# document_text = blobtotxt(base64.b64encode(open(document_path, "rb").read()).decode("utf-8"), os.path.splitext(document_path)[1])
document_text = open(document_path).read()

document_text = preprocess(document_text)
document_id = db.add_document(document_path, document_text)
print(document_id)
# exit()
print(f"Document {document_path} added to the database with ID {document_id}")

threshold = float(input("Enter a threshold for similarity (0 to 1): "))

similar_documents = find_similar_documents(threshold)

if len(similar_documents) == 0:
    print("No similar7 documents found in the database.")
else:
    print("Similar documents found in the database:")
    for doc in similar_documents:
        print(doc) 
