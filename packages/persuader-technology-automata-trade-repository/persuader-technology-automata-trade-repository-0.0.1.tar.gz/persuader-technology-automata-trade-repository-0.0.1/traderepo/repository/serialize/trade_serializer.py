from core.trade.InstrumentTrade import InstrumentTrade
from utility.string_utility import is_empty


def serialize_trade(trade: InstrumentTrade) -> dict:
    serialized = {
        'instrument_from': trade.instrument_from,
        'instrument_to': trade.instrument_to,
        'quantity': str(trade.quantity),
        'status': trade.status.value
    }
    if not is_empty(trade.description):
        serialized['description'] = trade.description
    if not is_empty(trade.order_id):
        serialized['order_id'] = trade.order_id
    return serialized
