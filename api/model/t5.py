import os
from transformers import T5ForConditionalGeneration, AutoTokenizer

_model_name_or_path = os.environ.get("VXFZ_TRANSLATOR_MODEL_T5_NAME", "azaraks/t5-xlarge-ko-kb")
_max_length = int(os.environ.get("VXFZ_TRANSALTOR_MODEL_T5_MAX_LENGTH", "256"))
_max_input_length = _max_length >> 2

model = T5ForConditionalGeneration.from_pretrained(_model_name_or_path).to('cuda')
tokenizer = AutoTokenizer.from_pretrained(_model_name_or_path)


def split_sentence_with_tokenizer(sentence):
    words = sentence.split()
    result = []
    start, end = 0, len(words)

    while start < len(words):
        low, high = start, end
        while low < high:
            mid = (low + high) // 2
            chunk = " ".join(words[start:mid + 1])
            tokenized = tokenizer(chunk, return_tensors='pt', max_length=_max_length, truncation=True)
            if tokenized.input_ids.shape[1] <= _max_input_length:
                low = mid + 1
            else:
                high = mid
        result.append(" ".join(words[start:low]))
        start = low

    return result


def translate(text):
    chunks = split_sentence_with_tokenizer(text)
    output_texts = []
    for chunk in chunks:
        print(chunk)
        instruction = f'translate Korean to Braille: "{chunk}"'
        inputs = tokenizer(instruction,
                           return_tensors='pt',
                           max_length=_max_length,
                           truncation=True,
                           ).to('cuda')

        outputs = model.generate(**inputs,
                                 max_length=_max_length,
                                 num_beams=4,
                                 early_stopping=True)

        output_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
        print(output_text)
        output_texts.append(output_text[6:-5])
    output_text = ' '.join(output_texts)
    return output_text
