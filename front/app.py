import os
import streamlit as st
from document import extract_text_from_pdf, extract_text_from_docx
from split_merge import temp_merge_results, temp_gather_results
import chardet

st.title("🌱 한점 두점 ⠚⠒⠨⠎⠢ ⠊⠍⠨⠎⠢")

if "api_url" not in st.session_state:
    st.session_state.api_url = os.environ.get("VXFZ_TRANSLATOR_API_URL")

# 탭 생성
tab0, tab1, tab2, tab3 = st.tabs(["단문 점역", "파일 점역 보기", "BRL 다운로드", "BRF 다운로드"])


def process_uploaded_file(uploaded_file):
    if not uploaded_file:
        return None
    file_type = uploaded_file.name.split('.')[-1]

    ret = None
    if file_type == 'pdf':
        ret = extract_text_from_pdf(uploaded_file)
    elif file_type == 'txt':
        chardet_ret = chardet.detect(uploaded_file.read())  # 인코딩 추정
        encoding = chardet_ret['encoding']
        uploaded_file.seek(0)
        ret = uploaded_file.read().decode(encoding)
    elif file_type == 'docx':
        ret = extract_text_from_docx(uploaded_file)

    if ret is None:
        st.error("지원하지 않는 파일 형식입니다.")
        st.stop()

    return ret


st.write("PDF, TXT 또는 DOCX 파일을 업로드하여 점자로 변환해보세요.")
uploaded_file = st.file_uploader("파일을 업로드하세요 (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
text = process_uploaded_file(uploaded_file)

if "translated_unicode" not in st.session_state:
    st.session_state.translated_unicode = None

if "translated_unicode_tt" not in st.session_state:
    st.session_state.translated_unicode_tt = None

if text and st.session_state.translated_unicode is None:
    st.session_state.translated_unicode = temp_gather_results(text, st)

translated_unicode = st.session_state.translated_unicode

with tab0:
    tt_text = st.text_area("텍스트를 입력하세요", height=200)
    tt_code = st.code("", language="braille")
    if st.button("변환") and tt_text:
        st.session_state.translated_unicode_tt = temp_gather_results(tt_text, st)
    # ToDo : Recover original positions of sentences.
    if st.session_state.translated_unicode_tt:
        tt_code.code('\n'.join(st.session_state.translated_unicode_tt))

# 탭 1: 기본 변환
with tab1:
    if text:
        # 추출된 텍스트 확인
        st.subheader("추출된 텍스트")
        st.write(text)
        st.code('\n'.join(translated_unicode), language="braille")
    else:
        st.session_state.translated_unicode = None

# 탭 2: brl 변환
with tab2:
    if text and translated_unicode:
        st.header("BRL 변환")
        st.download_button(
            label="Download BRL",
            data=temp_merge_results(translated_unicode, False),
            file_name="output.brl",
            mime="text/plain",
        )

# 탭 3: brf 변환
with tab3:
    if text and translated_unicode:
        st.header("BRF 변환")
        st.download_button(
            label="Download BRF",
            data=temp_merge_results(translated_unicode, True),
            file_name="output.brf",
            mime="text/plain",
        )
