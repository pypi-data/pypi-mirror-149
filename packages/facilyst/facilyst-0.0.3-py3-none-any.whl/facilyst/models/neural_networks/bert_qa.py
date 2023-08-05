"""A BERT Question Answering neural network model."""
from typing import Any, Optional

from facilyst.models import ModelBase
from facilyst.utils import import_errors_dict, import_or_raise


class BERTQuestionAnswering(ModelBase):
    """The BertForQuestionAnswering model (via transformers' implementation).

    This is a pretrained bidirectional encoder.
    """

    name: str = "BERT Question Answering"

    primary_type: str = "regression"
    secondary_type: str = "neural"
    tertiary_type: str = "nlp"

    hyperparameters: dict = {}

    def __init__(self, **kwargs) -> None:
        self.tokenizer = None
        self.encoded_input = None
        self.all_tokens = None
        self.segment_ids = None
        self.encoded_answer = None
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
            self.transformers.BertForQuestionAnswering.from_pretrained(
                "bert-large-uncased-whole-word-masking-finetuned-squad"
            )
        )

        super().__init__(model=question_answering_model, parameters=parameters)

    # @torch.no_grad()
    def fit(self, question: str, text: str) -> ModelBase:
        """Fit with BERTQuestionAnswering.

        :param question: Question to ask.
        :type question: str
        :param text: Corpus of text.
        :type text: str
        :return: Returns self.
        :rtype class:
        """
        self.tokenizer = self.transformers.BertTokenizer.from_pretrained(
            "bert-large-uncased-whole-word-masking-finetuned-squad"
        )

        self.encoded_input = self.tokenizer.encode(question, text)
        self.all_tokens = self.tokenizer.convert_ids_to_tokens(self.encoded_input)

        first_sep_id = self.encoded_input.index(self.tokenizer.sep_token_id)
        num_tokens_question = first_sep_id + 1
        num_tokens_text = len(self.encoded_input) - num_tokens_question
        self.segment_ids = [0] * num_tokens_question + [1] * num_tokens_text

        return self

    def predict(self, x: Optional[Any] = None, y: Optional[Any] = None) -> str:
        """Fit with BERTQuestionAnswering.

        :param x: Ignored.
        :type x: None
        :param y: Ignored.
        :type y: None
        :return: Returns answer.
        :rtype str:
        """
        token_tensors = self.torch.tensor([self.encoded_input])
        segment_tensors = self.torch.tensor([self.segment_ids])

        output = self.model(token_tensors, token_type_ids=segment_tensors)

        start_tensor = self.torch.argmax(output.start_logits)
        end_tensor = self.torch.argmax(output.end_logits) + 1
        self.encoded_answer = self.encoded_input[start_tensor:end_tensor]
        answer = self.tokenizer.decode(self.encoded_answer)
        answer = answer.capitalize()

        return answer

    def get_tokenizer(self):
        """Get the tokenizer.

        :return: Returns tokenizer.
        :rtype transformers.models.bert.tokenization_bert.BertTokenizer:
        """
        if self.tokenizer:
            return self.tokenizer
        else:
            raise ValueError("Call fit to set the tokenizer.")

    def get_encoded_input(self) -> list:
        """Get the encoded input.

        :return: Returns encoded input.
        :rtype list:
        """
        if self.encoded_input:
            return self.encoded_input
        else:
            raise ValueError("Call fit to get the encoded input.")

    def get_all_tokens(self) -> list:
        """Get all tokens.

        :return: Returns all tokens.
        :rtype list:
        """
        if self.all_tokens:
            return self.all_tokens
        else:
            raise ValueError("Call fit to get all tokens.")

    def get_num_tokens_question(self) -> int:
        """Get the number of tokens in the question.

        :return: Returns the number of tokens in the question.
        :rtype int:
        """
        if self.segment_ids:
            return len(self.segment_ids) - sum(self.segment_ids)
        else:
            raise ValueError("Call fit to get the number of tokens in the question.")

    def get_num_tokens_text(self) -> int:
        """Get the number of tokens in the text.

        :return: Returns the number of tokens in the text.
        :rtype int:
        """
        if self.segment_ids:
            return sum(self.segment_ids)
        else:
            raise ValueError("Call fit to get the number of tokens in the text.")

    def get_encoded_answer(self) -> list:
        """Get the encoded answer.

        :return: Returns encoded answer..
        :rtype list:
        """
        if self.encoded_answer:
            return self.encoded_answer
        else:
            raise ValueError("Call predict to get the encoded answer.")
