# This is a generic interface for strategies in the strategy folder.
from abc import ABC, abstractmethod
from order import Order
class StrategyInterface(ABC):
    @abstractmethod
    def generate_signals(self, timestamp, market_data):
        """
        Generate trading signals based on the provided market data.
        Take in timestamp (datetime) and market_data (from data_loader)
        Return a list of Order objects.
        """
        pass