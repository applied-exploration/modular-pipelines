from typing import Dict
import pandas as pd
from blocks.pipeline import Pipeline
from type import Evaluators
from .store import Store
from typing import List, Union
from .integrity import check_integrity
from pprint import pprint
from .evaluation import evaluate
import datetime
from configs import Const


class Runner:
    def __init__(
        self,
        pipeline: Pipeline,
        data: Dict[str, Union[pd.Series, List]],
        labels: pd.Series,
        evaluators: Evaluators,
        train: bool,
    ):
        self.run_path = f"{Const.output_runs_path}/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}/"
        self.pipeline = pipeline
        self.store = Store(data, labels, self.run_path)
        self.evaluators = evaluators
        self.train = train

    def run(self):
        print("🗼 Hierarchy of Models:")
        pprint(self.pipeline.children())

        print("🆔 Verifying pipeline integrity")
        if not check_integrity(self.pipeline):
            raise Exception("Pipeline integrity check failed")

        print("💈 Loading existing models")
        self.pipeline.load()

        print("📡 Looking for remote models")
        self.pipeline.load_remote()

        if self.train:
            print("🏋️ Training pipeline")
            self.pipeline.fit(self.store)

            print("📡 Uploading models")
            self.pipeline.save_remote()

        print("🔮 Predicting with pipeline")
        preds_probs = self.pipeline.predict(self.store)
        predictions = [pred[0] for pred in preds_probs]

        evaluate(predictions, self.store, self.evaluators, self.run_path)

        return predictions
