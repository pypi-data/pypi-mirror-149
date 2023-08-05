from typing import List, Optional

from core.oracle.Prediction import Prediction
from exchange.rate.ExchangeRateHolder import ExchangeRateHolder

from oracle.Oracle import Oracle


class PredictionResolver:

    def __init__(self, oracles, threshold):
        self.oracles: List[Oracle] = oracles
        self.threshold = threshold

    def resolve(self, instrument, exchange_rates, exchanged_from, instant) -> Optional[Prediction]:
        self.set_all_oracle_with_exchange_rates(exchange_rates)
        predictions = self.collect_predictions_from_oracles(instrument, exchanged_from, instant)
        self.reset_oracles()
        return self.determine_best_prediction(predictions)

    def set_all_oracle_with_exchange_rates(self, exchange_rates: ExchangeRateHolder):
        for oracle in self.oracles:
            oracle.set_exchange_rates(exchange_rates)

    def collect_predictions_from_oracles(self, instrument, exchanged_from, instant) -> List[Prediction]:
        predictions = []
        for oracle in self.oracles:
            prediction = oracle.predict(instrument, exchanged_from, instant)
            predictions.append(prediction)
        valid_predictions = [p for p in predictions if p is not None]
        return valid_predictions

    def determine_best_prediction(self, predictions: List[Prediction]):
        if not predictions:
            return None
        sorted_predictions = sorted(predictions, key=lambda prediction: prediction.percent, reverse=True)
        return self.designate_appropriate_prediction(sorted_predictions)

    def designate_appropriate_prediction(self, predictions: List[Prediction]):
        best_prediction = predictions[0]
        if best_prediction.percent > self.threshold:
            return best_prediction
        forced_predictions = [p for p in predictions if p.forced is True]
        if len(forced_predictions) > 0:
            return forced_predictions[0]

    def reset_oracles(self):
        for oracle in self.oracles:
            oracle.reset()

