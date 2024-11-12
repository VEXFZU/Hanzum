import streamlit as st
import requests
import fitz  # PyMuPDF
import docx

# FastAPI 서버 URL
ip = "34.81.26.181" # ip 바뀔때마다 수정
API_URL = f"http://{ip}:8002/predict"



# PDF 파일에서 텍스트 추출
def extract_text_from_pdf(file):
    text = ""
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

# DOCX 파일에서 텍스트 추출
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# 텍스트를 점자로 번역 (FastAPI 서버에 요청)
def translate_to_braille(text):
    print("Text to be translated:", text)  # 전송할 텍스트 확인용
    try:
        response = requests.post(API_URL, json={"input_text": text})
        response.raise_for_status()  # 에러 발생 시 예외 발생
        return response.json().get("prediction", "")
    except requests.exceptions.RequestException as e:
        st.error(f"번역 서버에서 오류가 발생했습니다: {e}")
        return ""



# Streamlit 인터페이스 구성
st.title("한국어 점자 번역기")
st.write("PDF, TXT 또는 DOCX 파일을 업로드하여 점자로 변환해보세요.")

uploaded_file = st.file_uploader("파일을 업로드하세요 (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type == 'pdf':
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == 'txt':
        text = uploaded_file.read().decode("utf-8")
    elif file_type == 'docx':
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("지원하지 않는 파일 형식입니다.")
        st.stop()

    # 추출된 텍스트 확인
    st.subheader("추출된 텍스트")
    st.write(text if text else "텍스트가 포함된 파일인지 확인해 주세요.")

    # 점자 번역 결과 출력
    if text:
        st.subheader("점자 번역 결과")
        braille_text = translate_to_braille(text)
        
        # 점자만 추출
        braille_translation = braille_text.split("Braille Translation:")[-1].strip()
        st.text_area(" ",braille_translation, height=300)
