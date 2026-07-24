import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector


load_dotenv()

def ingest_pdf():

    print("Starting PDF ingestion process...\n")

    ## Validate environment variables
    for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    ## Load PDF   
    current_dir = Path(__file__).parent
    pdf_path = current_dir / os.getenv("PDF_PATH")

    print(f"Loading PDF file from {pdf_path}")

    ## Load the PDF file using PyPDFLoader
    docs = PyPDFLoader(str(pdf_path)).load()

    ## Split the document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False)
    docs = splitter.split_documents(docs)

    if not docs:
        print("No documents found to ingest. Please check the PDF file.")
        raise SystemExit(0) 

    ## Enrich the documents by removing empty metadata fields
    enriched = [
                Document(
                    page_content=d.page_content,
                    metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
                )
                for d in docs
            ] 

    print (f"Loaded {len(enriched)} documents\n")

    ## Generate embeddings for the documents
    print("Generating embeddings for the documents...\n")
    ids = [f"doc-{i}" for i in range(len(enriched))]


    ## Initialize the OpenAI embeddings model
    print
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    ## Initialize the PostgreSQL vector store
    print("Initializing the PostgreSQL vector store...")
    store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )

    ### Add the documents to the PostgreSQL vector store
    print("Adding documents to the PostgreSQL vector store...\n ")
    store.add_documents(documents=enriched, ids=ids)

    print(f"Successfully ingested {len(enriched)} documents into the PostgreSQL vector store.")





if __name__ == "__main__":
    ingest_pdf()