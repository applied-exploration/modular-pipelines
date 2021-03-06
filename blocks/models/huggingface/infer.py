from typing import Callable, List, Tuple
from type import HuggingfaceConfig, PredsWithProbs
from datasets import Dataset
import numpy as np
from configs.constants import Const
import pandas as pd


def run_inference_pipeline(
    model: Callable, test_data: Dataset, config: HuggingfaceConfig
) -> List[PredsWithProbs]:

    scores = model(test_data[Const.input_col], top_k=config.num_classes)
    probs = [convert_scores_dict_to_probs(score) for score in scores]
    predicitions = [np.argmax(prob) for prob in probs]

    return list(zip(predicitions, probs))


def take_first(elem):
    return elem[0]


def convert_scores_dict_to_probs(scores: List[dict]) -> List[Tuple]:
    sorted_scores = sorted(
        [
            (int(scores_dict["label"].split("_")[1]), scores_dict["score"])
            for scores_dict in scores
        ],
        key=take_first,
    )
    return [item[1] for item in sorted_scores]
