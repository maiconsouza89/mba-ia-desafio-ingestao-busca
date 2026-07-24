import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

def search_vector(question=None) -> dict:
    """Retorna uma lista com texto, score e metadados dos documentos encontrados."""
    for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    results = store.similarity_search_with_score(query=question, k=10)  

    itens = []

    for i, (doc, score) in enumerate(results, start=1):
        itens.append(
            {
                "resultado": i,
                "score": score,
                "texto": doc.page_content.strip(),
                "metadados": dict(doc.metadata),
            }
        )

    return itens