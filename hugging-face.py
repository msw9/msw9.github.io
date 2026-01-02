from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments,Seq2SeqTrainer
import numpy as np

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

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    # In case the model returns more than the prediction logits
    if isinstance(preds, tuple):
        preds = preds[0]

    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100s in the labels as we can't decode them
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [[label.strip()] for label in decoded_labels]

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    return {"bleu": result["score"]}

raw_datasets = load_dataset("csv", data_files="resultats.csv")
split_datasets = raw_datasets["train"].train_test_split(train_size=0.9, seed=20)

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-tc-bible-big-aav-fra_ita_por_spa")

max_length = 128 # à changer (?) car nos phrases plus longues que dans tutoriel

# I. PRE-PROCESS DATA
tokenized_datasets = split_datasets.map(
    preprocess_function,
    batched=True,
    remove_columns=split_datasets["train"].column_names,
)

#print(tokenized_datasets['train'][0])

# II. FINE-TUNING
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-tc-bible-big-aav-fra_ita_por_spa")
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

args = Seq2SeqTrainingArguments(
    f"mye-fra-model",
    eval_strategy="no",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3,
    predict_with_generate=True,
    fp16=True,
    push_to_hub=False,
)

trainer = Seq2SeqTrainer(
    model,
    args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.evaluate(max_length=max_length) #évaluer AVANT et après entraînement
"""
trainer.train()

trainer.evaluate(max_length=max_length)
"""
