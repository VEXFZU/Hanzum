import torch
from transformers import (
    StoppingCriteria, StoppingCriteriaList
)

from unsloth import FastLanguageModel

# 최대 시퀀스 길이 및 데이터 타입 설정
max_seq_length = 4096

# 모델과 토크나이저 로드
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="doiee/llama3-8b-instruct-ko-to-braille-checkpoint-9500",
    max_seq_length=max_seq_length,
    dtype=torch.bfloat16,
    load_in_4bit=True,
)

# LoRA 적용 설정
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    lora_dropout=0.01,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj"
    ],
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
    use_rslora=False,
    loftq_config=None,
)

class StopOnToken(StoppingCriteria):
    def __init__(self, stop_token_id):
        self.stop_token_id = stop_token_id

    def __call__(self, input_ids, scores, **kwargs):
        return self.stop_token_id in input_ids[0]

# 추론에 사용할 정지 기준 설정
stop_token = "<|end_of_text|>"
stop_token_id = tokenizer.encode(stop_token, add_special_tokens=False)[0]
stopping_criteria = StoppingCriteriaList([StopOnToken(stop_token_id)])

# 모델을 추론 모드로 전환
FastLanguageModel.for_inference(model)
