# import Flask library
from flask import Flask, render_template, request, redirect, url_for, abort, Markup
from init import bootstrap_system
from src.errors import StockError, SearchError, bun_error, check_numBuns_error, checkStock

# create a flask project, assigning to a variable called app
app = Flask(__name__)
system = bootstrap_system()

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
                return redirect(url_for('order_details', id=id))
            
        # if user insert orderID and confirm "Check Order"
        elif 'confirmCO' in request.form and 'id' in request.form:
            id = request.form['id']
            # try to get the order, if Error can be catch, display error msg on the same page
            try:
                order = system.getNextOrder(None, id)
            except (SearchError, ValueError) as er:
                return render_template('home.html', form=request.form, continueOrder=True, error=str(er))
            
            # if no error occur, r edirect to order detail page
            else:
                return redirect(url_for('order_details', id=id))
        
    return render_template('home.html')

# displaying menu and handle ordering
@app.route("/menu/<id>", methods=["GET", "POST"])
def menu(id):
    
    
    
    return render_template('menu.html',id=id)

# displaying order detail. If order is submitted, it allows user to refresh to get latest order status and optionally send email.
# If order is not submitted, it allows user to continue order by redirecting to menu page.
@app.route('/order/details/<id>', methods=['GET', 'POST'])
def order_details(id):
    id = int(id)
    try:
        order = system.getNextOrder(None, id)
    except (SearchError, ValueError) as er:
        return render_template('errors.html', msg=str(er))
    msg = str(order)
    msg = Markup(msg.replace('\n', '<br/>'))
    status=order.orderStatus
    
    if request.method == 'POST':
        # if user would like to refresh order status
        if 'refresh' in request.form:
            return render_template('order_details.html', msg=msg, status=status)
        
        # if user would like to send receipt to eamil
        elif 'sendEmail' in request.form and 'email' in request.form:
            return render_template('order_details.html', msg=msg, status=status, email=request.form['email'], send=True)
        
        # if the order is not submitted, and user want to continue ordering
        elif 'continueOrder' in request.form:
            return redirect(url_for('menu', id=id))
        
    return render_template('order_details.html', msg=msg, status=status)


# to run the project
if __name__ == "__main__":  # optionally add a name guard
    app.run(debug=True)
