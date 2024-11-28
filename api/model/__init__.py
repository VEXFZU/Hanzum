import os

match os.environ.get("VXFZ_TRANSLATOR_MODEL_TYPE", "t5"):
    case 'llama3':
        from api.model.llama import translate
    case 't5' | _:  # default to t5. better to throw an error, but this is more convenient for now.
        from api.model.t5 import translate
