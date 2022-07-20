from typing import Dict
import pandas as pd
from blocks.pipeline import Pipeline

from type import Evaluators
from .store import Store
from typing import List, Union

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
        plugins: List["Plugin"],
    ):
        self.run_path = f"{Const.output_runs_path}/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}/"
        self.pipeline = pipeline
        self.store = Store(data, labels, self.run_path)
        self.evaluators = evaluators
        self.train = train
        self.plugins = plugins

    def run(self):
        for plugin in self.plugins:
            plugin.on_run_begin(self.pipeline)

        print("💈 Loading existing models")
        self.pipeline.load(self.plugins)

        print("📡 Looking for remote models")
        self.pipeline.load_remote()

        if self.train:
            print("🏋️ Training pipeline")
            self.pipeline.fit(self.store, self.plugins)

            print("📡 Uploading models")
            self.pipeline.save_remote()

        print("🔮 Predicting with pipeline")
        preds_probs = self.pipeline.predict(self.store, self.plugins)
        predictions = [pred[0] for pred in preds_probs]

        stats = evaluate(predictions, self.store, self.evaluators, self.run_path)
        self.store.set_stats("final", stats)

        for plugin in self.plugins:
            plugin.on_run_end(self.pipeline, stats)

        return predictions