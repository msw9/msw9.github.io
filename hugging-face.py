from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

"""
TUTORIELS
https://huggingface.co/learn/llm-course/chapter7/4
https://huggingface.co/docs/hub/datasets-upload-guide-llm
"""
raw_datasets = load_dataset("csv", data_files="resultats.csv")
split_datasets = raw_datasets["train"].train_test_split(train_size=0.9, seed=20)

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-tc-bible-big-aav-fra_ita_por_spa")


mye_sentence = split_datasets['train'][1]['Myènè']
fr_sentence = split_datasets['train'][1]['Français']
inputs = tokenizer(mye_sentence,text_target = fr_sentence)
print(inputs)

