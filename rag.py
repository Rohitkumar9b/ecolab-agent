import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# CONFIG
DATA_PATH = "documents"
INDEX_PATH = "faiss_index"

embedding = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def load_documents():
    docs = []

    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)

        if file.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())

        elif file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())

    return docs


def create_vectorstore():
    print("🔄 Creating vector DB...")

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embedding)
    vectorstore.save_local(INDEX_PATH)

    print("✅ Vector DB created & saved")

    return vectorstore


def load_vectorstore():
    if os.path.exists(INDEX_PATH):
        print("✅ Loading existing vector DB...")
        return FAISS.load_local(INDEX_PATH, embedding, allow_dangerous_deserialization=True)
    else:
        return create_vectorstore()


# Initialize once (important)
vectorstore = load_vectorstore()


def rag_query(query: str):
    """
    Production RAG pipeline
    """

    # Step 1: Retrieve relevant docs
    docs = vectorstore.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 2: LLM answer with context
    prompt = f"""
    You are an intelligent assistant.

    Use ONLY the provided context to answer.

    Context:
    {context}

    Question:
    {query}

    If answer not found, say "I don't know".
    """

    response = llm.invoke(prompt)

    return response.content