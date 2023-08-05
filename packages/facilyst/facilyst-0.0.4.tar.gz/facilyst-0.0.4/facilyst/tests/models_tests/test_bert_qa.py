import pytest

from facilyst.models.neural_networks.bert_qa import BERTQuestionAnswering

pytestmark = pytest.mark.needs_extra_dependency


def test_bert_qa_class_variables():
    assert BERTQuestionAnswering.name == "BERT Question Answering"
    assert BERTQuestionAnswering.primary_type == "regression"
    assert BERTQuestionAnswering.secondary_type == "neural"
    assert BERTQuestionAnswering.tertiary_type == "nlp"
    assert BERTQuestionAnswering.hyperparameters == {}


def test_bert_qa_errors_before_fit():
    bert = BERTQuestionAnswering()
    with pytest.raises(ValueError, match="Call fit to set the tokenizer."):
        bert.get_tokenizer()

    with pytest.raises(ValueError, match="Call fit to get the encoded input."):
        bert.get_encoded_input()

    with pytest.raises(ValueError, match="Call fit to get all tokens."):
        bert.get_all_tokens()

    with pytest.raises(
        ValueError, match="Call fit to get the number of tokens in the question."
    ):
        bert.get_num_tokens_question()

    with pytest.raises(
        ValueError, match="Call fit to get the number of tokens in the text."
    ):
        bert.get_num_tokens_text()


text = (
    "New York (CNN) -- More than 80 Michael Jackson collectibles -- "
    "including the late pop star's famous rhinestone-studded glove from a 1983 performance -- "
    "were auctioned off Saturday, reaping a total $2 million. Profits from the auction at the "
    "Hard Rock Cafe in New York's Times Square crushed pre-sale expectations of only $120,000 in sales. "
    "The highly prized memorabilia, which included items spanning the many stages of Jackson's career, "
    "came from more than 30 fans, associates and family members, who contacted Julien's Auctions to sell "
    "their gifts and mementos of the singer. Jackson's flashy glove was the big-ticket item of the night, "
    "fetching $420,000 from a buyer in Hong Kong, China. Jackson wore the glove at a 1983 performance "
    'during "Motown 25," an NBC special where he debuted his revolutionary moonwalk. '
    'Fellow Motown star Walter "Clyde" Orange of the Commodores, who also performed in the special '
    "26 years ago, said he asked for Jackson's autograph at the time, but Jackson gave him "
    'the glove instead. \'The legacy that [Jackson] left behind is bigger than life for me," Orange said. "I '
    "hope that through that glove people can see what he was trying to say in his music and what he said in "
    'his music." Orange said he plans to give a portion of the proceeds to charity. Hoffman Ma, who bought '
    "the glove on behalf of Ponte 16 Resort in Macau, paid a 25 percent buyer's premium, which was tacked "
    "onto all final sales over $50,000. Winners of items less than $50,000 paid a 20 percent premium."
)


def test_bert_qa_error_before_predict():
    bert = BERTQuestionAnswering()
    bert.fit("Who died?", text)
    with pytest.raises(ValueError, match="Call predict to get the encoded answer."):
        bert.get_encoded_answer()


@pytest.mark.parametrize(
    "question, answer, expected_num_tokens_question, expected_encoded_answer",
    [
        (
            "Where was the Auction held?",
            "Hard rock cafe in new york's times square",
            8,
            [2524, 2600, 7668, 1999, 2047, 2259, 1005, 1055, 2335, 2675],
        ),
        ("Who bought the glove?", "Hoffman ma", 7, [15107, 5003]),
        (
            "What was the name of the auction",
            "Julien's auctions",
            9,
            [19290, 1005, 1055, 10470, 2015],
        ),
        ("Who died?", "Michael jackson", 5, [2745, 4027]),
    ],
)
def test_bert_qa(
    question, answer, expected_num_tokens_question, expected_encoded_answer
):
    import transformers

    bert = BERTQuestionAnswering()
    bert.fit(question, text)

    tokenizer = bert.get_tokenizer()
    encoded_input = bert.get_encoded_input()
    all_tokens = bert.get_all_tokens()
    num_tokens_question = bert.get_num_tokens_question()
    num_tokens_text = bert.get_num_tokens_text()

    assert isinstance(
        tokenizer, transformers.models.bert.tokenization_bert.BertTokenizer
    )
    assert all(isinstance(each_input, int) for each_input in encoded_input)
    assert all(isinstance(each_token, str) for each_token in all_tokens)
    assert num_tokens_question == expected_num_tokens_question
    assert num_tokens_text == 349

    bert_answer = bert.predict()

    encoded_answer = bert.get_encoded_answer()

    assert encoded_answer == expected_encoded_answer
    assert bert_answer == answer
