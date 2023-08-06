# reference
# https://christopher5106.github.io/deep/learning/2020/04/02/fasttext_pretrained_embeddings_subword_word_representations.html

import fasttext
import numpy as np


class FastTextExtension:
    """FastTextExtension

    Args:
        filename (str): /path/to/bin/file
    """

    def __init__(self, filename: str) -> None:
        self.ft: fasttext.FastText._FastText = fasttext.load_model(filename)

    @property
    def embeddings(self) -> np.ndarray:
        """Get word and subword embeddings.

        Returns:
            embeddings (np.ndarray): word and subword embeddings
        """
        return self.ft.get_input_matrix()

    @property
    def vocab(self) -> list[str]:
        """Get vocabulary list.

        Returns:
            vocab (list[str]): list of vocabularies
        """
        return self.ft.get_words()

    def get_word_vectors(self, sent: str, norm: bool = False) -> list[np.ndarray]:
        """Get list of word vectors.

        Args:
            sent (str): sentence
            norm (bool): normalize each word vectors

        Returns:
            vectors (list[np.ndarray]): list of word vectors
        """
        words: list[str] = fasttext.tokenize(sent)
        vectors: list[np.ndarray] = []

        for word in words:
            vector = self.ft.get_word_vector(word)

            if norm:
                vector_norm = np.linalg.norm(vector)

                if vector_norm > 0:
                    vector /= vector_norm

            vectors.append(vector)

        return vectors
