from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError
from core.trade.InstrumentTrade import InstrumentTrade

from traderepo.repository.serialize.trade_deserializer import deserialize_trade
from traderepo.repository.serialize.trade_serializer import serialize_trade

TRADE_KEY = 'TRADE_KEY'


class TradeRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {TRADE_KEY}')
        if TRADE_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {TRADE_KEY}')

    def build_trade_key(self):
        return self.options[TRADE_KEY]

    def store_trade(self, trade: InstrumentTrade):
        trade_key = self.build_trade_key()
        trade_to_store = serialize_trade(trade)
        self.cache.store(trade_key, trade_to_store)

    def retrieve_trade(self) -> InstrumentTrade:
        trade_key = self.build_trade_key()
        raw_trade = self.cache.fetch(trade_key, as_type=dict)
        return deserialize_trade(raw_trade)
