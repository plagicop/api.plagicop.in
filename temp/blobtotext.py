import PyPDF2
import io
import docx

def blobtotxt(blob, fileType):
    doc1 = ""
    if fileType == "pdf":
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(blob))
        for i in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(i)
            doc1 += page.extractText()
    elif fileType == "txt":
        with io.BytesIO(blob) as file:
            doc1 = file.read()
    elif fileType == "docx":
        docx1 = docx.Document(io.BytesIO(blob))
        doc1 = '\n'.join([paragraph.text for paragraph in docx1.paragraphs])
    return doc1