
#created by Yanning Cao from memberless Team
#mains class

from abc import ABC, abstractmethod

class Food(ABC):
    
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    #implement this later!!!!!!!!!!!!!!!
    @abstractmethod
    def computePrice(self):
        pass

    def __str__(self):
        return f"{self.name}: ${self.price}"