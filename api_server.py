from fastapi import FastAPI, Request
from unsloth import FastLanguageModel
from transformers import AutoTokenizer, TextStreamer, StoppingCriteria, StoppingCriteriaList
import torch
from fastapi.responses import Response


class StopOnToken(StoppingCriteria):
    def __init__(self, stop_token_id):
        self.stop_token_id = stop_token_id

    def __call__(self, input_ids, scores, **kwargs):
        return self.stop_token_id in input_ids[0]


# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 최대 시퀀스 길이 및 데이터 타입 설정
max_seq_length = 4096
dtype = torch.bfloat16

# 모델과 토크나이저 로드
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="doiee/llama3-8b-instruct-ko-to-braille-checkpoint-9500",
    max_seq_length=max_seq_length,
    dtype=dtype,
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
        "down_proj",
    ],
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
    use_rslora=False,
    loftq_config=None,
)

# 추론에 사용할 정지 기준 설정
stop_token = "<|end_of_text|>"
stop_token_id = tokenizer.encode(stop_token, add_special_tokens=False)[0]
stopping_criteria = StoppingCriteriaList([StopOnToken(stop_token_id)])

# 모델을 추론 모드로 전환
FastLanguageModel.for_inference(model)


# 기본 경로 응답 정의
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI server is running!"}


# favicon.ico 요청 무시
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


# 예측 API 엔드포인트 정의
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()

    text = data.get("input_text")

    print("Received input_text:", text)

    input_text = f"Convert the following Korean sentence to Braille.\n\nKorean Sentence: {text}"

    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
    text_streamer = TextStreamer(tokenizer)

    output = model.generate(
        **inputs,
        streamer=text_streamer,
        stopping_criteria=stopping_criteria,
    )

    prediction = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"prediction": prediction}
