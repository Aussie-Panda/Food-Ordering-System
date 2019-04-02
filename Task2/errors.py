class StockError(Exception):
	
	def __init__(self, errors, msg=None):
		if msg is None:
			msg = "Those items are out of stock: %s"%(', '.join(errors))

		def __str__(self):
			return msg

		self._erros = errors