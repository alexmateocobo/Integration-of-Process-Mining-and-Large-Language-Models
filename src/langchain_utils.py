import os
import logging
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.chat_models import init_chat_model


class LangChainUtils:
    def __init__(self, context_dir, index_name="integration-of-pm-and-llms"):
        load_dotenv()

        self.context_dir = context_dir
        self.index_name = index_name

        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.pinecone_api_key or not self.openai_api_key:
            raise EnvironmentError("Missing API keys. Please check your .env file.")

        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index = self.pc.Index(name=self.index_name)
        self.vector_store = None
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    def load_and_embed_documents(self):
        logging.info("Loading and embedding documents...")

        loader = DirectoryLoader(
            self.context_dir,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunked_docs = text_splitter.split_documents(documents)
        ids = [f"doc_{i}" for i in range(len(chunked_docs))]

        embeddings = OpenAIEmbeddings(api_key=self.openai_api_key, model="text-embedding-3-small")
        self.vector_store = PineconeVectorStore(index=self.index, embedding=embeddings)
        self.vector_store.add_documents(documents=chunked_docs, ids=ids)

        logging.info("Documents successfully embedded and stored in Pinecone.")

    def query_context(self, query, k=10):
        if self.vector_store is None:
            raise Exception("Vector store not initialized. Run load_and_embed_documents() first.")

        logging.info(f"Running similarity search for query: {query}")
        retrieved_docs = self.vector_store.similarity_search(query, k=k)
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

        prompt = f"""You are a helpful and knowledgeable assistant specialized in process mining. Your role is to analyze process-related data, models, and documentation to provide accurate and concise answers.

        Here’s a user question: {query}

        Here is some extracted documentation and context:

        {docs_content}

        Now please answer the question as clearly and precisely as possible:
        """

        logging.info("Invoking LLM with prompt...")
        answer = self.llm.invoke(prompt)
        return answer
