import sqlite3
import hashlib

class Database:
    def __init__(self, db_file='documents.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS documents
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      file_path TEXT NOT NULL UNIQUE,
                      content_hash TEXT NOT NULL,
                      content TEXT NOT NULL)''')
        self.conn.commit()

    def add_document(self, file_path, content):
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO documents (file_path, content_hash, content) VALUES (?, ?, ?)", (file_path, content_hash, content))
            self.conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError:
            # The document already exists in the database
            return None

    def get_all_documents(self):
        c = self.conn.cursor()
        c.execute("SELECT file_path, id, content FROM documents")
        return c.fetchall()

    def get_document(self, document_name):
        c = self.conn.cursor()
        c.execute("SELECT content FROM documents WHERE file_path=?", (document_name,))
        return c.fetchone()[0]
    
    def get_document_content(self, document_id):
        c = self.conn.cursor()
        c.execute("SELECT content FROM documents WHERE id=?", (document_id,))
        return c.fetchone()[0]

    def get_similar_documents(self, content, threshold):
        c = self.conn.cursor()
        c.execute("SELECT id, file_path FROM documents")
        documents = c.fetchall()
        similar_documents = []
        for doc_id, file_path in documents:
            doc_content = self.get_document_content(doc_id)
            similarity = self.calculate_similarity(content, doc_content)
            if similarity >= threshold:
                similar_documents.append(file_path)
        return similar_documents

    def calculate_similarity(self, text1, text2):
        # This method should be implemented in a separate file/module
        pass