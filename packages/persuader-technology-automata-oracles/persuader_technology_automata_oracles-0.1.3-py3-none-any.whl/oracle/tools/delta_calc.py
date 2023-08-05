from core.exchange.InstrumentExchange import InstrumentExchange
from core.oracle.Prediction import Prediction
from exchange.rate.InstantRate import InstantRate
from utility.number.BigFloatSubtract import BigFloatSubtract


def calc_delta(instant_rate: InstantRate, other_instant_rate: InstantRate):
    return BigFloatSubtract(instant_rate.rate, other_instant_rate.rate).result()


def calc_delta_prediction(instant_rate: InstantRate, other_instant_rate: InstantRate, instrument_exchange: InstrumentExchange) -> Prediction:
    (instrument, to_instrument) = instrument_exchange
    delta = calc_delta(instant_rate, other_instant_rate)
    return Prediction(outcome=[instrument, to_instrument], profit=delta)
