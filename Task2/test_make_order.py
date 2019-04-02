from ordering_system import OrderingSystem
from Food import Food
from order import Order
from stock import Stock
from errors import StockError, QuantityError
import pytest

@pytest.fixture
def sys():
	return OrderingSystem()

	