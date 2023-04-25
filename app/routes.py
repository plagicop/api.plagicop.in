from flask import request, jsonify
from app.lib.cosine_similarity_files import cosine_similarity_files
from app.lib.blobtotext import blobtotxt
from app.lib.find_similar_documents import find_similar_documents
import base64
import json

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

@app.route('/multisimilarity', methods=['POST'])
def multisimilarity():
    data = request.json
    # print(data)
    # return "ok"
    nooffiles = int(data['noofdocs'])
    textfiles = {}
    for i in range(nooffiles):
        textfiles[data[f'doc{i}']['name']] = blobtotxt(data[f'doc{i}']['base64'], data[f'doc{i}']['type'])
    print(textfiles.keys())
    similarity = []
    for i in textfiles.keys():
        extrafiles = dict(textfiles)
        extrafiles.pop(i)
        for ii in find_similar_documents(textfiles[i], extrafiles):
            result = {}
            result['file1'] = i
            result['file2'] = ii[0]
            result['similarity'] = ii[1]
            similarity.append(result)
        # similarity.append(find_similar_documents(textfiles[i], textfiles[:i]+textfiles[i+1:]))
    print(similarity)
    return jsonify({
        "data": similarity
    })
