from transformers import MarianMTModel, MarianTokenizer

model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-hi", use_auth_token=True)
tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi", use_auth_token=True)


def translate(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    translated_tokens = model.generate(**inputs)
    hindi_translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

    return hindi_translation
