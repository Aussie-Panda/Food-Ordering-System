from src.ordering_system import OrderingSystem
from src.food import Food
from src.order import Order
from src.stock import Stock
from src.errors import StockError, bun_error, check_numBuns_error, checkStock
from src.mains import Mains, Burger, Wrap
from src.drinks import Drinks
from src.sides import Sides


def bootstrap_system():
    system = OrderingSystem()
    
    # initialise menu
    # Mains Burger(numBun, numPat) Wrap(numPat)
    burger = Burger('Burger', 5)
    wrap = Wrap('Wrap', 4)

    # Drinks(name, price, size, volumn)
    can = Drinks('Lemonade', 3, 'Cans', 375)
    bottles = Drinks('Lemonade', 5, 'Bottles', 600)
    smlJuice = Drinks('Orange_Juice', 2, 'sml', 250)
    medJuice = Drinks('Orange_Juice', 4, 'med', 450)

    # Sides(self, name, price, size, type)
    smlNuggets = Sides('Nuggets', 1, 'sml', 3)
    lrgNuggets = Sides('Nuggets', 2, 'lrg', 6)
    smlFries = Sides('Fries', 1, 'sml', 20)
    medFries = Sides('Fries', 2, 'med', 40)
    lrgFries = Sides('Fries', 3, 'lrg', 60)

    system.mainsMenu = [burger, wrap]
    system.drinksMenu = [can, bottles, smlJuice, medJuice]
    system.sidesMenu = [smlNuggets, lrgNuggets, smlFries, medFries, lrgFries]
    
    # initialise stock
    for category in [system.stock.mains, system.stock.drinks, system.stock.sides, system.stock.ingredients]:
        for item in category:
            if item == 'Fries':
                category[item] = 10000
            elif 'Juice' in item:
                category[item] = 100000
            else:
                category[item] = 100
    
    return system
