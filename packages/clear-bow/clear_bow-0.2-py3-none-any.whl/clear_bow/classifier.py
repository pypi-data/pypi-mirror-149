import math
from pathlib import Path

import numpy as np
from srsly import read_json, write_json


class DictionaryClassifier:
    def __init__(
        self, model_path=None, classifier_type="multi_class", label_dictionary=None
    ):
        # alwyas use Path boject
        model_path = Path(model_path) if model_path else None
        self.round_value = 4

        # init with default values, otherwise, use serialised values
        self.classifier_type = classifier_type or None
        self.label_dictionary = (
            {k: list(set(v)) for k, v in label_dictionary.items()}
            if label_dictionary
            else None
        )

    def _format_predict_dict(self, pred_dict):
        # explicitly round floats within results dict
        return {k: round(float(v), self.round_value) for k, v in pred_dict.items()}

    def _transform_predict_dict(self, pred_dict):
        # if all word counts are 0
        if all(x == 0 for x in pred_dict.values()):
            prob_dict = {k: 0.0 for k in pred_dict.keys()}
            prob_dict["no_label"] = 1.0
            return prob_dict

        elif self.classifier_type == "multi_class":
            return dict(
                zip(pred_dict.keys(), self._softmax_array(list(pred_dict.values())))
            )

        elif self.classifier_type == "multi_label":
            return dict(
                zip(pred_dict.keys(), self._sigmoid_array(list(pred_dict.values())))
            )

    def _sigmoid_array(self, x):
        return [1 / (1 + math.exp(-e)) for e in x]

    def _softmax_array(self, x):
        e_x = np.exp(x - np.max(x))
        return list(e_x / e_x.sum(axis=0))

    def _get_label_word_count(self, text):
        tally = {}
        for k, v in self.label_dictionary.items():
            tally_temp = sum(e in text.lower() for e in v)
            tally[k] = tally_temp

        return tally

    def from_disk(self, model_path):
        model_path = Path(model_path)
        self.classifier_type = read_json(model_path / "config.json")["classifier_type"]
        self.label_dictionary = read_json(model_path / "label_dictionary.json")

    def to_disk(self, model_path):
        # create as needed
        model_path = Path(model_path)
        if not model_path.exists():
            model_path.mkdir(parents=True, exist_ok=True)

        write_json(
            model_path / "config.json", {"classifier_type": self.classifier_type}
        )
        write_json(model_path / "label_dictionary.json", self.label_dictionary)

    def predict_single(self, text, round_preds=True):
        # retrieve absolute counts
        pred_dict = self._get_label_word_count(text)

        # transform with softmax/sigmoid
        pred_dict = self._transform_predict_dict(pred_dict)

        # round, return
        return self._format_predict_dict(pred_dict) if round_preds else pred_dict

    def predict_batch(self, texts, round_preds=True):
        return [self.predict_single(e, round_preds=round_preds) for e in texts]
