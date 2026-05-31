import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("MODELSCOPE_CACHE", os.path.join(os.path.expanduser("~"), ".cache", "modelscope"))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompt.templates import RAG_PROMPT_TEMPLATE, CLASSIFY_PROMPT_TEMPLATE
import datetime


class LocalLLMClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_path_or_id: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        if self._initialized:
            return

        print("====== 开始加载本地 Hugging Face 模型 ======")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path_or_id, trust_remote_code=True
        )

        if torch.cuda.is_available():
            self.device = "cuda"
            self.torch_dtype = torch.float16
        else:
            self.device = "cpu"
            self.torch_dtype = torch.float32

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path_or_id,
            torch_dtype=self.torch_dtype,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        print(f"====== 模型成功加载至设备: {self.model.device} ======")
        self._initialized = True

    def generate_response(self, system_prompt: str, user_prompt: str, temperature: float = 0.1, max_tokens: int = 512) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True if temperature > 0 else False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    def generate_answer(self, question, context_list):
        context = "\n".join(context_list)
        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")

        system_prompt = RAG_PROMPT_TEMPLATE.format(
            current_date=current_date,
            context=context,
            question=question
        )

        try:
            response = self.generate_response(
                system_prompt=system_prompt,
                user_prompt=question,
                temperature=0.1
            )
            return response
        except Exception as e:
            return f"AI 助手开小差了，请稍后再试。错误: {str(e)}"

    def classify_feedback(self, feedback):
        system_prompt = CLASSIFY_PROMPT_TEMPLATE.format(feedback=feedback)

        try:
            response = self.generate_response(
                system_prompt=system_prompt,
                user_prompt=feedback,
                temperature=0.0,
                max_tokens=20
            )
            return response.strip()
        except Exception as e:
            return "其他建议"


MODEL_PATH = os.environ.get(
    "LLM_MODEL_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models", "Qwen2.5-1.5B-Instruct")
)
llm_client = LocalLLMClient(MODEL_PATH)
