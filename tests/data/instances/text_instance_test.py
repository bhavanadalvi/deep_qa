# pylint: disable=no-self-use,invalid-name
from deep_qa.common.params import Params
from deep_qa.data.data_indexer import DataIndexer
from deep_qa.data.instances.instance import TextInstance
from deep_qa.data.instances.text_classification import IndexedTextClassificationInstance
from deep_qa.data.instances.text_classification import TextClassificationInstance
from deep_qa.data.tokenizers import tokenizers
from ...common.test_case import DeepQaTestCase

class TestTextInstance(DeepQaTestCase):
    """
    The point of this test class is to test the TextEncoder used by the TextInstance, to be sure
    that we get what we expect when using character encoders, or word-and-character encoders.
    """
    def tearDown(self):
        super(TestTextInstance, self).tearDown()
        TextInstance.tokenizer = tokenizers['words'](Params({}))

    def test_words_tokenizes_the_sentence_correctly(self):
        t = TextClassificationInstance("This is a sentence.", None)
        assert t.words() == {'words': ['this', 'is', 'a', 'sentence', '.']}
        TextInstance.tokenizer = tokenizers['characters'](Params({}))
        assert t.words() == {'words': ['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 's',
                                       'e', 'n', 't', 'e', 'n', 'c', 'e', '.']}
        TextInstance.tokenizer = tokenizers['words and characters'](Params({}))
        assert t.words() == {'words': ['this', 'is', 'a', 'sentence', '.'],
                             'characters': ['t', 'h', 'i', 's', 'i', 's', 'a', 's', 'e', 'n', 't',
                                            'e', 'n', 'c', 'e', '.']}

    def test_to_indexed_instance_converts_correctly(self):
        data_indexer = DataIndexer()
        sentence_index = data_indexer.add_word_to_index("sentence", namespace='words')
        capital_a_index = data_indexer.add_word_to_index("A", namespace='words')
        space_index = data_indexer.add_word_to_index(" ", namespace='words')
        a_index = data_indexer.add_word_to_index("a", namespace='words')
        s_index = data_indexer.add_word_to_index("s", namespace='words')
        e_index = data_indexer.add_word_to_index("e", namespace='words')
        n_index = data_indexer.add_word_to_index("n", namespace='words')
        t_index = data_indexer.add_word_to_index("t", namespace='words')
        c_index = data_indexer.add_word_to_index("c", namespace='words')
        a_char_index = data_indexer.add_word_to_index("a", namespace='characters')
        s_char_index = data_indexer.add_word_to_index("s", namespace='characters')
        e_char_index = data_indexer.add_word_to_index("e", namespace='characters')
        n_char_index = data_indexer.add_word_to_index("n", namespace='characters')
        t_char_index = data_indexer.add_word_to_index("t", namespace='characters')
        c_char_index = data_indexer.add_word_to_index("c", namespace='characters')

        instance = TextClassificationInstance("A sentence", None).to_indexed_instance(data_indexer)
        assert instance.word_indices == [a_index, sentence_index]

        TextInstance.tokenizer = tokenizers['characters'](Params({}))
        instance = TextClassificationInstance("A sentence", None).to_indexed_instance(data_indexer)
        assert instance.word_indices == [capital_a_index, space_index, s_index, e_index, n_index, t_index,
                                         e_index, n_index, c_index, e_index]
        TextInstance.tokenizer = tokenizers['words and characters'](Params({}))
        instance = TextClassificationInstance("A sentence", None).to_indexed_instance(data_indexer)

        assert instance.word_indices == [[a_index, a_char_index],
                                         [sentence_index, s_char_index, e_char_index, n_char_index,
                                          t_char_index, e_char_index, n_char_index, c_char_index,
                                          e_char_index]]


class TestIndexedInstance(DeepQaTestCase):
    def test_get_padding_lengths_works_with_words_and_characters(self):
        instance = IndexedTextClassificationInstance([[1, 2], [3, 1, 2]], True)
        assert instance.get_padding_lengths() == {'num_sentence_words': 2, 'num_word_characters': 3}

    def test_pad_word_sequence_handles_words_and_characters_less(self):
        instance = IndexedTextClassificationInstance([[1, 2], [3, 1, 2]], True)
        padded = instance.pad_word_sequence(instance.word_indices,
                                            {'num_sentence_words': 3, 'num_word_characters': 4})
        assert padded == [[0, 0, 0, 0], [1, 2, 0, 0], [3, 1, 2, 0]]

    def test_pad_word_sequence_handles_words_and_characters_greater(self):
        instance = IndexedTextClassificationInstance([[1, 2], [3, 1, 2]], True)
        padded = instance.pad_word_sequence(instance.word_indices,
                                            {'num_sentence_words': 5, 'num_word_characters': 4})
        assert padded == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 2, 0, 0], [3, 1, 2, 0]]
