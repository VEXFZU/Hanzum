from kss import Kss
from converter import (
    convert_braille_text_to_brf,
    convert_unicode_braille_to_ascii_braille,
    translate_to_braille,
)


# ToDo: Add seq. number to the result. if queue is used.
def split_text(text: str) -> list[str]:
    splitter = Kss("split_sentences")
    ret = splitter(text)
    return ret


## These functions won't be used in the final code.
# ToDo: Enqueue split texts.
# ToDo: Dequeue results and merge them.
# ToDo: Write merged results to a file.
def temp_gather_results(long_text, st):
    list_text = split_text(long_text)
    unicode_brailles = [translate_to_braille(i, st) for i in list_text]
    return unicode_brailles

def temp_merge_results(unicode_brailles, is_brf=True):
    if is_brf:
        return convert_braille_text_to_brf(unicode_brailles)
    return convert_unicode_braille_to_ascii_braille(unicode_brailles)
