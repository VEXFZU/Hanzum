from fastapi import FastAPI, Body
from fastapi.responses import Response
from pydantic import BaseModel
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


class Item(BaseModel):
    input_text: str

# 예측 API 엔드포인트 정의
@app.post("/predict")
def predict(item: Item):
    text = item.input_text
    print("Received input_text:", text)

    prediction = translate(text)

    return {"prediction": prediction}
