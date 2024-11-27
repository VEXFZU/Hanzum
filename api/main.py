from fastapi import FastAPI, Request
from fastapi.responses import Response

from api.model import translate

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
    
    prediction = translate(text)

    return {"prediction": prediction}
