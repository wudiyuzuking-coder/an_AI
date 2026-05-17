import datetime
import ollama
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompt.templates import RAG_PROMPT_TEMPLATE

class QwenClient:
    def __init__(self, model_name="qwen:7b"):
        self.model_name = model_name

    def generate_answer(self, question, context_list):
        context = "\n".join(context_list)
        
        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
        
        prompt = RAG_PROMPT_TEMPLATE.format(
            current_date=current_date,
            context=context,
            question=question
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
                options={
                    'temperature': 0.1
                }
            )
            return response['message']['content']
            
        except Exception as e:
            return f"AI 助手开小差了，请稍后再试。错误: {str(e)}"

    def classify_feedback(self, feedback):
        from prompt.templates import CLASSIFY_PROMPT_TEMPLATE
        prompt = CLASSIFY_PROMPT_TEMPLATE.format(feedback=feedback)
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.0}
            )
            return response['message']['content'].strip()
        except Exception as e:
            return "其他建议"
