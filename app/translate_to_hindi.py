from transformers import MBartForConditionalGeneration, MBart50Tokenizer
import torch
from .sentiment_analysis import chunk_text
import streamlit as st
if torch.cuda.is_available():
    device = torch.device("cuda")

else:
    device = torch.device("cpu")


@st.cache_resource()
def load_model():
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50Tokenizer.from_pretrained(model_name, src_lang="en_XX", tgt_lang="hi_IN")
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    model.to(device)
    return model, tokenizer


def translate(text):
    # Tokenize the input text
    chunks = chunk_text(text)
    print(f"Total Chunks: {len(chunks)}")
    translated_texts = []
    model, tokenizer = load_model()
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=256, padding=True)
        # Move input tensors to the same device as the model
        inputs = {k: v.to(device) for k, v in inputs.items()}
        translated_tokens = model.generate(**inputs, max_length=256, num_beams=4,
                                           forced_bos_token_id=tokenizer.lang_code_to_id["hi_IN"])
        hindi_translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        translated_texts.append(hindi_translation)
    return " ".join(translated_texts)

