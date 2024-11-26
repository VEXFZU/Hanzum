import os
from transformers import T5ForConditionalGeneration, AutoTokenizer

_model_name_or_path = os.environ.get("VXFZ_TRANSLATER_MODEL_T5_NAME", "azaraks/t5-xlarge-ko-kb")
_max_length = int(os.environ.get("VXFZ_TRANSALTER_MODEL_T5_MAX_LENGTH", "256"))

model = T5ForConditionalGeneration.from_pretrained(_model_name_or_path).to('cuda')
tokenizer = AutoTokenizer.from_pretrained(_model_name_or_path)


def translate(text):
    input_text = f'translate Korean to Braille: "{text}"'
    inputs = tokenizer(input_text,
                       return_tensors="pt",
                       max_length=_max_length,
                       truncation=True,
                       ).to('cuda')
    outputs = model.generate(**inputs,
                             max_length=_max_length,
                             num_beams=4,
                             early_stopping=True,
                             )
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return output_text[6:-5]  # removes `<pad>"`(6 chars) from the start and `"</s>`(5 chars) from the end.
