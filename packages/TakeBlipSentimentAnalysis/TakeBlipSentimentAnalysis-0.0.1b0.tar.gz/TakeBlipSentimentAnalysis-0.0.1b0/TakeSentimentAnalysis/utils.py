import torch
import torch.autograd as autograd
import csv
import typing as tp

from torch import Tensor
from gensim.models import KeyedVectors
from gensim.models.keyedvectors import FastTextKeyedVectors
from take_text_preprocess.presentation import pre_process as pp

from .constants import PREPROCESS_OPTION
from .vocab import Vocabulary


def load_fasttext_embeddings(path: str, pad: str) -> FastTextKeyedVectors:
    """Load fasttext model and add pad representation

    Parameters
    ----------
    path: str
        Path to the fasttext embedding file
    pad: str
        String that represents pad.

    Return
    ------
    FastTextKeyedVectors
        Loaded embedding model
    """
    fasttext = KeyedVectors.load(path, mmap=None)
    fasttext.add(pad, [0] * fasttext.vector_size, replace=True)
    return fasttext


def prepare_batch(sentences: Tensor, labels: Tensor, sentences_length: Tensor,
                  index: Tensor = None) -> tp.Tuple[Tensor,
                                                    Tensor,
                                                    Tensor]:
    """Prepare batch for training sorting by length

    Parameters
    ----------
    sentences: Tensor
        tensor of shape (1, batch_size, maximum length sentences) with the
        representation of each word of the sentence in the batch.
    labels: Tensor
        tensor of shape (1, batch_size, 1) with the label of each sentence in
        the batch.
    sentences_length: Tensor
        tensor of shape (batch_size) with the length of each sentence in the
        batch.
    index: Tensor
        tensor of shape (batch_size) with the index of each sentence in the
        batch.

    Return
    ------
    tp.Tuple[Tensor, Tensor, Tensor]
        Return the input tensor ordered by the length of the sentence. The
        first tensor is the sentences, the second is either the labels or the
        index, and the last is the lens tensor.
    """
    sentences_length, idx = torch.sort(sentences_length, 0, True)
    if labels is not None:
        sentences, labels = sentences[:, idx], labels[:, idx]
        labels = autograd.Variable(labels)
    elif index is not None:
        sentences, labels = sentences[:, idx], index[idx]
    else:
        sentences = sentences[:, idx]

    sentences = autograd.Variable(sentences)
    sentences_length = autograd.Variable(sentences_length)
    return sentences, labels, sentences_length


def tighten(sequences: list, sentences_length: torch.Tensor) -> list:
    """Tighten each sentence removing the pad

    Parameters
    ----------
    sequences: list
        List with the sentences.
    sentences_length: torch.Tensor
        tensor of shape (batch_size) with the length of each sentence in
        the batch.

    Return
    ------
    list
        List with the unpadded sequence.
    """
    return [sequence[:seq_len] for sequence, seq_len in zip(sequences, sentences_length)]


def get_words_by_id(sentence: list, vocab: Vocabulary) -> list:
    """Get the words in a sequence by their id

    Parameters
    ----------
    sentence: list
        List with the words id in a sentence.
    vocab: Vocabulary
        Vocabulary with the relation id-word.

    Return
    ------
    list
        A list with the word in input sentence.
    """

    return [vocab.get(ind, '<unk>') for ind in sentence]


def get_words_id(sentence: list, vocab: Vocabulary) -> list:
    """Get the id of the words in a sequence

    Parameters
    ----------
    sentence: list
        List of word tokens in a sentence.
    vocab: Vocabulary
         Vocabulary with the relation word-id.

    Return
    ------
    list
        A list with the index of the words in input sentence.
    """
    if '<unk>' in vocab.f2i:
        unk_index = vocab.f2i['<unk>']
    else:
        unk_index = None

    return [vocab.get(word, unk_index) for word in sentence]


def get_sequence_words_by_id(sequences: list, lens: torch.Tensor,
                             vocab: Vocabulary) -> list:
    """Get the words of sentences in a batch

    The list of sentences with the index of the words is shortened removing the
    pads and the index is converted to the word.

    Parameters
    ----------
    sequences: list
        List with the sentences in a batch.
    lens: torch.Tensor
        tensor of shape (batch_size) with the length of each sentence in
        the batch.
    vocab: Vocabulary
        Vocabulary of the sentences to get the words by the id

    Return
    ------
    list
        List with the sequence with the words and pad removed.
    """
    return [get_words_by_id(sequence, vocab) for sequence in
            tighten(sequences, lens)]


def pre_process(sentence: str) -> str:
    """Pre process a line

    Parameters
    ----------
    sentence: str
        Sentence to be processed

    Return
    ------
    str
        Processed sentence

    """
    return pp(sentence, PREPROCESS_OPTION)


def create_save_file(path: str) -> None:
    """Create the file here the predictions will be saved

    The file will be generated and the first line will be completed with two
    columns Sentence and Label, separated by '|'.

    Parameters
    ----------
    path: str
        String with the path to te file.
    """
    with open(path, 'w') as file:
        writer = csv.writer(file, delimiter='|', lineterminator='\n')
        writer_parameter = ['Sentence', 'Label']
        writer.writerow(writer_parameter)


def save_predict(path: str, sequence: list, pred: list) -> None:
    """Save the predictions of a dataset in a file

    Parameters
    ----------
    path: str
        String with the path to the file.
    sequence: list
        A list with the sentences used in prediction.
    pred: list
        A list with the prediction for each sentence in sequence.
    """
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter='|', lineterminator='\n')
        writer_parameter = zip([' '.join(k) for k in sequence],
                               [k for k in pred])
        for row in writer_parameter:
            writer.writerow(row)
