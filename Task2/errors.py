class StockError(Exception):
	
	def __init__(self, errors, msg=None):
		if msg is None:
			msg = "Those items are out of stock: %s"%(', '.join(errors))

		def __str__(self):
			return msg

		self._erros = errors


class QuantityError(Exception):
	def __init__(self,item):
		self._item = item

		def __str__(self):
			return f"Item {self._item} has invalid Quantity!"