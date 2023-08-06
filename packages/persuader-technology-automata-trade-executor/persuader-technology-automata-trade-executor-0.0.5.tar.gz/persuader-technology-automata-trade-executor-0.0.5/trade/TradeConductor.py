import logging

from core.trade.InstrumentTrade import InstrumentTrade, Status
from traderepo.repository.TradeRepository import TradeRepository

from trade.executor.TradeExecutor import TradeExecutor


class TradeConductor:

    def __init__(self, options, trade_repository: TradeRepository, trade_executor: TradeExecutor):
        self.options = options
        self.trade_repository = trade_repository
        self.trade_executor = trade_executor

    def build_trade_key(self):
        return self.options['TRADE_KEY']

    def store_submitted_trade(self, trade: InstrumentTrade):
        self.trade_repository.store_trade(trade)

    def fetch_trade_to_submit(self) -> InstrumentTrade:
        return self.trade_repository.retrieve_trade()

    def perform_trade(self):
        trade = self.fetch_trade_to_submit()
        if trade.status == Status.NEW:
            updated_trade = self.trade_executor.trade(trade)
            self.store_submitted_trade(updated_trade)
        else:
            logging.warning(f'Trade is not new, so will not trade -> {trade}')
