*Notes: Bold text just for easy reading, feel free to remove them.*

|ID |Priority|Points (1/day)|
|:-:|:------:|:----:|
|US1|Very High|4     |
|US2|  High   |3     |
|US3|low    |1     |
|US4|medium|2
|US5|medium|2
|US6|low|1
|US6|High|3


### **Epic story 1: As a customer, I would like to order and pay for my meal online.**

**US1:** As a customer, I would like to create mains and order their gourmet creation so I can avoid allergy and have my favourite food.

**AC:**

* **Two types of mains are offered: a burger or a wrap**.
* **A customer can choose number of buns**(e.g., 3 sesame buns for a double burger or 2 muffin buns for a standard single burger) - the number of buns cannot exceed the maximum allowable limit (e.g., if only single, double and triple burgers are permitted, then the customer cannot choose more than 4 buns).
* **A customer can also choose number of patties** (e.g., 2 chicken patties, vegetarian, beef). here again, customers are restricted to the maximum allowable patties.
* **Other ingredients of their choice should be provided** such as tomato, lettuce, tomato sauce, cheddar cheese, swiss cheese etc.
* **The base price of the mains and he additional price of each ingredient carries is displaced next to them**.
* **Once a customer has complete their gourmet creation, the net price of their created main will be calculated based on the chosen ingredients and displayed to the customer**.

-----
**US2**: As a customer, I would like to optionally order sides and drinks so I can have more types of food in the meal and won't get thirsty.

**AC:**

* The sides inclcude 2 size of nuggets (6 pack and 3 pack) and three sizes of fries (small, medium, large).
* The drinks can be either bottles (600ml) and cans (3075ml).
* Drinks such as orange juice has vary sizes (e.g., a small = 250 ml, a medium = 450 ml etc).

-----
**US3**: As a customer, I should be able to checkout to complete my order.

**AC:**

*  Once the customer checkout, a unique order-id will be issued to customer.
*  The order time is displayed on screen.

-----
**US4:** As a customer, I should be able to check the status of my order at any point so I can be notified if the order is completed.

**AC:**

*  If the order has been cooked, when the customer refresh their page at their end, their order status should change and indicate that the order is available for pickup by the customer.
*  The time that customer first place the order should be also displayed on the screen.

----
### **Epic story 2: As a staff for services, I would like to view and update the orders, so that I can acknowledge the current working progress and work more efficiently**

**US5:** As a staff for services, I should be able to view the current orders so that I can have an idea on my current workload.

**AC:**

* **The staff can view the order at any point in time**

----

**US6:** As a staff for services, I shoulld be able to update the status of the order so that when the order is ready I can serve the order to the customer more efficiently.


**AC:**

* **When the oder finishes, it should disappear from staff orders menu**
----
### **Epic story 3: As a staff for maintainance, I should be able to update the ingredientes quantities in the stock.**

**US7:** As a staff for maintainance, I should be able to update the ingredientes quantities in the stock according to the amount that customers' have ordered.

**AC:**
* **Burgers, wraps, nuggets should all stocked in whole quantities.**
* **Bottled drinks should stocked in either cans (375 ml) or bottles (600 ml)**
* **Drinks such as orange juiceshould be input as varying sizes** (e.g., a small = 250 ml, a medium = 450 ml etc).
* **Sides such as fries will need to be stocked by weight (in gms).**
* **When customers place an order, Inventory should be reduced the according amount**