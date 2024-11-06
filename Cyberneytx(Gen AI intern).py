#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install fastapi uvicorn chromadb sentence-transformers PyPDF2 python-docx python-docx2txt aiofiles


# In[ ]:


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
import chromadb
import os
import PyPDF2
import docx2txt

app = FastAPI()

# Initialize ChromaDB client and collection
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("documents")

# Load the sentence transformer model
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def process_file(file_path: str):
    ext = os.path.splitext(GenerativeAIandMentalHealth)[1].lower()
    text = ""
    
    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join([page.extract_text() for page in reader.pages])
    elif ext in ['.doc', '.docx']:
        text = docx2txt.process(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    return text

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a document and store its embeddings."""
    file_location = f"./temp/{file.filename}"
    
    # Save the uploaded file temporarily
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    
    # Process the file to extract text
    text = process_file(file_location)
    
    # Generate embeddings for the extracted text
    embeddings = embed_model.encode(text).tolist()
    
    # Store the embeddings in ChromaDB
    collection.add(documents=[text], embeddings=[embeddings], metadatas=[{"filename": file.filename}])
    
    # Clean up temporary file
    os.remove(file_location)
    
    return JSONResponse(content={"message": "File uploaded and processed successfully."})

@app.get("/query/")
async def query_document(query: str):
    """Query the stored documents using embeddings."""
    query_embedding = embed_model.encode(query).tolist()
    
    results = collection.query(embeddings=[query_embedding], n_results=5)
    
    return JSONResponse(content={"results": results})

if __name__ == "__main__":
    import uvicorn
    
    # Ensure the temp directory exists
    os.makedirs("./temp", exist_ok=True)

    uvicorn.run(app, host="0.0.0.0", port=8000)

