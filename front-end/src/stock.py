from src.mains import Mains, Burger, Wrap

class Stock():
    def __init__(self):
        '''
        self._mains = {'Burger': 0, 'Wrap': 0}
        self._drinks = {'Lemonade(Bottles)': 0, 'Lemonade(Cans)': 0, 'Orange_Juice': 0}
        self._sides = {'Fries': 0, 'Nuggets': 0, 'Sundae': 0}
        self._ingredients = {'buns': 0, 'patties': 0, 'tomato': 0, 'lettuce' : 0, 'cheddar_cheese' : 0, 'swisse_cheese' : 0, 'tomato_sauce' : 0}
        self._whole = {'Mains': self._mains, 'Drinks': self._drinks, 'Sides': self._sides, 'Ingredients': self._ingredients}
        '''
        self._mains = {}
        self._drinks = {}
        self._sides = {}
        self._ingredients = {}
        self._whole = {'Mains': self._mains, 'Drinks': self._drinks, 'Sides': self._sides, 'Ingredients': self._ingredients}
        
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

    @property
    def whole(self):
        return self._whole

    # add (initialise) food into stock
    def addFood(self, category, food, quantity):
        if category in self.whole.keys():
            stock = self.whole[category]

            if category == 'Mains':
                stock[food.name] = quantity

                for addOn in food.addOn.keys():
                    self._ingredients[addOn.lower()] = quantity

                for ingred in food.ingredientsMenu.keys():
                    self._ingredients[ingred.lower()] = quantity

            elif category == 'Drinks':
                if 'Juice' in food.name:
                    stock[food.name] = quantity
                else:
                    name = f'{food.name}({food.size})'
                    stock[name] = quantity

            elif category == 'Sides':
                stock[food.name] = quantity
 
        else:
            raise SearchError("Category")


    
    # item is a str, amount is int，size is str(Bottles, Cans)
    # for Juice, amount is in ml. For others amount is in whole 
    def increaseQuantity(self, item, amount):
        assert(item != None)
        assert(amount != None)
        if amount < 0:
            raise Exception("Amount cannot be negative :(")

        for stock in self.whole.keys():
            if item in self.whole[stock]:
                self.whole[stock][item] += amount
        
    
    # item is a str or instance of Food, amount is instance of Food.
    def decreaseQuantity(self, item, amount):
        assert(amount>=0)
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
