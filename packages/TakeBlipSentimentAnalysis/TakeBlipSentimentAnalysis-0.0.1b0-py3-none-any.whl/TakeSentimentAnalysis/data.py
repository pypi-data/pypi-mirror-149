import csv
import torch
import sys
import typing as tp

from torch.utils.data import DataLoader, Dataset, IterableDataset
from take_text_preprocess.presentation import pre_process

from .constants import PREPROCESS_OPTION

STRING_LIST = tp.List[str]


class ModelIterableDatasetCSV(IterableDataset):
    """
    An iterable dataset to csv files.
    """

    def __init__(self, path: str, label_column: tp.Optional[str],
                 encoding: str, separator: str,
                 use_pre_processing: bool = False):
        """
        Parameters
        ----------
        path: str
            Path of the dataset.
        label_column: tp.Optional[str]
            Name of the column with the labels. If label column is none, the
            function to treat the line will be for prediction.
        encoding: str
            Encoding of the dataset.
        separator: str
            Separator of the columns in the dataset.
        use_pre_processing: bool
            Whether to pre process input data.
        """
        self.__set_file_iterable(path, encoding, separator)
        self.__set_process(use_pre_processing)
        self.line_mapper = self.line_mapper_training if label_column else self.line_mapper_predicting

    def __set_file_iterable(self, path: str, encoding: str,
                            separator: str) -> None:
        """
        Set the iterable of the dataset

        Parameters
        ----------
        path: str
            Path of the dataset.
        encoding: str
            Encoding of the dataset.
        separator: str
            Separator of the columns in the dataset.
        """
        self.file_pointer = open(path, encoding=encoding)
        self.file_iterable = csv.reader(self.file_pointer, delimiter=separator)
        next(self.file_iterable)

    def __set_process(self, use_pre_processing: bool) -> None:
        """
        Set the process of the sentences.

        If use_pre_processing is True the line will be processed and splitted,
        else the line will only be splitted.

        Parameters
        ----------
        use_pre_processing: bool
            Whether to pre process the sentences.
        """
        if use_pre_processing:
            self.process = self.line_pre_process
        else:
            self.process = self.split_sentence

    def close_file(self) -> None:
        """ Close file pointer
        """
        self.file_pointer.close()

    def line_mapper_training(self, line: STRING_LIST) -> tp.List[STRING_LIST]:
        """Define mapper of the training dataset

        In the train dataset the line has two columns. The first is the line
        is the sentence and the second is the label.

        Parameters
        ----------
        line: STRING_LIST
            Line of the dataset.

        Return
        ------
        tp.List[STRING_LIST]
            A list with the sentence processed and splitted and the label
            splitted.
        """
        return [self.process(line[0]), self.split_sentence(line[1])]

    def line_mapper_predicting(self, line: STRING_LIST) -> tp.List[
        STRING_LIST]:
        """Define mapper of the predict dataset

        Parameters
        ----------
        line: STRING_LIST
            Line of the dataset.

        Return
        ------
        tp.List[STRING_LIST]
            A list with the sentence processed and splitted.
        """
        return [self.process(line[0])]

    @staticmethod
    def line_pre_process(sentence: str) -> STRING_LIST:
        """
        Process and split the line

        Parameters
        ---------
        sentence: str
            Sentence to be processed

        Return
        ------
        STRING_LIST
            The sentence processed and splitted.
        """
        return pre_process(sentence, PREPROCESS_OPTION).split()

    @staticmethod
    def split_sentence(sentence: str) -> STRING_LIST:
        """
        Split the line

        Parameters
        ---------
        sentence: str
            Sentence to be processed

        Return
        ------
        STRING_LIST
            The sentence splitted.
        """
        return sentence.split()

    def __iter__(self):
        file_iter = self.file_iterable
        return map(self.line_mapper, file_iter)

    def __len__(self):
        return 1


class ModelBatchDataset(Dataset):
    """
    A dataset based on a list with a batch of sentences.
    """
    def __init__(self, use_pre_processing: bool, sentences: list):
        """
        Parameters
        ----------
        use_pre_processing: bool
            Whether to pre process input data
        sentences: list
            A list of dictionaries with the id of the sentence and
            the sentence.
        """
        self.use_pre_processing = use_pre_processing
        self.sentences = sentences
        self.__set_default_process()

    @staticmethod
    def line_pre_process(sentence: str) -> STRING_LIST:
        """
        Process and split the line

        Parameters
        ---------
        sentence: str
            Sentence to be processed

        Return
        ------
        STRING_LIST
            The sentence processed and splitted.
        """
        return pre_process(sentence, PREPROCESS_OPTION).split()

    @staticmethod
    def split_sentence(sentence: str) -> STRING_LIST:
        """
        Split the line

        Parameters
        ---------
        sentence: str
            Sentence to be processed

        Return
        ------
        STRING_LIST
            The sentence splitted.
        """
        return sentence.split()

    def __set_default_process(self):
        """Set the process of the sentences.

        If use_pre_processing is True the line will be processed and splitted,
        else the line will only be splitted.
        """
        if self.use_pre_processing:
            self.process = self.line_pre_process
        else:
            self.process = self.split_sentence

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx: int):
        return [self.process(self.sentences[idx]['sentence']),
                int(self.sentences[idx]['id'])]


class ModelDataLoader(DataLoader):
    """
    Wraps loader dataset functions
    """
    def __init__(self, dataset: tp.Union[ModelIterableDatasetCSV,
                                         ModelBatchDataset],
                 vocabs: list, pad_string: str, unk_string: str,
                 use_index: bool = False, is_train: bool = False, **kwargs):
        """
        Parameters
        ---------
        dataset: tp.Union[ModelIterableDatasetCSV, MultiSentWordBatchDataset]
            Dataset to be loaded
        vocabs: list
            List of vocabularies generated of the dataset
        pad_string: str
            String that represents pad.
        unk_string: str
            String that represent unknown.
        use_index: bool
            Whether to use sentence index. Default: False
        is_train
            Whether is train or predict dataset. Default:False
        """
        super(ModelDataLoader, self).__init__(
            dataset=dataset,
            collate_fn=self.collate_fn,
            **kwargs
        )

        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu")
        self.pad_string = pad_string
        self.unk_string = unk_string
        self.vocabs = vocabs
        self.use_index = use_index
        self.is_train = is_train

    def get_words_id(self, sentence: list) -> list:
        """Get the vocabulary index of each word

        Parameters
        ----------
        sentence: list
            List with each token of the sentence to be indexed.

        Return
        ------
        list
            List with the indexed tokens of the sentence.
        """
        if self.unk_string in self.vocab.f2i:
            unk_idx = self.vocab.f2i[self.unk_string]
        else:
            unk_idx = None
        return [self.vocab.get(word, unk_idx) for word in sentence]

    def pad(self, sentence: list) -> list:
        """Pad a sentence

        Parameters
        ----------
        sentence: list
            List with each token of the sentence to be padded.

        Return
        ------
        list
            List with the tokens of the padded sentence.
        """
        return sentence + [self.vocab.f2i[self.pad_string]] * (
                self.max_len - len(sentence))

    def pad_sequence(self, sentence_list: list, vocabs: list) -> torch.Tensor:
        """ Get a padded tensor of the sentences

        Parameters
        ----------
        sentence_list: list
            List with the sentences information to be padded.
        vocabs: list
            List with the vocabularies of each information.

        Return
        ------
        torch.Tensor
            tensor of shape (1, batch_size, maximum length sentences) with the
            representation of each word of the sentence in the batch

        """
        sequences_collation = []
        for sentences, vocab in zip(sentence_list, vocabs):
            self.vocab = vocab
            sentences = map(self.pad, map(self.get_words_id, sentences))
            sequences_collation.append(
                torch.LongTensor(list(sentences)).unsqueeze(0))
        return sequences_collation

    def get_sequence_collation(self, sentences_list: list,
                               is_train: bool) -> tp.Tuple[torch.Tensor,
                                                           torch.Tensor]:
        """ Get the tensors of the sequence and the labels

        Parameters
        ----------
        sentences_list: list
            List with the sentence information
        is_train: bool
            Whether the dataset will be loaded in train ou predict.

        Return
        ------
        tp.Tuple[torch.Tensor, torch.Tensor]
            tensor of shape (1, batch_size, maximum length sentences) with the
            representation of each word of the sentence in the batch; tensor of
            shape (1, batch_size, 1) with the label of each sentence in the
            batch;
        """
        if is_train:
            sequences_collation = self.pad_sequence(sentences_list[:-1],
                                                    self.vocabs[:-1])
            self.vocab = self.vocabs[-1]
            labels = map(self.get_words_id, sentences_list[-1])
            labels = torch.LongTensor(list(labels)).unsqueeze(0)
            return sequences_collation, labels
        else:
            sequences_collation = self.pad_sequence(sentences_list,
                                                    self.vocabs)
            return sequences_collation, None

    def collate_fn(self, batches: list) -> tp.Tuple[torch.Tensor, torch.Tensor,
                                                    torch.Tensor, torch.Tensor]:
        """
        Function to collate all information in a batch of sentences

        Parameters
        ----------
        batches: list
            Batches of sentences

        Return
        ------
        tp.Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]
            tensor of shape (1, batch_size, maximum length sentences) with the
            representation of each word of the sentence in the batch; tensor of
            shape (batch_size) with the length of each sentence in the batch;
            tensor of shape (1, batch_size, 1) with the label of each sentence
            in the batch; tensor of shape (batch_size) with the index of each
            sentence in the batch;

        """
        batches = filter(lambda x: len(x[0]) > 0, batches)
        sentences_list = list(zip(*batches))
        lens = [len(sentence) for sentence in sentences_list[0]]
        self.max_len = max(lens)
        sequences_collation, labels = self.get_sequence_collation(
            sentences_list,
            self.is_train)
        sequence_tensor = torch.cat(sequences_collation).to(self.device)
        lens_tensor = torch.LongTensor(lens).to(self.device)
        if self.use_index:
            index_tensor = torch.LongTensor(sentences_list[-1]).to(self.device)
            return sequence_tensor, lens_tensor, labels, index_tensor
        else:
            return sequence_tensor, lens_tensor, labels, None


maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)
