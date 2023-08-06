import os
import typing as tp
import torch

from TakeSentimentAnalysis import model, utils, data, vocab, mlflowlogger


class LSTMTrainer(object):
    """
    Wraps all train functions
    """

    def __init__(self, lstm_model: model.LSTM, input_vocab: vocab.Vocabulary,
                 input_path: str, label_vocab: vocab.Vocabulary, save_dir: str,
                 val: bool, val_period: int, pad_string: str, unk_string: str,
                 batch_size: int, shuffle: bool, label_column: str,
                 encoding: str, separator: str, use_pre_processing: bool,
                 learning_rate: float, learning_rate_decay: float,
                 max_patience: int, max_decay_num: int,
                 patience_threshold: float, epochs: int, model_name: str,
                 val_path: str = None):
        """
        Parameters
        ----------
        lstm_model: model.LSTM
            LSTM model to be trained.
        input_vocab: vocab.Vocabulary
            Vocabulary of the sentences in train dataset.
        input_path: str
            Path of the train dataset.
        label_vocab: vocab.Vocabulary
            Vocabulary of the labels in train dataset.
        save_dir: str
            Path to the directory to save the model and validation predictions.
        val: bool
            Whether to perform validation.
        val_period: int
            Period to wait until a validation is performed. In epochs.
        pad_string: str
            String that represents pad.
        unk_string: str
            String that represent unknown.
        batch_size: int
            Mini-batch size to train the model.
        shuffle: bool
            Whether to shuffle the dataset.
        label_column: str
            Name of the column with the labels.
        encoding: str
            Encoding of the dataset.
        separator: str
            Separator of the columns in the dataset.
        use_pre_processing: bool
            Whether to pre process input data.
        learning_rate: float
            Learning rate to train the model.
        learning_rate_decay: float
            Learning rate decay after the model not improve.
        max_patience: int
            Number maximum of epochs accept with decreasing loss in validation,
            before reduce the learning rate.
        max_decay_num: int
            Number maximum of times that the learning can be reduced.
        patience_threshold: float
            Threshold of the loss in validation to be considered that the model
            didn't improve.
        epochs: int
            Number of epochs to train the model.
        model_name: str
            Model name to be logged
        val_path: str
            Path of the validation dataset.
        """
        self.model = lstm_model
        self.epochs = epochs
        self.optimizer = torch.optim.Adam(self.model.parameters(),
                                          learning_rate)
        self.save_dir = save_dir
        self.input_vocab = input_vocab
        self.label_vocab = label_vocab
        self.input_path = input_path
        self.val_path = val_path
        self.val = val
        self.encoding = encoding
        self.label_column = label_column
        self.separator = separator
        self.use_pre_processing = use_pre_processing
        self.pad_string = pad_string
        self.unk_string = unk_string
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.patience_threshold = patience_threshold
        self.max_patience = max_patience
        self.max_decay_num = max_decay_num
        self.learning_rate_decay = learning_rate_decay
        self.val_period = val_period
        self.model_name = model_name
        self.validation_number = 0

        self.min_dev_loss = float('inf')
        self.patience = 0
        self.decay_num = 0
        self.logic_break = False
        self.loss_function = torch.nn.CrossEntropyLoss()

    def load_data(self, train: bool) -> data.ModelDataLoader:
        """
        Load dataset to be use in the train iterator.

        Parameters
        ---------
        train: bool
            Whether te dataset is a train or validate dataset.

        Return
        ------
        data.ModelDataLoader
            DataLoader to be iterate training the model.
        """
        path = self.input_path if train else self.val_path

        dataset = data.ModelIterableDatasetCSV(
            path=path,
            label_column=self.label_column,
            encoding=self.encoding,
            separator=self.separator,
            use_pre_processing=self.use_pre_processing)

        dataloader = data.ModelDataLoader(
            dataset=dataset,
            vocabs=[self.input_vocab] + [self.label_vocab],
            pad_string=self.pad_string,
            unk_string=self.unk_string,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            is_train=True)

        return dataloader

    def save_model(self) -> None:
        """
        Save the trained model
        """
        save_path = os.path.join(self.save_dir, 'model.pkl')
        torch.save(self.model, save_path)

    def train(self) -> None:
        """
        Train the model and validate the model
        """
        self.model.train(True)
        global_iter = 0

        for epoch_idx in range(self.epochs):
            epoch_idx += 1
            train_data = self.load_data(train=True)
            for iteration_idx, (batch, lens, labels, _) in enumerate(
                    train_data):
                global_iter += 1
                self.model.zero_grad()

                batch_sentences, batch_labels, batch_lens = utils.prepare_batch(
                    batch, labels, lens)

                lstm_output = self.model.forward(batch_sentences, batch_lens)
                loss = self.loss_function(lstm_output[0, :],
                                          batch_labels.view(-1))
                mlflowlogger.save_metric('CrossEntropyLoss', loss.item())
                mlflowlogger.save_system_metrics()
                loss.backward()
                self.optimizer.step()

            train_data.dataset.close_file()
            if self.val and epoch_idx % self.val_period == 0:
                self.validate()
                self.model.train(True)

            if self.logic_break:
                self.save_model()
                break
        mlflowlogger.save_model(self.model, self.model_name)
        mlflowlogger.save_param('Final iteration', global_iter)
        self.save_model()

    def get_unindex_output(self, batch: list, labels: list,
                           lens: torch.Tensor) -> tp.Tuple[list, list]:
        """
        Get the unindex sequence and labels.

        Parameters
        ----------
        batch: list
            List with the sentences in a batch.
        labels: list
            List with the labels of the sentences in a batch.
        lens: torch.Tensor
            tensor of shape (batch_size) with the length of each sentence in
            the batch.

        Return
        ------
        tp.Tuple[list, list]
            List with the list of tokens in the sentences. List with the labels
            of the sentences.

        """
        unindex_label = [self.label_vocab[label] for label in labels]

        unidex_sequence = utils.get_sequence_words_by_id(batch,
                                                         lens,
                                                         self.input_vocab)

        return unidex_sequence, unindex_label

    def save_output_validation(self, path: str, batch: list, labels: list,
                               lens: torch.Tensor) -> None:
        """Save output of the predict in validation

        Parameters
        ----------
        path: str
            Path to save the validation prediction file.
        batch: list
            List with the sentences in a batch.
        labels: list
            List with the labels of the sentences in a batch.
        lens: torch.Tensor
            tensor of shape (batch_size) with the length of each sentence in
            the batch.
        """
        unindex_sequence, unindex_label = self.get_unindex_output(batch,
                                                                  labels,
                                                                  lens)
        utils.save_predict(path, unindex_sequence, unindex_label)

    def validate(self) -> None:
        """
        Validate the model and check the progress in the loss
        """
        path = os.path.join(self.save_dir, 'predict_validation.csv')
        utils.create_save_file(path)
        self.model.train(False)
        data_size = 0
        val_data = self.load_data(train=False)
        nb_classes = len(self.label_vocab)
        confusion_matrix = torch.zeros(nb_classes, nb_classes)
        loss = 0
        for i_idx, (batch, lens, labels, _) in enumerate(val_data):
            i_idx += 1
            batch_size = batch.size(1)
            data_size += batch_size

            with torch.no_grad():
                batch_sentences, batch_labels, batch_lens = utils.prepare_batch(
                    batch, labels, lens)
                lstm_output = self.model.forward(batch_sentences, batch_lens)
                loss += self.loss_function(lstm_output[0, :],
                                           batch_labels.view(-1))
                preds = self.model.predict(batch_sentences, batch_lens)

                pred_list = preds.data.tolist()
                sentences_list = batch_sentences.data.tolist()[0]

                self.save_output_validation(path, sentences_list,
                                            pred_list, batch_lens)

                for true, pred in zip(batch_labels.view(-1),
                                      preds.view(-1)):
                    confusion_matrix[true.long(), pred.long()] += 1

        val_data.dataset.close_file()
        loss = loss / data_size
        self.check_loss(loss)

        mlflowlogger.save_metric('CrossEntropyLossValidation', loss.item())
        mlflowlogger.save_confusion_matrix_from_tensor(
            confusion_matrix=confusion_matrix,
            labels=list(self.label_vocab.f2i.keys()),
            current_epoch=self.validation_number,
            save_dir=self.save_dir
        )
        mlflowlogger.save_metrics(confusion_matrix,
                                  list(self.label_vocab.f2i.keys()))
        self.validation_number += 1
        print(confusion_matrix)

    def check_loss(self, loss: torch.Tensor) -> None:
        """Check if the loss decayed from previous value

        Parameters
        ----------
        loss: torch.Tensor
            Actual loss value
        """
        if loss < (self.min_dev_loss * self.patience_threshold):
            self.min_dev_loss = loss
            self.patience = 0
        else:
            self.patience += 1
            if self.patience == self.max_patience:
                self.decay_num += 1
                if self.decay_num == self.max_decay_num:
                    self.logic_break = True
                learning_rate = self.optimizer.param_groups[0][
                                    'lr'] * self.learning_rate_decay
                self.optimizer.param_groups[0]['lr'] = learning_rate
                self.patience = 0
