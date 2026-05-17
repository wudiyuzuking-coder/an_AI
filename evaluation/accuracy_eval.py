import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from backend.model.llm_client import QwenClient

def run_accuracy_test():
    print("====== 开始评估：大模型反馈分类准确率 ======")
    llm_client = QwenClient(model_name="qwen3:1.7b")
    
    test_dataset = [
        ("这个菜里有头发，太恶心了，洗菜能认真点吗？", "食品卫生"),
        ("土豆牛肉里的牛肉根本咬不动，太老了。", "菜品口味"),
        ("一食堂现在的盒饭越来越贵了，大荤居然要8块钱。", "菜价建议"),
        ("打菜的阿姨态度很差，问一句话爱搭不理的。", "服务态度"),
        ("建议三食堂加装几个排队隔离带，大家都插队。", "其他建议"),
        ("西红柿炒鸡蛋全是皮，而且盐放多了，好咸。", "菜品口味"),
        ("盘子边缘还有干涸的菜汤，餐具消毒到位了吗？", "食品卫生"),
        ("学校食堂的定价能不能听证一下？感觉普遍偏贵。", "菜价建议")
    ]
    
    correct_count = 0
    total_count = len(test_dataset)
    
    for idx, (feedback, expected) in enumerate(test_dataset, 1):
        predicted = llm_client.classify_feedback(feedback)
        
        is_correct = (predicted == expected)
        if is_correct:
            correct_count += 1
            status = "成功"
        else:
            status = f"失败 (预期: {expected} -> 实际: {predicted})"
            
        print(f"[{idx}/{total_count}] 输入: {feedback[:15]}... | 结果: {status}")
        
    accuracy = (correct_count / total_count) * 100
    print("\n====== 评估报告 ======")
    print(f"总测试样本数: {total_count}")
    print(f"预测正确样本数: {correct_count}")
    print(f"最终分类准确率 (Accuracy): {accuracy:.2f}%")
    print("======================")

if __name__ == "__main__":
    run_accuracy_test()
