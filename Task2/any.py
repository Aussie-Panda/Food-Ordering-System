from abc import ABC, abstractmethod

class Any(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @abstractmethod
    def asd(self):
        pass

    '''
    def __str__(self):
        return f"name: {self.name}, price: ${self.price}"
    '''

class thing(Any):
    def __init(self, name, price):
        super().__init__(name,price)

    def asd(self):
        pass

t1 = thing('haha',1)
t2 = thing('hahaha', 2)
t3 = thing('hahahaha', 3)

l = [t1, t2, t3]
l2 = [t1, t3]

print(l[0]) # <__main__.thing object at 0x1013de6a0>
print(l2[0]) # <__main__.thing object at 0x1013de6a0>




