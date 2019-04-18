class Cart:
    def __init__(self, id):
        self._id = id
        self._items = {}

    def addFood(self, food, quantity, overwrite = False):
        assert(type(food) is str)
        if food not in self._items.keys():
            self._items[food] = quantity

        else:
            if overwrite == True:
                self._items[food] = quantity
            else:
                self._items[food] += quantity
        
    def deleteFood(self, food, quantity=None):
        assert(type(food) is str)
        if food not in self._items.keys():
            pass
        else: 
            if quantity is None:
                self._items.pop(food)
            else:
                if quantity >= self._items[food]:
                    self._items.pop(food)
                else:   
                    self._items[food] -= quantity
    
    def empty(self):
        self._items.clear()
    
    @property
    def id(self):
        return self._id
    
    @property
    def items(self):
        return self._items