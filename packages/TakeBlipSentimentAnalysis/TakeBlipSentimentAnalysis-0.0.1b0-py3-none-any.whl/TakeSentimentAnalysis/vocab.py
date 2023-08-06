import os
import pickle
import csv
import typing as tp
from take_text_preprocess.presentation import pre_process

from .constants import PREPROCESS_OPTION


class Vocabulary:
    """ Create and manipulate a object with the vocabulary of sentences.

    The two dictionaries used in the vocabulary are:

    * f2i: feature (word) to index
    * i2f: index to feature (word)

    """

    def __init__(self):
        self.f2i = {}
        self.i2f = {}

    def add(self, word: str) -> None:
        """Add word to the vocabulary

        Parameters
        ----------
        word: str
            Word to be add to the vocabulary.

        """
        if word not in self.f2i:
            idx = len(self.f2i)
            self.f2i[word] = idx
            self.i2f[idx] = word

    def get(self, item: tp.Any, value: tp.Any) -> tp.Any:
        """Get a value of a key

        Parameters
        ----------
        item: tp.Any
            Key value to be used in search.
        value: tp.Any
            Value to be return if the key doesn't exist.

        Return
        ------
        tp.Any
            Key value founded or the parameter value.
        """
        if isinstance(item, int):
            return self.i2f.get(item, value)
        elif isinstance(item, str):
            return self.f2i.get(item, value)
        elif hasattr(item, '__iter__'):
            return [self[ele] for ele in item]
        else:
            raise ValueError(f'Unknown type: "{type(item)}')

    def __getitem__(self, item: tp.Any):
        if isinstance(item, int):
            return self.i2f[item]
        elif isinstance(item, str):
            return self.f2i[item]
        elif hasattr(item, '__iter__'):
            return [self[ele] for ele in item]
        else:
            raise ValueError(f'Unknown type: "{type(item)}"')

    def __contains__(self, item: tp.Any):
        return item in self.f2i or item in self.i2f

    def __len__(self):
        return len(self.f2i)


def populate_vocab(sentences: list, vocab: Vocabulary) -> None:
    """Populate a vocabulary based on list of sentences.

    Parameters
    ----------
    sentences: list
        A list with the sentences to generate the vocabulary.
    vocab: Vocabulary
        Vocabulary to be populate.
    """
    for sentence in sentences:
        for word in sentence:
            vocab.add(word)


def line_pre_process(line: str, use_pre_processing: bool) -> tp.List[str]:
    """Process a string

    Parameters
    ----------
    line: str
        String to be processed.
    use_pre_processing: bool.
        Use or not the pre process on the sentences. If False, the sentence
        will only be split

    Return
    ------
    tp.List[str]
        A list with all the words in the line (processed or not).
    """
    if use_pre_processing:
        return pre_process(line, PREPROCESS_OPTION).split()
    else:
        return line.split()


def create_vocabulary(input_path: str, column_name: str, pad_string: str,
                      unk_string: str, encoding: str, separator: str,
                      use_pre_processing: bool = False, is_label: bool = False,
                      sentences: list = None) -> Vocabulary:
    """Create a vocabulary object based on sentences.

    Parameters
    ----------
    input_path: str
        String with the path to the dataframe.
    column_name: str
        Name of the column with the sentences.
    pad_string: str
        String that represents pad.
    unk_string: str
        String that represent unknown.
    encoding: str
        Encoding of the dotaframe.
    separator: str
        Separator of the columns in the dataframe.
    use_pre_processing: bool
        Use or not the pre processing in the sentences.
    is_label: bool
        The vocabulary is a label vocabulary. Default: False.
    sentences: list
        List with the sentences to generate the vocabulary. If input_path is
        not empty, this argument is not required. Default: None.

    Returns
    -------
    Vocabulary
        Return the vocabulary generated from the sentences.

    """
    vocabulary = Vocabulary()

    if is_label:
        use_pre_processing = False
    else:
        vocabulary.add(pad_string)
        vocabulary.add(unk_string)

    if sentences:
        sentences = [line_pre_process(sentence['sentence'], use_pre_processing)
                     for sentence in sentences]
    else:
        sentences = read_sentences(input_path, column_name, encoding,
                                   separator, use_pre_processing)
    populate_vocab(sentences, vocabulary)
    return vocabulary


def save_vocabulary(save_path: str, input_vocab: Vocabulary,
                    file_name: str) -> None:
    """Save vocabularies in a pickle file.

    Parameters
    ----------
    save_path: str
        Path to the folder where the vocabulary will be saved.
    input_vocab: Vocabulary
        Vocabulary to be saved.
    file_name: str
        Name of the file.
    """
    vocab_path = os.path.join(save_path, file_name)
    pickle.dump(input_vocab, open(vocab_path, 'wb'))


def read_sentences(path: str, column: str, encoding: str, separator: str,
                   use_pre_processing: bool) -> tp.List[str]:
    """ Read sentences of a csv file

    Parameters
    ---------
    path: str
        Path to the file
    column: str
        Name of the column with the sentences
    encoding: str
        File encoding
    separator: str
        File column separator
    use_pre_processing: bool
        Use or not the pre processing in the sentences.

    Return
    ------
    tp.List[tp.List[str]]
        Returns a list with all the sentences splitted.

    """
    with open(path, newline='', encoding=encoding) as file:
        reader = csv.DictReader(file, delimiter=separator)
        if use_pre_processing:
            for line in reader:
                yield pre_process(line[column], PREPROCESS_OPTION).split()
        else:
            for line in reader:
                yield line[column].split()
