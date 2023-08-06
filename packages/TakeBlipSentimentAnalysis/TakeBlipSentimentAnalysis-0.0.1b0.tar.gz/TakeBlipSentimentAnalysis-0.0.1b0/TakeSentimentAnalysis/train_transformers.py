import torch
from tqdm import tqdm

from datasets import load_dataset
from transformers import (AutoTokenizer, DataCollatorWithPadding, AdamW,
                          BertForSequenceClassification,
                          get_linear_schedule_with_warmup)


def preprocess_function(batch):
    tokenized_batch = tokenizer(batch["MessageProcessed"],
                                padding=True,
                                truncation=True)
    tokenized_batch["labels"] = [sentiment_2_int(label) for label in
                                 batch["sentimentLabel"]]
    return tokenized_batch


def send_inputs_to_device(inputs, device):
    return {key: tensor.to(device) for key, tensor in inputs.items()}


def validate(model, dataset_loader, device):
    validation_loss = 0
    with torch.no_grad():
        model.eval()
        for idx, inputs in dataset_loader:
            inputs = send_inputs_to_device(inputs, device)
            loss, scores = model(**inputs)[:2]
            validation_loss += loss
    loss = loss/len(dataset_loader)
    return loss


input_path = 'files/input/sample_sentiment.csv'
validate_path = 'files/input/sample_sentiment_validation.csv'

pre_trained_model = 'neuralmind/bert-base-portuguese-cased'
batch_size = 16
num_epochs = 1
num_warmup_steps = 500
val = True
val_period = 1

raw_datasets = load_dataset('csv', data_files={'train': input_path,
                                               'test': validate_path})
tokenizer = AutoTokenizer.from_pretrained(pre_trained_model,
                                          do_lower_case=False)
tokenized_data = raw_datasets.map(preprocess_function, batched=True)
tokenized_data.set_format(type='torch',
                          columns=['input_ids', 'token_type_ids',
                                   'attention_mask', 'labels'])

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

train_loader = torch.utils.data.DataLoader(tokenized_data['train'],
                                           batch_size=batch_size,
                                           collate_fn=data_collator)
test_loader = torch.utils.data.DataLoader(tokenized_data['test'],
                                          batch_size=batch_size,
                                          collate_fn=data_collator)

model = BertForSequenceClassification.from_pretrained(pre_trained_model,
                                                      num_labels=3)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model.train().to(device)

optimizer = AdamW(model.parameters(), lr=5e-6)
scheduler = get_linear_schedule_with_warmup(optimizer,
                                            num_warmup_steps,
                                            num_epochs * len(train_loader))

epoch_bar = tqdm(range(num_epochs))

loss_function = torch.nn.CrossEntropyLoss()

for epoch in epoch_bar:
    for idx, inputs in enumerate(train_loader):
        inputs = send_inputs_to_device(inputs, device)
        optimizer.zero_grad()
        loss, logits = model(**inputs)[:2]

        loss.backward()
        optimizer.step()
    if val and epoch % val_period == 0:
        val_loss = validate(model, test_loader, device)
        model.train()
