"""A BERT Binary Classification neural network model."""
import datetime
import random
import time
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import train_test_split

from facilyst.models import ModelBase
from facilyst.utils import import_errors_dict, import_or_raise


def format_time(time_: float) -> str:
    """Formats the passed time.

    :param time_: The time.
    :type time_: float
    :return: The formatted time in seconds.
    :rtype str:
    """
    time_ = int(round(time_))
    return str(datetime.timedelta(seconds=time_))


class BERTBinaryClassifier(ModelBase):
    """The BertForSequenceClassification model (via transformers' implementation).

    This is a pretrained bidirectional encoder.

    :param batch_size: The number of observations to use in each batch. Defaults to 30.
    :type batch_size: int, optional
    :param seed_val: Value of the random seed. Defaults to 42.
    :type activation: int, optional
    """

    name: str = "BERT Binary Classifier"

    primary_type: str = "classification"
    secondary_type: str = "neural"
    tertiary_type: str = "nlp"

    hyperparameters: dict = {}

    def __init__(
        self, batch_size: Optional[int] = 30, seed_val: Optional[int] = 42, **kwargs
    ) -> None:
        self.predictions = None
        self.mcc = None
        self.scheduler = None
        self.optimizer = None
        self.max_sentence_length = None
        self.tokenizer = None
        self.batch_size = batch_size
        self.seed_val = seed_val
        parameters = {}
        parameters.update(kwargs)

        self.torch = import_or_raise("torch", import_errors_dict["torch"])
        self.kp = import_or_raise(
            "keras_preprocessing", import_errors_dict["keras_preprocessing"]
        )
        self.transformers = import_or_raise(
            "transformers", import_errors_dict["transformers"]
        )

        question_answering_model = (
            self.transformers.BertForSequenceClassification.from_pretrained(
                "bert-base-uncased",
                num_labels=2,
                output_attentions=False,
                output_hidden_states=False,
            )
        )

        super().__init__(model=question_answering_model, parameters=parameters)

    def encode(self, sentences: pd.Series) -> list:
        """Encode all sentences.

        :param sentences: Collection of sentences.
        :type sentences: pd.Series
        :return: Encoded sentences.
        :rtype list:
        """
        input_ids = []
        for sent in sentences:
            encoded_sent = self.tokenizer.encode(sent)
            input_ids.append(encoded_sent)
        return input_ids

    def set_max_length(self, input_ids: list) -> None:
        """Set the maximum sentence length.

        :param input_ids: List of encoded sentences.
        :type input_ids: list
        """
        self.max_sentence_length = max([len(sen) for sen in input_ids])

    def pad_sequences(self, input_ids: list) -> np.ndarray:
        """Pad all sentences.

        :param input_ids: List of encoded sentences.
        :type input_ids: list
        :return: Numpy array with shape `(len(input_ids), self.max_sentence_length)`.
        :rtype np.ndarray:
        """
        from keras_preprocessing.sequence import pad_sequences

        return pad_sequences(
            input_ids,
            maxlen=self.max_sentence_length,
            dtype="long",
            value=0,
            truncating="post",
            padding="post",
        )

    @staticmethod
    def _get_attention_masks(input_ids_padded: np.ndarray) -> np.ndarray:
        attention_masks = []
        for sent in input_ids_padded:
            att_mask = [int(token_id > 0) for token_id in sent]
            attention_masks.append(att_mask)
        return np.array(attention_masks)

    @staticmethod
    def _split_train_val(features: np.ndarray, target: np.ndarray) -> list:
        return train_test_split(features, target, random_state=0, test_size=0.1)

    def get_train_dataloader(
        self,
        train_inputs,
        train_masks,
        train_labels,
    ):
        """Get DataLoader for training data.

        :param train_inputs: Tensor of padded input ids for training.
        :type train_inputs: torch.tensor
        :param train_masks: Tensor of attention masks for training.
        :type train_masks: torch.tensor
        :param train_labels: Tensor of labels for training.
        :type train_labels: torch.tensor
        :return: DataLoader for the training data.
        :rtype DataLoader:
        """
        train_data = self.torch.utils.data.TensorDataset(
            train_inputs, train_masks, train_labels
        )
        train_sampler = self.torch.utils.data.RandomSampler(train_data)
        train_dataloader = self.torch.utils.data.DataLoader(
            train_data, sampler=train_sampler, batch_size=self.batch_size
        )
        return train_dataloader

    def get_validation_dataloader(
        self,
        validation_inputs,
        validation_masks,
        validation_labels,
    ):
        """Get DataLoader for validation data.

        :param validation_inputs: Tensor of padded input ids for validation.
        :type validation_inputs: torch.tensor
        :param validation_masks: Tensor of attention masks for validation.
        :type validation_masks: torch.tensor
        :param validation_labels: Tensor of labels for validation..
        :type validation_labels: torch.tensor
        :return: DataLoader for the validation data.
        :rtype DataLoader:
        """
        validation_data = self.torch.utils.data.TensorDataset(
            validation_inputs, validation_masks, validation_labels
        )
        validation_sampler = self.torch.utils.data.SequentialSampler(validation_data)
        validation_dataloader = self.torch.utils.data.DataLoader(
            validation_data, sampler=validation_sampler, batch_size=self.batch_size
        )
        return validation_dataloader

    def get_optimizer(self):
        """Get the optimizer.

        :return: Optimizer for the model parameters.
        :rtype transformers.AdamW:
        """
        return self.transformers.AdamW(self.model.parameters(), lr=2e-5, eps=1e-8)

    def _set_seeds(self) -> None:
        random.seed(self.seed_val)
        np.random.seed(self.seed_val)
        self.torch.manual_seed(self.seed_val)

    def train_batch(self, batch: list, total_loss: int) -> float:
        """Train batch.

        :param batch: Batch of padded input ids for training.
        :type batch: list
        :param total_loss: Total loss.
        :type total_loss: int
        :return: DataLoader for the validation data.
        :rtype float:
        """
        b_input_ids = batch[0]
        b_input_mask = batch[1]
        b_labels = batch[2]

        # self.model.zero_grad()

        # noinspection PyCallingNonCallable
        outputs = self.model(
            b_input_ids,
            token_type_ids=None,
            attention_mask=b_input_mask,
            labels=b_labels,
        )

        loss = outputs[0]
        total_loss += loss.item()
        loss.backward()
        self.torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        self.scheduler.step()
        return total_loss

    def validate_batch(
        self, batch: list, eval_accuracy: float, nb_eval_steps: int
    ) -> Tuple[float, int]:
        """Validate batch.

        :param batch: Batch of padded input ids for validation.
        :type batch: list
        :param eval_accuracy: Evaluation accuracy.
        :type eval_accuracy: float
        :param nb_eval_steps: Number of evaluation steps.
        :type nb_eval_steps: int
        :return: DataLoader for the validation data.
        :rtype (float, int):
        """
        b_input_ids, b_input_mask, b_labels = batch

        with self.torch.no_grad():
            # noinspection PyCallingNonCallable
            outputs = self.model(
                b_input_ids, token_type_ids=None, attention_mask=b_input_mask
            )

        logits = outputs[0]
        logits = logits.detach().cpu().numpy()
        label_ids = b_labels.to("cpu").numpy()

        tmp_eval_accuracy = BERTBinaryClassifier._flat_accuracy(logits, label_ids)
        eval_accuracy += tmp_eval_accuracy
        nb_eval_steps += 1
        return eval_accuracy, nb_eval_steps

    def epoch_iteration(
        self,
        train_dataloader,
        validation_dataloader,
        loss_values: list,
    ) -> list:
        """Iterate through epoch.

        :param train_dataloader: DataLoader for the training data.
        :type train_dataloader: DataLoader
        :param validation_dataloader: DataLoader for the validation data.
        :type validation_dataloader: DataLoader
        :param loss_values: List of average training loss across batches.
        :type loss_values: list
        :return: Updated list of average training loss across batches.
        :rtype list:
        """
        t_0 = time.time()
        total_loss = 0
        self.model.train()

        for step, batch in enumerate(train_dataloader):
            if step % 40 == 0 and not step == 0:
                time_taken = format_time(time.time() - t_0)

                print(
                    "  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.".format(
                        step, len(train_dataloader), time_taken
                    )
                )
            total_loss = self.train_batch(batch, total_loss)

        avg_train_loss = total_loss / len(train_dataloader)
        loss_values.append(avg_train_loss)

        print("")
        print("  Average training loss: {0:.2f}".format(avg_train_loss))
        print("  Training epoch took: {:}".format(format_time(time.time() - t_0)))

        print("")
        print("Running Validation...")

        t0 = time.time()

        self.model.eval()

        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0

        for batch in validation_dataloader:
            eval_accuracy, nb_eval_steps = self.validate_batch(
                batch, eval_accuracy, nb_eval_steps
            )

        print("  Accuracy: {0:.2f}".format(eval_accuracy / nb_eval_steps))
        print("  Validation took: {:}".format(format_time(time.time() - t0)))
        return loss_values

    def fit(self, x: pd.DataFrame, y: pd.Series) -> ModelBase:
        """Fit with BertForSequenceClassification.

        :param x: DataFrame with one column of sentences.
        :type x: pd.DataFrame
        :param y: Series of binary classification labels.
        :type y: pd.Series
        :return: Returns self.
        :rtype class:
        """
        sentences = x.iloc[:, 0]
        labels = y.values

        self.tokenizer = self.transformers.BertTokenizer.from_pretrained(
            "bert-base-uncased", do_lower_case=True
        )

        input_ids = self.encode(sentences)
        self.set_max_length(input_ids)
        input_ids_padded = self.pad_sequences(input_ids)
        attention_masks = BERTBinaryClassifier._get_attention_masks(input_ids_padded)

        (
            train_inputs,
            validation_inputs,
            train_labels,
            validation_labels,
        ) = BERTBinaryClassifier._split_train_val(input_ids_padded, labels)
        train_masks, validation_masks, _, _ = BERTBinaryClassifier._split_train_val(
            attention_masks, labels
        )

        train_inputs = self.torch.tensor(train_inputs)
        validation_inputs = self.torch.tensor(validation_inputs)
        train_masks = self.torch.tensor(train_masks)
        validation_masks = self.torch.tensor(validation_masks)
        train_labels = self.torch.tensor(train_labels)
        validation_labels = self.torch.tensor(validation_labels)

        train_dataloader = self.get_train_dataloader(
            train_inputs, train_masks, train_labels
        )
        validation_dataloader = self.get_validation_dataloader(
            validation_inputs, validation_masks, validation_labels
        )
        self.optimizer = self.get_optimizer()

        epochs = 4
        total_steps = len(train_dataloader) * epochs
        self.scheduler = self.transformers.get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=0,
            num_training_steps=total_steps,
        )
        self._set_seeds()

        loss_values = []
        for epoch_i in range(0, epochs):
            print("")
            print("======== Epoch {:} / {:} ========".format(epoch_i + 1, epochs))
            print("Training...")
            loss_values = self.epoch_iteration(
                train_dataloader, validation_dataloader, loss_values
            )

        print("")
        print("Training complete!")

        return self

    @staticmethod
    def _flat_accuracy(preds: np.ndarray, labels: np.ndarray) -> float:
        pred_flat = np.argmax(preds, axis=1).flatten()
        labels_flat = labels.flatten()
        return np.sum(pred_flat == labels_flat) / len(labels_flat)

    @staticmethod
    def _get_matthews_correlation(
        true_labels: list, predictions: list
    ) -> Tuple[float, np.ndarray]:
        matthews_set = []

        print("Calculating Matthews Corr. Coef. for each batch...")

        for i in range(len(true_labels)):
            pred_labels_i = np.argmax(predictions[i], axis=1).flatten()
            matthews = matthews_corrcoef(true_labels[i], pred_labels_i)
            matthews_set.append(matthews)

        flat_predictions = [item for sublist in predictions for item in sublist]
        flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
        flat_true_labels = [item for sublist in true_labels for item in sublist]
        mcc = matthews_corrcoef(flat_true_labels, flat_predictions)
        print("MCC: %.3f" % mcc)
        return mcc, flat_predictions

    def predict(self, x: pd.DataFrame, y: pd.Series = pd.Series) -> np.ndarray:
        """Predict with BertForSequenceClassification.

        :param x: DataFrame with one column of sentences.
        :type x: pd.DataFrame
        :param y: Series of binary classification labels.
        :type y: pd.Series
        :return: Returns predicted classes.
        :rtype np.ndarray:
        """
        sentences = x.iloc[:, 0].values
        labels = y.values

        input_ids = self.encode(sentences)
        input_ids_padded = self.pad_sequences(input_ids)
        attention_masks = BERTBinaryClassifier._get_attention_masks(input_ids_padded)

        prediction_inputs = self.torch.tensor(input_ids_padded)
        prediction_masks = self.torch.tensor(attention_masks)
        prediction_labels = self.torch.tensor(labels)

        prediction_dataloader = self.get_validation_dataloader(
            prediction_inputs, prediction_masks, prediction_labels
        )

        print(
            "Predicting labels for {:,} test sentences...".format(
                len(prediction_inputs)
            )
        )

        self.model.eval()

        predictions, true_labels = [], []

        for batch in prediction_dataloader:
            b_input_ids, b_input_mask, b_labels = batch

            with self.torch.no_grad():
                # noinspection PyCallingNonCallable
                outputs = self.model(
                    b_input_ids, token_type_ids=None, attention_mask=b_input_mask
                )

            logits = outputs[0]
            logits = logits.detach().cpu().numpy()
            label_ids = b_labels.to("cpu").numpy()

            predictions.append(logits)
            true_labels.append(label_ids)

        print(
            "Positive samples: %d of %d (%.2f%%)"
            % (y.sum(), len(y), (y.sum() / len(y) * 100.0))
        )

        self.mcc, self.predictions = self._get_matthews_correlation(
            true_labels, predictions
        )

        return self.predictions
