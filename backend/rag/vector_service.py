import os
os.environ["HF_HOME"] = "D:\\Code\\an_AI\\backend\\.cache\\huggingface"
os.environ["TRANSFORMERS_CACHE"] = "D:\\Code\\an_AI\\backend\\.cache\\huggingface"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from huggingface_hub import snapshot_download
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

MODEL_NAME = "BAAI/bge-small-zh-v1.5"
MODEL_DIR = "D:\\Code\\an_AI\\backend\\.cache\\models\\bge-small-zh-v1.5"

def download_model():
    if not os.path.exists(os.path.join(MODEL_DIR, "config.json")):
        print("正在下载嵌入模型...")
        snapshot_download(
            repo_id=MODEL_NAME,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False
        )
        print("模型下载完成！")
    else:
        print("模型已存在，跳过下载。")

class CanteenRAG:
    def __init__(self):
        download_model()
        self.embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_DIR,
            model_kwargs={'device': 'cpu'}
        )
        self.persist_directory = "./database/chroma_db"
        self.vector_store = None

    def init_vector_db(self, file_path):
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=0,
            separators=["\n\n", "\n"]
        )
        docs = text_splitter.split_documents(documents)
        
        self.vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        print("向量数据库构建成功！")

    def search(self, query, k=2):
        if not self.vector_store:
            self.vector_store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
