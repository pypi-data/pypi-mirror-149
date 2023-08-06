import torch.nn as nn
import torch


class LSTM(nn.Module):
    """
    Generate and operate over a LSTM architecture.

    The LSTM architecture used in this class has an embedding layer, a LSTM
    layer (that could be bidirectional), a linear output layer and a softmax
    layer for prediction.

    The embedding layer: will get the embedding representations of a word.

    The LSTM: receives as input the embedding representation of each word,
    and for each word generate a output with size defined by the usage
    (hidden_size).

    The linear output layer: receives as input the last word hidden output of
    the LSTM and applies a linear function to get a vector of the size of the
    possibles labels.

    Softmax layer: receives de output of the linear layer and apply softmax
    operation to get the probability of each label.

    For the bidirectional LSTM the linear output layer receives the hidden
    output from the first (on the direction right-left) and the last word (on
    the direction left-right).

    Methods
    -------
    reset_parameters
        reset all models parameters.
    forward
        forward pass through the layers.
    predict
        predict a label of a sentence.
    update_embedding
        update embedding layer.
    """

    def __init__(self, vocab_size: int, word_dim: int, n_labels: int,
                 hidden_dim: int, layers: int, dropout_prob: float,
                 device: torch.device, bidirectional: bool = False):
        """
        Parameters
        ----------
        vocab_size: int
            size of sentences vocabulary.
        word_dim: int
            dimensions of word embeddings.
        n_labels: int
            number of possibles labels to each sentence.
        hidden_dim: int
            dimensions of lstm cells. This determines the hidden state and cell
            state sizes.
        layers: int
            number of layers in the LSTM.
        dropout_prob: float
            probability in dropout layers.
        device: torch.device
            loads model on CPU or GPU.
        bidirectional: bool
            if True, the LSTM becomes a bidirectional LSTM. Default: False
        """
        super(LSTM, self).__init__()

        self.vocab_size = vocab_size
        self.word_dim = word_dim
        self.hidden_dim = hidden_dim
        self.layers = layers
        self.dropout_prob = dropout_prob
        self.device = device
        self.bidirectional = bidirectional
        self.n_labels = n_labels

        self.output_hidden_dim = hidden_dim

        if bidirectional:
            self.output_hidden_dim *= 2

        self.embeddings = nn.ModuleList(
            [nn.Embedding(vocab_size, word_dim).to(self.device)]).to(
            self.device)

        self.lstm = nn.LSTM(input_size=self.word_dim,
                            hidden_size=self.hidden_dim,
                            num_layers=self.layers,
                            bidirectional=self.bidirectional,
                            dropout=self.dropout_prob,
                            batch_first=True)

        self.output_layer = nn.Linear(self.output_hidden_dim, self.n_labels)
        self.softmax = nn.Softmax(dim=1)

    def reset_parameters(self) -> None:
        """
        Reset all models parameters.
        """
        for emb in self.embeddings:
            nn.init.xavier_normal_(emb.weight.data)

        nn.init.xavier_normal_(self.output_layer.weight.data)
        self.lstm.reset_parameters()

    def _embeddings(self, sequences_batch: torch.Tensor) -> torch.Tensor:
        """
        Get the embedding representation of a batch of sentences.

        Parameters
        ----------
        sequences_batch: torch.Tensor
            tensor of shape (1, batch_size, maximum length sentences) with the
            representation of each word of the sentence in the batch.

        Returns
        -------
        torch.Tensor
            tensor of shape (batch_size,  maximum length sentences, word_dim)
            with the embedding representation of each word of the sentence in
            the batch.
        """
        embedded_sequence_combination = self.embeddings[0].to(self.device)(
            sequences_batch[0].to(self.device))
        return embedded_sequence_combination

    def forward(self, sequence_batch: torch.Tensor, lens: torch.Tensor) -> \
            torch.Tensor:
        """
        Forward pass through the layers.

        Parameters
        ----------
        sequence_batch: torch.Tensor
            tensor of shape (1, batch_size, maximum length sentences) with the
            representation of each word of the sentence in the batch.
        lens: torch.Tensor
            tensor of shape (batch_size) with the length of each sentence in
            the batch.

        Returns
        -------
        torch.Tensor
            tensor of shape (1, batch_size, n_labels) with the output of the
            linear layer for each label. Values of this tensor are real values.
        """

        _, batch_size, seq_len = sequence_batch.size()

        emb_sequence_batch = self._embeddings(sequence_batch)

        hidden = self._run_rnn_packed(emb_sequence_batch, lens)

        if self.bidirectional:
            hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
            hidden = hidden.unsqueeze(dim=0)
        else:
            hidden = hidden[-1].unsqueeze(dim=0)

        output = self.output_layer(hidden)

        return output

    def _run_rnn_packed(self, sequence_batch: torch.Tensor,
                        sequence_batch_len: torch.Tensor) -> torch.Tensor:
        """
        Run rnn neural network in padded sequence.

        This function will run the LSTM layer for padded sequence. This will
        ignore the outputs for the pad token.

        Parameters
        ---------
        sequence_batch: torch.Tensor
            tensor of shape (batch_size,  maximum length sentences, word_dim)
            with the embedding representation of each word of the sentence in
            the batch.
        sequence_batch_len: torch.Tensor
            tensor of shape (batch_size) with the length of each sentence in
            the batch.

        Returns
        -------
        torch.Tensor
            tensor of shape (B*layers, batch_size, hidden_dim) with the last
            hidden output of each sentence in each layer. If is Bi-LSTM B=2,
            else B=1.
        """
        sequence_batch_packed = nn.utils.rnn.pack_padded_sequence(
            sequence_batch,
            sequence_batch_len.data.tolist(),
            batch_first=True)

        _, (hidden, _) = self.lstm(sequence_batch_packed)
        return hidden

    def predict(self, sequences: torch.Tensor,
                lens: torch.Tensor) -> torch.Tensor:
        """Predict the label of a batch of sentences

        Parameters
        ----------
        sequences: torch.Tensor
            tensor of shape (batch_size,  maximum length sentences, word_dim)
            with the embedding representation of each word of the sentence in
            the batch.

        lens: torch.Tensor
            tensor of shape (batch_size) with the length of each sentence in
            the batch.

        Return
        ------
        torch.Tensor
             tensor of shape (batch_size) with the the prediction of each
             sentence in the batch.

        """
        output_lstm = self.forward(sequences, lens)

        return self.softmax(output_lstm[0, :]).argmax(dim=1)

    def reset_embedding(self, vocab_size: int) -> None:
        """Reset the embedding layer to fit a new vocabulary

        The vocab size will set the new dimensions of the Embedding Layer

        Parameters
        ----------
        vocab_size: int
            Length of the vocabulary
        """
        self.embeddings = nn.ModuleList(
            [nn.Embedding(vocab_size, self.word_dim).to(self.device)]
        ).to(self.device)
