from .base import Transformation
from configs.constants import Const
import pandas as pd
from utils.spacy import get_spacy
from typing import List, Any
import spacy


class Lemmatizer(Transformation):
    def preload(self):
        self.nlp = get_spacy()
        self.spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

    def predict(self, dataset: List) -> List[str]:
        return [preprocess(item) for item in dataset]



def preprocess(tokens: List[Any]) -> str:
    return " ".join(
        [
            token.lemma_
            for token in tokens
            if not token.is_stop and not token.is_punct and token.lemma_ != " "
        ]
    )
