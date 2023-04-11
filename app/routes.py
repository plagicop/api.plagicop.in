from flask import request, jsonify
from app.lib.cosine_similarity_files import cosine_similarity_files
from app.lib.blobtotxt import blobtotxt
import base64

from app import app

@app.route('/health')
def health():
    return "OK"

@app.route('/similarity', methods=['POST'])
def get_similarity():
    data = request.json
    if data['isdoc1blob'] == True:
        doc1blob = data['doc1blob']
        print(doc1blob)
        doc1blob = bytes(base64.b64decode(doc1blob))
        doc1 = blobtotxt(doc1blob, data['doc1fileType'])
    else:
        doc1 = data['doc1']
    if data['isdoc2blob'] == True:
        doc2blob = data['doc2blob']
        print(doc2blob)
        doc2blob = bytes(base64.b64decode(doc2blob))
        doc2 = blobtotxt(doc2blob, data['doc2fileType'])
    else:
        doc2 = data['doc2']
    similarity = cosine_similarity_files(str(doc1), str(doc2))

    threshold = 0.8

    if similarity > threshold:
        message = "The two documents are similar."
    else:
        message = "The two documents are not similar."
    
    response = {'similarity_score': similarity, 'message': message}
    print(response)
    # response = {'similarity_score': 0.99*100, 'message': "pl"}

    return jsonify(response)