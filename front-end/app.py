# import Flask library
from flask import Flask, render_template, request, redirect, url_for, abort, Markup,session, make_response
from init import bootstrap_system#, ser, orders
from src.errors import StockError, SearchError, bun_error, check_numBuns_error, checkStock
from src.shoppingCart import Cart

# create a flask project, assigning to a variable called app
app = Flask(__name__)
system = bootstrap_system()

# take in a Mains instance and extract information
def formatMains(food):
    assert(isinstance(food, Mains))

    pass


# take in a Drinks or Sides instance and extract information
def formatDS(food):
    info = {}
    for m in [system.drinksMenu, system.sidesMenu]:
        for i in m:
            if i.name == food:
                info[i.size] = f'{i.volumn}{i.unit} {i.price}'
                
    return info

# def fetch_session_cart(id):
#     # Creates a new cart first if the cart never existed
#     if 'cart' not in session:
#         print('cart not in session')
#         cart = Cart()
#         session['cart'] = id
#         orders[id] = cart
#     else:
#         # Check the current cookie is valid
#         print('cart in session')
#         try:
#             return orders[session['cart']]
#         except KeyError: 
#             print('exception raised: cart not in session')
#             cart = Cart()
#             session['cart'] = cart._id
#             orders[cart._id] = cart
#             print(cart._id)
#             print("session cookie from ex: " ,session['cart'])
#     return orders[session['cart']]

# a handler of root URL
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        
        # if user click "Check Status" button, ask for order ID
        if 'checkStatus' in request.form:
            return render_template('home.html', checkStatus=True)
        
        # if user click "Continue Order button, ask for order ID
        elif 'continueOrder' in request.form:
            return render_template('home.html', continueOrder=True)
        
        # if user click "Make New Order" button, create new order and redirect to menu page
        elif 'newOrder' in request.form:
            order = system.makeOrder()
            # fetch_session_cart(order.orderId)
            return redirect(url_for('menu', id=order.orderId))
        
        # if user insert orderID and comfirm "Check Status"
        elif 'confirmCS' in request.form  and 'id' in request.form:
            id = request.form['id']
            # try to get the order, if Error can be catch, display error msg on the same page
            try:
                order = system.getNextOrder(None, id)
            except (SearchError, ValueError) as er:
                return render_template('home.html', form=request.form, checkStatus=True,error=str(er))
            
            # if no error occur, redirect to order detail page
            else:
                return redirect(url_for('order_details', id=id, todo='checkStatus'))
            
        # if user insert orderID and confirm "Check Order"
        elif 'confirmCO' in request.form and 'id' in request.form:
            id = request.form['id']
            # try to get the order, if Error can be catch, display error msg on the same page
            try:
                order = system.getNextOrder(None, id)
            except (SearchError, ValueError) as er:
                return render_template('home.html', form=request.form, continueOrder=True, error=str(er))
            
            # if no error occur and the order is not submitted, redirect to order detail page
            else:
                if order.orderStatus != 'Not Submitted':
                    er = "Your order has been submitted, please go to 'Check Status'"
                    return render_template('home.html',  form=request.form, checkStatus=True, error=er)
                else:
                    return redirect(url_for('order_details', id=id, todo='continueOrder'))
        
    return render_template('home.html')

# displaying menu and handle ordering
@app.route("/menu/<id>", methods=["GET", "POST"])
def menu(id):
    try:
        order = system.getNextOrder(None,id)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))

    else:
        orderDetail = str(order).replace('\n', '<br/>')
        # print(orderDetail)
        return render_template('menu.html',id=id, order=Markup(orderDetail), mainsM=system.mainsMenu, drinksM=system.drinksMenu, sidesM=system.sidesMenu)


@app.route("/menu/<id>/Mains/<mains>", methods=["GET","POST"])
def Mains(id,mains):
    assert(mains!= None)
    try:
        food = system.getFood(mains)
    except SearchError as er:
        return render_template('errors.html', msg=str(er))
    # print('food is', food, 'type is ', type(food))
    
    if request.method == 'POST':
        numBun = request.form['Buns']
        # print(numBun, int(numBun))
        # int_numBun = int(numBun)
        numPat = request.form['Patties']
        # int_numPat = int(numPat)
        # print(numPat)
        
        ingreds = request.form['ingredients']
        # print('ingred is :', ingreds)
        ingredQty = request.form['quantity']
        # print('ingredqty is :', ingredQty)
        food.changeIngredients(ingreds,ingredQty)
        #whyyyyyyyyyy?????????????
        # food.addBuns(int_numBun)
        # food.addPats(int_numPat)
        # food._numBun = float(int_numBun)
        # food._numPat = float(int_numPat)
        print('food is', food)

        if 'confirm' in request.form:
            # put food into ordered list
            order = system.getNextOrder(None,id)
            # ERROR order not found here
            print(order)
            # not sure!!!!!!!!!
            order.orderedItem[food] = 1
            print(order)
            
            #put food in the cart
            # cart = fetch_session_cart()
            # cart._items.append(food)
            # print("no: ", len(cart._items))



    return render_template('mains.html', food=food)


@app.route("/menu/<id>/DrinksOrSides/<drinks_or_sides>", methods=["GET", "POST"])
def DrinksOrSides(id, drinks_or_sides):

    info = formatDS(drinks_or_sides)
    print(info)
    
    return render_template('drinks_or_sides.html', food=drinks_or_sides, info=info)



# displaying order detail. If order is submitted, it allows user to refresh to get latest order status and optionally send email.
# If order is not submitted, it allows user to continue order by redirecting to menu page.
@app.route('/order/details/<todo>/<id>', methods=['GET', 'POST'])
def order_details(id, todo):
    id = int(id)
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html', msg=str(er))
    '''
    try:
        order.updateOrder('dfdf')
    except Exception as er:
        return render_template('errors.html', msg=str(er))
    '''
    # order.updateOrder('Pending')
    msg = str(order)
    msg = Markup(msg.replace('\n', '<br/>'))
    status=order.orderStatus
    
    if request.method == 'POST':
        # if user would like to refresh order status
        if 'refresh' in request.form:
            return render_template('order_details.html', msg=msg, status=status)
        
        # if user would like to send receipt to eamil
        elif 'sendEmail' in request.form and 'email' in request.form and request.form['email'] != "":
            return render_template('order_details.html', msg=msg, status=status, email=request.form['email'], send=True)
        
        # if the order is not submitted, and user want to continue ordering
        elif 'continueOrder' in request.form:
            return redirect(url_for('menu', id=id))
     
    
    return render_template('order_details.html', msg=msg, status=status, todo=todo)



# to run the project
if __name__ == "__main__":  # optionally add a name guard
    app.run(debug=True)
