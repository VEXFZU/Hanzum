import streamlit as st
from document import extract_text_from_pdf, extract_text_from_docx
from converter import translate_to_braille

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
        braille_text = translate_to_braille(text, st)

        # 점자만 추출
        braille_translation = braille_text.split("Braille Translation:")[-1].strip()
        st.code(braille_translation, language="braille")
