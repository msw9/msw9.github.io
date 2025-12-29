from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

"""
TUTORIELS
https://huggingface.co/learn/llm-course/chapter7/4
https://huggingface.co/docs/hub/datasets-upload-guide-llm
"""
def preprocess_function(examples): # example = split_datasets['train']
    inputs = examples['Myènè']
    targets = examples['Français']
    model_inputs = tokenizer(
        inputs, text_target=targets,max_length=max_length,truncation=True
        )
    return model_inputs

raw_datasets = load_dataset("csv", data_files="resultats.csv")
split_datasets = raw_datasets["train"].train_test_split(train_size=0.9, seed=20)

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-tc-bible-big-aav-fra_ita_por_spa")

max_length = 128 # à changer car nos phrases plus longues que dans tutoriel


tokenized_datasets = split_datasets.map(
    preprocess_function,
    batched=True,
    remove_columns=split_datasets["train"].column_names,
)

print(tokenized_datasets['train'][0])
