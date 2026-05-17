from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from rag.vector_service import CanteenRAG
from model.llm_client import QwenClient

app = FastAPI(title="校园食堂 AI 助手后端")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = os.path.dirname(BASE_DIR)
CHROMA_DB_DIR = os.path.join(PROJECT_ROOT, "database", "chroma_db")
KNOWLEDGE_FILE = os.path.join(PROJECT_ROOT, "database", "canteen_docs", "rules.txt")

rag_service = CanteenRAG()
rag_service.persist_directory = CHROMA_DB_DIR
llm_client = QwenClient(model_name="qwen3:1.7b")

class QueryModel(BaseModel):
    question: str

class FeedbackModel(BaseModel):
    content: str

@app.on_event("startup")
def startup_event():
    print(f"检查向量库路径: {CHROMA_DB_DIR}")
    print(f"检查知识库文件路径: {KNOWLEDGE_FILE}")
    
    if not os.path.exists(CHROMA_DB_DIR):
        print("正在首次初始化向量数据库...")
        if os.path.exists(KNOWLEDGE_FILE):
            rag_service.init_vector_db(KNOWLEDGE_FILE)
        else:
            print(f"错误：未找到知识库文件 {KNOWLEDGE_FILE}，请确认文件是否存在！")
    else:
        print("成功加载已有向量数据库。")

@app.post("/api/chat")
async def chat(data: QueryModel):
    if not data.question:
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    print(f"\n[收到小程序提问]: {data.question}")
    
    context_list = rag_service.search(data.question, k=2)
    print(f"[后端检索到的上下文片段数量]: {len(context_list)}")
    for idx, ctx in enumerate(context_list):
        print(f" -> 片段 {idx+1}: {ctx.strip()}")
        
    answer = llm_client.generate_answer(data.question, context_list)
    print(f"[Ollama 生成的回复]: {answer}")
    
    return {"answer": answer}

@app.post("/api/feedback")
async def submit_feedback(data: FeedbackModel):
    if not data.content:
        raise HTTPException(status_code=400, detail="反馈内容不能为空")
    
    print(f"\n[收到学生投诉/建议]: {data.content}")
    
    category = llm_client.classify_feedback(data.content)
    
    print(f"[大模型自动分类结果]: {category}")
    
    return {
        "status": "success",
        "category": category,
        "message": f"小安已收到您的【{category}】相关反馈，感谢您对食堂建设的贡献！"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
