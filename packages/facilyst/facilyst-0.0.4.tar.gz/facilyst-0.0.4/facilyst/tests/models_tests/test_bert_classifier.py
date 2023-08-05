from unittest.mock import patch

import pandas as pd
import pytest

from facilyst.models.neural_networks.bert_classifier import (
    BERTBinaryClassifier,
)

pytestmark = pytest.mark.needs_extra_dependency


def test_bert_binary_classifier_class_variables():
    assert BERTBinaryClassifier.name == "BERT Binary Classifier"
    assert BERTBinaryClassifier.primary_type == "classification"
    assert BERTBinaryClassifier.secondary_type == "neural"
    assert BERTBinaryClassifier.tertiary_type == "nlp"
    assert BERTBinaryClassifier.hyperparameters == {}


sentences_df = pd.DataFrame(
    {
        "Sentences": [
            "He is a great guy!",
            "He is the worst guy",
            "I'm so happy",
            "I couldn't be more sad",
            "My disappointment is immeasurable, and my day is ruined.",
            "Today is the best day of my life.",
            "What a wonderfully wonderful wonder!",
            "I'm so angry I could scream!",
            "Oh my goodness I am so frustrated!",
            "Thank you for this wonderful gift.",
        ]
        * 50
    }
)
target = pd.Series([1, 0, 1, 0, 0, 1, 1, 0, 0, 1] * 50)


def test_bert_classifier():
    train_x = sentences_df[:10]
    train_y = target[:10]

    test_x = sentences_df[10:15]
    test_y = target[10:15]

    bert_classifier = BERTBinaryClassifier(batch_size=6)
    bert_classifier.fit(train_x, train_y)
    predictions = bert_classifier.predict(test_x, test_y)

    assert len(predictions) == 5


@patch(
    "facilyst.models.neural_networks.bert_classifier.BERTBinaryClassifier.validate_batch"
)
@patch(
    "facilyst.models.neural_networks.bert_classifier.BERTBinaryClassifier.train_batch"
)
def test_bert_classifier_mock_train_validate_batches(
    mock_train_batch, mock_validate_batch
):
    import torch
    import transformers

    train_x = sentences_df[:350]
    train_y = target[:350]

    test_x = sentences_df[350:500]
    test_y = target[350:500]

    mock_train_batch.return_value = 0.0
    mock_validate_batch.return_value = (1, 1)

    bert_classifier = BERTBinaryClassifier(batch_size=6)
    bert_classifier.fit(train_x, train_y)
    predictions = bert_classifier.predict(test_x, test_y)

    assert mock_train_batch.call_count == 212
    assert mock_validate_batch.call_count == 24
    assert len(predictions) == 150
    assert isinstance(bert_classifier.mcc, float)
    assert isinstance(bert_classifier.max_sentence_length, int)
    assert isinstance(bert_classifier.scheduler, torch.optim.lr_scheduler.LambdaLR)
    assert isinstance(
        bert_classifier.tokenizer,
        transformers.models.bert.tokenization_bert.BertTokenizer,
    )
    assert isinstance(bert_classifier.optimizer, transformers.optimization.AdamW)
    assert bert_classifier.batch_size == 6
    assert bert_classifier.seed_val == 42
    assert (bert_classifier.predictions == predictions).all()
