class Cart:
    def __init__(self, id, name):
        self._id = id
        self._items = {}
        self._name = name

    def addFood(self, food, quantity, overwrite = False):
        assert(type(food) is str)
        if quantity < 0:
            self.deleteFood(food)
        elif food not in self._items.keys():
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
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        assert(type(name) is str)
        self._name = name