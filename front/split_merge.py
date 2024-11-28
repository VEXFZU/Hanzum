import os
import re
from transformers import AutoTokenizer
from converter import (
    convert_braille_text_to_brf,
    convert_unicode_braille_to_ascii_braille,
    translate_to_braille,
)

_tokenizer_name_or_path = os.environ.get("VXFZ_TRANSLATOR_MODEL_NAME")
_tokenizer = AutoTokenizer.from_pretrained(_tokenizer_name_or_path)
_max_length = int(os.environ.get("VXFZ_TRANSALTOR_MODEL_MAX_LENGTH"))
_max_input_length = int(os.environ.get("VXFZ_TRANSALTOR_MODEL_MAX_LENGTH")) >> 2


# ToDo: Add seq. number to the result, if queue is used.
def split_text(text: str) -> list[dict[str, str]]:
    segments = re.split(r'(\s+)', text)
    result = []
    current_chunk = []
    current_sep = ""

    for segment in segments:
        if re.match(r'\s+', segment):
            current_sep = segment
        else:
            current_chunk.append({'text': segment, 'sep': current_sep})
            current_sep = ""

            chunk = "".join([chunk['text'] + chunk['sep'] for chunk in current_chunk])
            tokenized = _tokenizer(chunk, return_tensors='pt', max_length=_max_length, truncation=True)

            if tokenized.input_ids.shape[1] > _max_input_length:
                current_chunk.pop()
                result.append(current_chunk)
                current_chunk = [{'text': segment, 'sep': current_sep}]

    if current_chunk:
        result.append(current_chunk)

    flattened_result = [item for sublist in result for item in sublist]
    return flattened_result


## These functions won't be used in the final code.
# ToDo: Enqueue split texts.
# ToDo: Dequeue results and merge them.
# ToDo: Write merged results to a file.
def temp_gather_results(long_text, st):
    list_text = split_text(long_text)
    unicode_brailles = [{'braille': translate_to_braille(i['text'], st), 'sep': i['sep']} for i in list_text]
    return unicode_brailles


def temp_merge_results(unicode_brailles, is_brf=True):
    if is_brf:
        return convert_braille_text_to_brf(unicode_brailles)
    else:
        return '\n'.join([convert_unicode_braille_to_ascii_braille(i)
                          for i in unicode_brailles])
