import os
import sys

os.environ["HF_HOME"] = "D:\\Code\\an_AI\\backend\\.cache\\huggingface"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.model.llm_client import QwenClient

def main():
    print("====== 反馈分类功能测试 ======")
    
    llm_client = QwenClient(model_name="qwen3:1.7b")
    
    test_cases = [
        "二食堂的红烧肉太咸了，根本没法吃",
        "一食堂的餐具都没洗干净，上面还有油渍",
        "现在菜价太贵了，一份素菜都要8块钱",
        "打菜的阿姨态度特别差，问她有没有这个菜还翻白眼",
        "希望食堂能延长晚上的营业时间"
    ]
    
    for i, feedback in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {feedback}")
        category = llm_client.classify_feedback(feedback)
        print(f"分类结果: {category}")
        print("-" * 50)

if __name__ == "__main__":
    main()
