from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from fastapi.responses import Response

torch.cuda.empty_cache()

app = FastAPI()

# 모델 로드 (서버가 실행 중인 동안에는 계속 로드된 상태)
tokenizer = AutoTokenizer.from_pretrained("doiee/llama3-8b-instruct-ko-to-braille-checkpoint-3250")
model = AutoModelForCausalLM.from_pretrained("beomi/Llama-3-Open-Ko-8B-Instruct-preview", torch_dtype=torch.float16).to("cuda") # GPU 사용

# 루트 경로에 간단한 응답 추가
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI server is running!"}

# favicon.ico 요청 무시
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.post("/predict")
async def predict(input_text: str):
    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = model.generate(inputs["input_ids"])
    prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"prediction": prediction}
