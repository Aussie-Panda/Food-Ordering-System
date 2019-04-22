# import Flask library
from flask import Flask, render_template, request, redirect, url_for, abort, Markup, session
from init import bootstrap_system
from src.errors import StockError, SearchError
from src.shoppingCart import Cart
import copy

OVER_WRITE = True

# create a flask project, assigning to a variable called app
app = Flask(__name__)
app.secret_key = 'very-secret-123' 
# initialise system
system = bootstrap_system()
# for session
orders = {}

# take in a Mains instance and extract information.
# info = {[item]: price}
def formatMains(food):
    info = {}
    try:
        target = system.getFood(food)
    except SearchError as er:
        raise(er)
    else:
        for i in target.ingredientsMenu.keys():
            info[i] = target.ingredientsMenu[i]
        for a in target.addOn.keys():
            info[a] = target.addOnMenu[a]
        
        info[food] = target.price
        if not info:
            raise SearchError('food')  
        return info

# take in a Drinks or Sides instance and extract information
# info = {[size]: f'{volumn}{unit} {price}'}
def formatDS(food):
    info = {}
    for menu in [system.drinksMenu, system.sidesMenu]:
        for item in menu:
            if item.name == food:
                info[item.size] = f'{item.volumn}{item.unit} {item.price}'
    if not info:
        raise SearchError(f'{food}')
    return info

# compute the total price of a cart
def computePrice(cart):
    price = 0
    # try get info if it's drinks/sides
    try:
        info = formatDS(cart.name)
        for size in cart.items.keys():
            price += (int(info[size].split()[1]) * cart.items[size])
    
    # getting error means it's mains
    except SearchError:
        try:
            info = formatMains(cart.name)

            for item in cart.items.keys():
                price += (info[item] * cart.items[item])
            # price += info[cart.name]

        except Exception as er:
            raise SearchError(f'{er} in conpute main price')
        
    return price

# fetch a cart with unique id from session
def fetch_session_cart(id, food_name):
    # Creates a new cart first if the cart never existed
    id = int(id)
    if 'cart' not in session:
        # print('cart not in session')
        cart = Cart(id,food_name)
        session['cart'] = cart.id
        orders[cart.id] = cart
    else:
        # Check the current cookie is valid
        # print(f'cart {id} in session')
        try:
            target = orders[session['cart']]
            target.name = food_name
            return target
        except KeyError: 
            # print('exception raised: cart not in session')
            cart = Cart(id, food_name)
            session['cart'] = cart.id
            orders[cart.id] = cart
            # print("session cookie from ex: " ,session['cart'])
    return orders[session['cart']]

# a handler of root URL
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        
        if 'action' in request.form:
            # if user click "Check Status" button, ask for order ID
            if request.form['action'] == 'Check Status':
                return render_template('home.html', name=system.name, checkStatus=True)
            
            # if user click "Continue Order button, ask for order ID
            elif request.form['action'] == 'Continue my order':
                return render_template('home.html', name=system.name, continueOrder=True)
            
            # if user click "Make New Order" button, create new order and redirect to menu page
            elif request.form['action'] == 'Make New Order':
                order = system.makeOrder()
                # fetch_session_cart(order.orderId)
                return redirect(url_for('menu', id=order.orderId))
        
        elif 'furtherAction' in request.form:
            id = request.form['id']
            # if user insert orderID and comfirm "Check Status"
            if request.form['furtherAction'] == 'Check My Order!':
                # try to get the order, if Error can be catch, display error msg on the same page
                try:
                    order = system.getNextOrder(None, id)
                except (SearchError, ValueError) as er:
                    return render_template('home.html', name=system.name, form=request.form, checkStatus=True,error=str(er))
                
                # if no error occur, redirect to order detail page
                else:
                    return redirect(url_for('order_details', id=id, todo='checkStatus'))
                
            # if user insert orderID and confirm "Check Order"
            elif request.form['furtherAction'] == 'Continue My Order!':
                # try to get the order, if Error can be catch, display error msg on the same page
                try:
                    order = system.getNextOrder(None, id)
                except (SearchError, ValueError) as er:
                    return render_template('home.html', name=system.name,form=request.form, continueOrder=True, error=str(er))
                
                # if no error occur and the order is not submitted, redirect to order detail page
                else:
                    if order.orderStatus != 'Not Submitted':
                        er = "Your order has been submitted, please go to 'Check Status'"
                        return render_template('home.html', name=system.name, form=request.form, continueOrder=True, error=er)
                    else:
                        return redirect(url_for('order_details', id=id, todo='continueOrder'))
            
    return render_template('home.html', name=system.name)

# displaying menu and handle ordering
@app.route("/menu/<id>", methods=["GET", "POST"])
def menu(id):
    try:
        order = system.getNextOrder(None,id)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))

    # two list store ordered item's name and it's corresponding size (append None if no size attribute)
    nameList = []
    sizeList = []
    error = ''
    for i in order.orderedItem.keys():
        try:
            sizeList.append(i.size)
        except:
            sizeList.append(None)
        finally:
            nameList.append(i.name)
    if request.method == "POST":
        
        # delete a corresponding food
        if 'delete' in request.form:
            target = request.form['delete'].split()[1]
            size = sizeList[nameList.index(target)]

            try:
                food_to_delete = order.getFood(target,size)
            except SearchError as er:
                error = str(er)

            order.deleteFood(food_to_delete)
        
        # customer click 'confirm'
        elif 'confirm' in request.form:
            # if order is empty, refuse to confirm 
            if len(order.orderedItem) == 0:
                error = 'Please order at least 1 item.'
                return render_template('menu.html', id=id, order=order, mainsM=system.mainsMenu, drinksM=system.drinksMenu, sidesM=system.sidesMenu,error=error)

            # if the order can be successfully confirm (no stockError), display order ditail
            else:
                try:
                    order = system.confirmOrder(order)
                except StockError as er:
                    error = str(er)
                else:
                    return redirect(url_for('order_details', id=id, todo='checkStatus'))
    
    return render_template('menu.html',id=id, order=order, mainsM=system.mainsMenu, drinksM=system.drinksMenu, sidesM=system.sidesMenu, error=error)

# display and order Mains 
@app.route("/menu/<id>/Mains/<mains>", methods=["GET","POST"])
def Mains(id,mains):
    try:
        order = system.getNextOrder(None, id)
        food = system.getFood(mains)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))
    
    cart = fetch_session_cart(id, mains)
    error = ""
    if request.method == 'POST':

        if 'action' in request.form:
            cart.action = request.form['action']
        # if customer wants to add Buns/Patties/Ingredients
        elif 'add' in request.form:
            target = request.form['add'][7:]
            
            # try to fetch the quantity
            try:
                num = int(request.form[f'quantity{target}'])
                assert(num >= 0)
            except:
                error = "Please insert positive integer"
            else:
                if target == 'Ingredients':
                    target = request.form['Ingredients']
                
                # delete the item is quantity is 0    
                if num == 0:
                    cart.deleteFood(target)
                else:
                    cart.addFood(target,num, OVER_WRITE)
        
        # if customer confirm to order the Mains
        elif 'confirm' in request.form:
            finish = True
            # copy an instance from menu
            new_food = copy.deepcopy(food)
            # if the mains is customed
            if cart.action == 'Custom':
                # Burger has to have buns
                
                if not cart.items:
                    error = "Please order at least 1 items"
                    finish = False

                else:
                    # add ingredients
                    for elem in new_food.ingredientsMenu.keys():
                        if elem in cart.items:
                            new_food.changeIngredients(elem, cart.items[elem])

                    # add addOn
                    for elem in new_food.addOn:
                        if elem in cart.items:
                            new_food.addOn[elem] += cart.items[elem]

                    order.addFood(new_food, 1)
                
            # if the mains is standard
            elif cart.action == 'Standard':
                try:
                    quantity = int(request.form['quantity'])
                    assert(quantity > 0)

                except Exception as er:
                    error = "Please insert positive integer"
                    finish = False
                else:
                    order.addFood(new_food, quantity)

            return render_template('mains.html', food=new_food, action=cart.action, orderedItem=cart.items, price=computePrice(cart), finish=finish, error=error)

        elif 'cancel' in request.form:
            cart.empty()
            return redirect(url_for('menu', id=id))
        
        elif 'return' in request.form:
            cart.empty()
            return redirect(url_for('menu', id=id))

    # compute current price in the cart and display
    return render_template('mains.html', food=food, action=cart.action, orderedItem=cart.items, price=computePrice(cart), error=error)


@app.route("/menu/<id>/DrinksOrSides/<drinks_or_sides>", methods=["GET", "POST"])
def DrinksOrSides(id, drinks_or_sides):
    
    error = ""
    cart = fetch_session_cart(id, drinks_or_sides)
    info = formatDS(drinks_or_sides)
    
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html',msg=str(er))

    if request.method == 'POST':
        if 'action' in request.form:
            # if customer wants to delete all current selected item
            if request.form['action'] == 'Delete All':
                cart.deleteFood(request.form['size'])

            # if quantity is not empty string, try to fetch it
            elif request.form['quantity'] != '':
                try:
                    quantity = int(request.form['quantity'])
                    assert(quantity > 0)
                except:
                    error = "Please insert positive integer."
                else:
                    # add or delete quantity
                    if request.form['action'] == 'Add':
                        cart.addFood(request.form['size'],quantity)
                    elif request.form['action'] == 'Delete':
                        cart.deleteFood(request.form['size'], quantity)

            else:
                error='Please insert quantity with integer.'

        # empty cart and return to menu
        elif 'cancel' in request.form:
            cart.empty()
            return redirect(url_for('menu', id=id))
        
        # add food into order and empty cart
        elif 'confirm' in request.form:
            for size in cart.items.keys():
                food = system.getFood(drinks_or_sides, size)
                new_food = copy.deepcopy(food)
                order.addFood(new_food, cart.items[size])
            
            cart.empty()
            return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info, price=computePrice(cart), error=error, orderedItem=cart._items, finish=True)
                
        elif 'return' in request.form:
            return redirect(url_for('menu', id=id))

    return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info, price=computePrice(cart), error=error,orderedItem=cart._items)



# displaying order detail. If order is submitted, it allows user to refresh to get latest order status and optionally send email.
# If order is not submitted, it will notify user to continue order by go to home page.
# if the order has been picked up, customer can still send receipt (if order has not been deleted by staff)
@app.route('/order/details/<todo>/<id>', methods=['GET', 'POST'])
def order_details(id, todo):
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html', msg=str(er))
    
    # order.updateOrder('Pending')
    msg = str(order)
    msg = Markup(msg.replace('\n', '<br/>'))
    status=order.orderStatus
    
    if request.method == 'POST':
        # if user would like to refresh order status
        if 'refresh' in request.form:
            return redirect(url_for('order_details',id=id,todo=todo))
        
        # if user would like to send receipt to eamil
        elif 'sendEmail' in request.form and 'email' in request.form and request.form['email'] != "":
            return render_template('order_details.html', msg=msg, status=status, email=request.form['email'], send=True)
        
        # if the order is not submitted, and user want to continue ordering
        elif 'continueOrder' in request.form:
            return redirect(url_for('menu', id=id))
        
        # simulate pick up action
        elif 'pickup' in request.form:
            order.updateOrder("Picked Up")
            return redirect(url_for('order_details',id=id,todo=todo))

    return render_template('order_details.html', msg=msg, status=status, todo=todo)

#beside each order has a button to indicate preparing/ready for pickup
@app.route('/staff',methods = ['GET', 'POST'])
def staff():
    # list to store order detail in str
    msgList = []
    error = ''
    orderList = system.order
    filterList = [None]

    if request.method == "POST":
        
        # if staff wants to delte a particular order
        if 'delete' in request.form:
            id = request.form['delete'].split()[2]
            try:
                id = int(id)
            except:
                error = 'No such order'
            else:
                try:
                    system.deleteOrder(id)
                except SearchError as er:
                    error = str(er)

        # change orderStatus to 'Prepare'
        elif 'prepare' in request.form:
            id = request.form['prepare'].split()[2]
            try:
                id = int(id)
            except:
                error = 'No such order'
            else:
                try:
                    order = system.getNextOrder(None,id)
                except SearchError as er:
                    error = str(er)
                else:
                    order.updateOrder('Preparing')
        
        # chagne orderStatus to 'Ready'
        elif 'ready' in request.form:
            id = request.form['ready'].split()[1]
            try:
                id = int(id)
            except:
                error = 'No such order'
            else:
                try:
                    order = system.getNextOrder(None,id)
                except SearchError as er:
                    error = str(er)
                else:
                    order.updateOrder('Ready')

        # if staff wnats to filter order
        if 'filter' in request.form:
            if request.form['filter'] == 'All':
                pass
            else:
                filterList = [request.form['filter']]
                orderList = system.filterOrder(filterList)

    # read python str in Markup
    for elem in orderList:
        msg = str(elem)
        msg = Markup(msg.replace('\n', ' <br/>'))
        msgList.append(msg)

    return render_template('staff.html', msgList = msgList, filter=filterList[0], statusList=system.statusList, error = error)
    
# a page to dispaly current stock
@app.route('/stock',methods = ['GET', 'POST'])
def stock():
    
    stock = system.stock
    wholeStock = stock.whole
    error = ""

    if request.method == 'POST':
        
        if 'refresh' in request.form:
            return redirect(url_for('stock'))

        # if staff wants to refill stock
        elif 'refill' in request.form:
            quantity = request.form['quantity']
            food = request.form['target']
            
            # set defualt quantity by 0
            if quantity == '':
                quantity = 0
            
            try:
                quantity = int(quantity)
            except Exception as er:
                error = str(er)
            else:
                try:
                    stock.increaseQuantity(food,quantity)
                except Exception as er:
                    error = str(er)

    return render_template('stock.html', wholeStock = wholeStock,error=error)



# to run the project
if __name__ == "__main__":  # optionally add a name guard
    app.run(debug=True, port=5050)
