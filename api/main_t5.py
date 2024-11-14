from fastapi import FastAPI, HTTPException, Request
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from data import read_braille_tokens, add_braille_tokens


# FastAPI 앱 초기화
app = FastAPI()

# 모델 및 토크나이저 로드
model_name = "azaraks/t5-v1.1-large-ko-to-kb"
tokenizer = AutoTokenizer.from_pretrained(model_name, revision="v0e5", force_download=True, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, revision="v0e5", force_download=True)
model.to('cuda')

braille_dict = read_braille_tokens()
add_braille_tokens(tokenizer, model)

if torch.cuda.is_available():
    model.to("cuda")

# 번역 함수 정의
def translate_text(text):
    max_length = 1024
    input_text = f'translate Korean to Braille: "{text}"\nBraille:'
    inputs = tokenizer(input_text, return_tensors="pt", max_length=max_length, truncation=True)
    
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    # 추론 실행
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            num_beams=4,
            early_stopping=True
        )
    
    # print("output:", outputs)

    return outputs

# 엔드포인트 정의
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("input_text")
    print("Received text:", text)
    
    try:
        result = ''.join(tokenizer.batch_decode(translate_text(text)))
        print("Decoded result: ", result)
        return {"prediction": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
