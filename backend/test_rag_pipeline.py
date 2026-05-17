import os
import sys

os.environ["HF_HOME"] = "D:/Code/an_AI/backend/.cache/huggingface"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag.vector_service import CanteenRAG
from backend.model.llm_client import QwenClient

def main():
    print("====== 校园食堂 AI 助手全链路测试 ======")
    
    rag_service = CanteenRAG()
    llm_client = QwenClient(model_name="qwen3:1.7b")
    
    knowledge_file = "./database/canteen_docs/rules.txt"
    if not os.path.exists(knowledge_file):
        print(f"错误: 未找到知识库文件：{knowledge_file}，请先创建它。")
        return
        
    print("正在建立/加载向量数据库...")
    rag_service.init_vector_db(knowledge_file)
    
    test_cases = [
        "今天二食堂还有低糖套餐吗？",
        "一食堂二楼档口为什么关门了？什么时候开？",
        "三食堂今天有黄焖鸡米饭吗？"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n--------------------------------------------------")
        print(f"测试用例 {i}: [学生提问] -> {question}")
        
        print("[Step 1/2] 正在检索向量数据库...")
        contexts = rag_service.search(question, k=2)
        print(f" -> 检索到的原始片段数量: {len(contexts)}")
        for idx, ctx in enumerate(contexts):
            print(f"    [相关片段{idx+1}]: {ctx.strip()}")
            
        print("[Step 2/2] 正在请求 Ollama 生成回答...")
        answer = llm_client.generate_answer(question, contexts)
        
        print(f"\n[AI小安的最终回复]:\n{answer}")
        print(f"--------------------------------------------------")

if __name__ == "__main__":
    main()
