import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Pinecone and OpenAI API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Pinecone client (v3 syntax)
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "integration-of-pm-and-llms"

# Initialize index client
index = pc.Index(name=index_name)

# Load documents
loader = DirectoryLoader(
    "/Users/alejandromateocobo/Documents/PythonProjects/Integration_Of_LLMs_And_Process_Mining/data/context",
    glob="**/*.txt",
    loader_cls=TextLoader
)
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunked_docs = text_splitter.split_documents(documents)

# Prepare unique IDs for each document chunk
def generate_ids(doc_chunk, index):
    doc_source = doc_chunk.metadata.get('source', f'doc_{index}')
    chunk_id = doc_chunk.metadata.get('chunk', index)
    return f"{os.path.basename(doc_source)}#chunk_{chunk_id}"

ids = [f"doc_{i}" for i in range(len(chunked_docs))]

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

# Initialize vector store
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Add documents to Pinecone
vector_store.add_documents(documents=chunked_docs, ids=ids)

print("Documents successfully embedded and stored in Pinecone!")

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

query = "Which activities seem to be the most frequent?"

retrieved_docs = vector_store.similarity_search(query, k=5)
docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

prompt = f'''You are a process mining assistant assistant:

Here's a question: {query}

Here's some context from the release notes:

{docs_content}


Question: {query}

Answer:
'''
print(prompt)

# This will take a few seconds to run, due to the generation of the response from OpenAI
answer = llm.invoke(prompt)
print(answer)
