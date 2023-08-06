# TakeBlipSentimentAnalysis
_Data & Analytics Research_

## Overview
Sentiment analysis is the process of detecting the sentiment of a sentence, the 
sentiment could be negative, positive or neutral.

This implementation uses a LSTM implementation to solve the task. The 
implementation is using PyTorch framework and Gensim FastText as input embedding.

To train the model it is necessary a csv file with the labeled dataset, and an 
embedding file. For prediction, the files needed are the embedding model, the 
trained model and the vocabulary of the labels (output of the train).

This implementation presents the possibility to predict the sentiment for a single
sentence and for a batch of sentences (by file or dictionary).

The LSTM architecture utilized in this implementation has 4 layers:

1) Embedding layer: a layer with the embedding representation of each word.

2) LSTM layer: receives as input the embedding representation of each word in 
a sentence. For each word generate a output with size pre-defined.

3) The linear output layer: receives as input the last word hidden output of 
the LSTM and applies a linear function to get a vector of the size of the 
possible labels.

4) Softmax layer: receives the output of the linear layer and apply softmax
    operation to get the probability of each label.

For the bidirectional LSTM the linear output layer receives the hidden
output from the first and the last word.

## Training 
To train your own Sentiment Analysis model you will need a csv file with the 
following structure:

	Message		                              Sentiment
    achei pessimo o atendimento	              Negative
    otimo trabalho		                      Positive
    bom dia                                       Neutral
    ...,						...

A few steps should be followed to train the model.

1) Import the main functions
2) Set the variables
3) Generate the vocabularies
4) Initialize the model
5) Training

An example with the steps
### Import main functions

```
import torch
import os
import pickle

from TakeSentimentAnalysis import model, utils
from TakeSentimentAnalysis.train import LSTMTrainer
```

### Set the variables

**File variables**
```
input_path = '*.csv'
sentence_column = 'Message'
label_column = 'Sentiment'
encoding = 'utf-8'
separator = '|'
use_pre_processing = True
save_dir = 'path_to_save_folder'
wordembed_path = '*.kv'
```

The file variables are:
* input-path: Path to input file that contains sequences of sentences.
* sentence_column: String with the name of the column of sentences to be read 
from input file.
* label_column: String with the name of the column of labels to be read from 
input file.
* encoding: Input file encoding.
* separator: Input file column separator.
* use_pre_processing: Whether to pre process input data
* save-dir: Directory to save outputs.
* wordembed-path: Path to pre-trained word embeddings.

**Validation variables**
```
val = True
val-path = '*.csv'
val-period = 1
```

* val: Whether to perform validation.
* val-path: Validation file path. Must follow the same structure of the input 
file.
* val-period: Period to wait until a validation is performed.

**Model variables**
```
word-dim = 300
lstm-dim = 300
lstm-layers = 1
dropout-prob = 0.05
bidirectional = False
epochs = 5
batch-size = 32
shuffle = False
learning-rate = 0.001
learning-rate-decay = 0.1
max-patience = 2
max-decay-num = 2
patience-threshold = 0.98
```

* word-dim: Dimension of word embeddings.
* lstm-dim: Dimensions of lstm cells. This determines the hidden state and cell
state sizes.
* lstm-layers: Number of layers of the lstm cells.
* dropout-prob: Probability in dropout layers.
* bidirectional: Whether lstm cells are bidirectional. 
* epochs: Number of training epochs.
* batch-size: Mini-batch size to train the model.
* shuffle: Whether to shuffle the dataset.
* learning-rate: Learning rate to train the model.
* learning-rate-decay: Learning rate decay after the model not improve.
* max-patience: Number maximum of epochs accept with decreasing loss in 
validation, before reduce the learning rate.
* max-decay-num: Number maximum of times that the learning can be reduced.
* patience-threshold: Threshold of the loss in validation to be considered 
that the model didn't improve.

### Generate the vocabularies 

Generate the sentences vocabulary. This steps is necessary to generate a index 
to each word in the sentences (on train and validation datasets) to retrieve 
information after PyTorch operations. 

```
    pad_string = '<pad>'
    unk_string = '<unk>'
    sentence_vocab = vocab.create_vocabulary(
        input_path=input_path,
        column_name=sentence_column,
        pad_string=pad_string,
        unk_string=unk_string,
        encoding=encoding,
        separator=separator,
        use_pre_processing=use_pre_processing)

    if val:
        sentences = vocab.read_sentences(
            path=val_path,
            column=sentence_column,
            encoding=encoding,
            separator=separator,
            use_pre_processing=use_pre_processing)
        vocab.populate_vocab(sentences, sentence_vocab)
```

Generating the labels vocabulary. To generate a index of each label, this 
object is necessary to predict, so must be saved.

```
    label_vocab = vocab.create_vocabulary(
        input_path=input_path,
        column_name=label_column,
        pad_string=pad_string,
        unk_string=unk_string,
        encoding=encoding,
        separator=separator,
        is_label=True)
    vocab_label_path = os.path.join(save_dir, 
                                    'vocab-label.pkl')
    pickle.dump(label_vocab, open(vocab_label_path, 'wb'))
```

### Initialize the model

Initialize the LSTM model.

```
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    lstm_model = model.LSTM(
        vocab_size=len(sentence_vocab),
        word_dim=word_dim,
        n_labels=len(label_vocab),
        hidden_dim=lstm_dim,
        layers=lstm_layers,
        dropout_prob=dropout_prob,
        device=device,
        bidirectional=bidirectional
    ).to(device)

    lstm_model.reset_parameters()

```

Fill the embedding layer with the representation of each word in the vocabulary.
```
    wordembed_path = wordembed_path
    fasttext = utils.load_fasttext_embeddings(wordembed_path, pad_string)
    lstm_model.embeddings[0].weight.data = torch.from_numpy(
        fasttext[sentence_vocab.i2f.values()])
    lstm_model.embeddings[0].weight.requires_grad = False
```

### Training 
```
    trainer = LSTMTrainer(
        lstm_model=lstm_model,
        epochs=epochs,
        input_vocab=sentence_vocab,
        input_path=input_path,
        label_vocab=label_vocab,
        save_dir=save_dir,
        val=val,
        val_period=val_period,
        pad_string=pad_string,
        unk_string=unk_string,
        batch_size=batch_size,
        shuffle=shuffle,
        label_column=label_column,
        encoding=encoding,
        separator=separator,
        use_pre_processing=use_pre_processing,
        learning_rate=learning_rate,
        learning_rate_decay=learning_rate_decay,
        max_patience=max_patience,
        max_decay_num=max_decay_num,
        patience_threshold=patience_threshold,
        val_path=val_path)
    trainer.train()

```

## Prediction
The prediction can be made for a single sentence or for a batch of sentences.

In both cases a few steps should be followed.

1) Import the main functions
2) Set the variables
3) Initialize the model
4) Predict

### Import main functions
```
import sys
import os
import torch

from TakeSentimentAnalysis import utils
from TakeSentimentAnalysis.predict import SentimentPredict
```

### Set the variables

```
model_path = '*.pkl'
label_vocab = '*.pkl'
save_dir = '*.csv'
encoding = 'utf-8'
separator = '|'
```

* model_path: Path to trained model.
* label_vocab: Path to input file that contains the label vocab.
* save_dir: Directory to save predict.
* encoding: Input file encoding.
* separator: Input file column separator.

### Initialize the model
```
sys.path.insert(0, os.path.dirname(model_path))
lstm_model = torch.load(model_path)

pad_string = '<pad>'
unk_string = '<unk>'

embedding = utils.load_fasttext_embeddings(wordembed_path, 
                                           pad_string)

SentimentPredicter = SentimentPredict(model=lstm_model,
                                      label_path=label_vocab,
                                      embedding=embedding,
                                      save_dir=save_dir,
                                      encoding=encoding,
                                      separator=separator)    
```

### Single Prediction
To predict a single sentence

```
SentimentPredicter.predict_line(line=sentence)
```

### Batch Prediction
To predict in a batch a few more variables are need:

* batch_size: Mini-batch size.
* shuffle: Whether to shuffle the dataset.
* use_pre_processing: Whether to pre-processing the input data.

To predict a batch using dictionary:
````
SentimentPredicter.predict_batch(
        filepath='',
        sentence_column='',
        pad_string=pad_string,
        unk_string=unk_string,
        batch_size=batch_size,
        shuffle=shuffle,
        use_pre_processing=use_pre_processing,
        sentences=[{'id': 1, 'sentence': sentence_1},
                   {'id': 2, 'sentence': sentence_2}]))
````

To predict a batch using a csv file:
```
SentimentPredicter.predict_batch(
            filepath=input_path,
            sentence_column=sentence_column,
            pad_string=pad_string,
            unk_string=unk_string,
            batch_size=batch_size,
            shuffle=shuffle,
            use_pre_processing=use_pre_processing)
```

* input_path: Path to the input file containing the sentences to be predicted.
*  sentence_column: String with the name of the column of sentences to be 
read from input file.
