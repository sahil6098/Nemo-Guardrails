from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def _make_documents():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = []
    for item in HR_DOCUMENTS:
        chunks = splitter.create_documents(
            texts=[item["content"]],
            metadatas=[{"source": item["title"]}],
        )
        docs.extend(chunks)
    return docs

def build_vectorstore():
    embeddings = FastEmbedEmbeddings(model_name=EMBED_MODEL)
    docs = _make_documents()
    vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
    return vectorstore

def retrieve(query: str, vectorstore, k: int = 3):
    """Return top-k chunks with relevance scores."""
    results = vectorstore.similarity_search_with_relevance_scores(query, k=k)
    return [
        {
            "source": doc.metadata.get("source", "Unknown"),
            "content": doc.page_content,
            "score": round(score, 3),
        }
        for doc, score in results
    ]
