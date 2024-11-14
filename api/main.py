from fastapi import FastAPI, Request
from transformers import TextStreamer
from fastapi.responses import Response

from model.llama import model, tokenizer, stopping_criteria #from api.model.llama로 되어 있던 것에서 같은 위치이므로 api 생략

# FastAPI 앱 인스턴스 생성
app = FastAPI()

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
    
    input_text = f"""
Convert the following Korean sentence to Braille.

Korean Sentence: "{text}"
Braille Translation: """
    
    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
    text_streamer = TextStreamer(tokenizer)  

    output = model.generate(
        **inputs,
        streamer=text_streamer,
        stopping_criteria=stopping_criteria
    )

    prediction = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"prediction": prediction}
