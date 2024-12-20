import torch
from transformers import TextStreamer

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

# 모델을 추론 모드로 전환
FastLanguageModel.for_inference(model)


def translate(text):
    input_text = f"""
Convert the following Korean sentence to Braille.

Korean Sentence: "{text}"
Braille Translation: """

    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
    text_streamer = TextStreamer(tokenizer)

    output = model.generate(
        **inputs,
        streamer=text_streamer,
    )

    prediction = tokenizer.decode(output[0], skip_special_tokens=True)
    prediction = prediction.split("Braille Translation: ")[-1].strip()

    return prediction
