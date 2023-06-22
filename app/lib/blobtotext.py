import PyPDF2
import io
import docx
import base64

def blobtotxt(blob, fileType):
    bytes_content = base64.b64decode(blob)
    doc1 = ""
    if fileType == "pdf":
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(bytes_content))
        for i in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(i)
            doc1 += page.extractText()
    elif fileType == "txt":
        with io.BytesIO(bytes_content.decode('utf-8')) as file:
            doc1 = file.read()
    elif fileType == "docx" or fileType == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        docx1 = docx.Document(io.BytesIO(bytes_content))
        doc1 = '\n'.join([paragraph.text for paragraph in docx1.paragraphs])
    print(fileType)
    return doc1