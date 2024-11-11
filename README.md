### FastAPI 

1. gcp 올라간 모델 사용 - ip로 연결
    
    그대로 사용하면 되지만 이때는 변경된 ip주소에 맞춰 수정해주셔야 합니다.

2. 로컬에서 FastAPI 직접 연결
    
    api_server.py    

    -> ```uvicorn api_server:app --host 0.0.0.0 --port 8002```

    먼저 실행 후 streamlit 실행

### Streamlit

app.py
