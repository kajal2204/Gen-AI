This implementation provides a lightweight FastAPI server designed for Retrieval-Augmented Generation (RAG) applications. It facilitates the ingestion, embedding, and querying of various document formats, including PDF, DOCX, and TXT. The server leverages ChromaDB for persistent storage of document embeddings and utilizes the sentence-transformers/all-MiniLM-L6-v2 model from Hugging Face to generate high-quality embeddings for text data.
Key Features
Document Upload and Processing:
Users can upload documents via a RESTful API endpoint (/upload/).
The server supports multiple file formats (PDF, DOCX, TXT) and extracts text content using appropriate libraries.
Temporary files are created during the upload process and are cleaned up after processing to maintain system hygiene.
Embedding Generation:
Extracted text is converted into embeddings using the SentenceTransformer model, enabling efficient similarity searches.
The embeddings are stored in ChromaDB along with metadata such as the original filename for easy retrieval.
Querying Capabilities:
An API endpoint (/query/) allows users to perform searches against the stored documents using natural language queries.
The server returns relevant documents based on their semantic similarity to the query input.
Asynchronous Handling:
The FastAPI framework supports asynchronous operations, ensuring non-blocking API endpoints that can handle concurrent requests efficiently.
Robust Error Handling:
The implementation includes comprehensive error handling to manage unsupported file types and potential processing errors, returning appropriate HTTP status codes and messages.
Technical Stack
FastAPI: A modern web framework for building APIs with Python 3.7+ that is fast and easy to use.
ChromaDB: A persistent database client used for storing document embeddings.
Hugging Face Transformers: Utilizes state-of-the-art models for generating text embeddings.
File Processing Libraries:
PyPDF2 for extracting text from PDF files.
python-docx and docx2txt for handling DOCX and DOC files.
