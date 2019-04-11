from src.mains import Mains, Burger, Wrap
class Stock():
    def __init__(self):
        self._mains = { 'Burger': 0, 'Wrap': 0}
        self._drinks = {'Lemonade(Bottles)': 0, 'Lemonade(Cans)': 0, 'Orange_Juice': 0}
        self._sides = {'Fries': 0, 'Nuggets': 0}
        self._ingredients = {'buns': 0, 'patties': 0, 'tomato': 0, 'lettuce' : 0, 'cheddar_cheese' : 0, 'swiss_cheese' : 0, 'tomato_sauce' : 0}

    @property
    def mains(self):
        return self._mains

    @property
    def drinks(self):
        return self._drinks

    @property
    def sides(self):
        return self._sides
    
    @property
    def ingredients(self):
        return self._ingredients


    # consume food from stock
    def consumeFood(self,food):
        for item in food:
                self.decreaseQuantity(item, food[item])

                # for Mains, should further find out how many buns/patties/ingradients are consumed
                if isinstance(item, Mains):
                    for i in item.ingredientsOrdered.keys():
                        self.decreaseQuantity(i, item.ingredientsOrdered[i]) 

                    if isinstance(item, Burger):
                        self.decreaseQuantity('buns', item.numBun)
                        self.decreaseQuantity('patties', item.numPat)
                    elif isinstance(item, Wrap):
                        self.decreaseQuantity('patties', item.numPat)
        
    # item is a str, amount is int，size is str(Bottles, Cans)
    # for Juice, amount is in ml. For others amount is in whole 
    def increaseQuantity(self, item, amount, size = None):
        assert(item != None)
        assert(amount != None)
        
        if item.name in self._mains.keys() :
            self._mains[item] += amount

        elif item in self._drinks.keys():
            if 'Juice' in item.name:
                self._drinks[item.name] += amount

            else:
                assert(size != None)
                # convert item name to name in stock 
                target = f"{item}({size})"
                self._drinks[target] += amount


        elif item.name in self._sides.keys():
            self._sides[item.name] += amount
            

        elif item.name in self._ingredients.keys():
            self._ingredients[item] += amount
    
    # item is a str or instance of Food, amount is instance of Food.
    def decreaseQuantity(self, item, amount):
        
        # ingredients don't have class(instance)
        if type(item) is str:
            if item in self._ingredients.keys():
                self._ingredients[item] -= amount

        # others are instances of Food
        else:
            # if it's Mains
            if item.name in self._mains.keys() :
                self._mains[item.name] -= amount

            # if it's in Sides
            elif item.name in self._sides.keys():
                self._sides[item.name] -=  item.volumn * amount

            # it's in Drinks            
            else:
                # if it's juice, directly decrease with it's volumn * amount
                if 'Juice' in item.name:
                    self._drinks[item.name] -=  item.volumn * amount

                else:
                    # convert item name to name in stock, e.g. "Lemonade(Bottles)"
                    target = f"{item.name}({item.size})"
                    self._drinks[target] -= amount
        

    def __str__(self):
        msg = ''
        for category in [self.mains, self.drinks, self.sides, self.ingredients]:
            for item in category:
                msg += f"{item}: {category[item]}; "
            msg += "\n"
        return msg
