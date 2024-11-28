import requests


# 텍스트를 점자로 번역 (FastAPI 서버에 요청)
def translate_to_braille(text, st):
    print("Text to be translated:", text)  # 전송할 텍스트 확인용
    try:
        response = requests.post(st.session_state.api_url,
                                 timeout=120,
                                 json={"input_text": text},
                                 )
        response.raise_for_status()  # 에러 발생 시 예외 발생
        braille_text = response.json().get("prediction", "")
        print(braille_text)
        return braille_text
    except requests.exceptions.RequestException as e:
        st.error(f"번역 서버에서 오류가 발생했습니다: {e}")
        return ""


def convert_unicode_braille_to_ascii_braille(unicode_braille):
    table = {
        k: v for k, v in zip("⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿",
                             " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)=")
    }
    ret = ''.join(table.get(c, c) for c in unicode_braille['braille'])
    ret += unicode_braille['sep']
    return ret


def convert_braille_text_to_brf(unicode_brailles: list[dict[str, str]],
                                char_per_line: int = 32,
                                line_per_page: int = 26) -> str:
    ret = str()

    def add_new_line_if_needed(t):
        if t:
            if t[-1] != '\n':
                return t + '\n'
            else:
                return t
        else:
            return '\n'

    num_line = 0
    ascii_brailles = []
    # if line is longer than char_per_line, split it into multiple lines
    # if num_line == line_per_page, add '\n\f' to ret and reset num_line
    for unicode_braille in unicode_brailles:
        # convert unicode braille to ascii braille
        ascii_braille = convert_unicode_braille_to_ascii_braille(unicode_braille)
        if len(ascii_braille) > char_per_line:
            ascii_brailles.extend([ascii_braille[i:i + char_per_line]
                                   for i in range(0, len(ascii_braille), char_per_line)])
        else:
            ascii_brailles.append(ascii_braille)
    for ascii_braille in ascii_brailles:
        if num_line == line_per_page:
            ret += '\f'
            num_line = 0
        ret += ascii_braille
        ret = add_new_line_if_needed(ret)
        num_line += 1
    return ret
