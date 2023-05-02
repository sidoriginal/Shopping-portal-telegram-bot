# Shopping-portal-telegram-bot

## HOW TO RUN

Create your bot and generate API token using 'botfather' bot on telegram

Then put that token in TOKEN variable in the python script along with the user-id of another telegram account which will act as shop-owner in the variable USER_ID_A, then run the python script, run the script in vscode or any other code editor or IDE or terminal, before running make sure you have ‘python-telegram-bot’ version 13.3 library installed, if not run ‘pip install python-telegram-bot==13.3’ on your terminal before running python script, after that you can start chatting with the bot (Note that this only works with version 13 so make sure that specific version is installed).

## FEATURES
The features of telegram bots are:

### The upfront commands are: 
•	/start will show welcome message.

•	/help will guide user on how to order and complete his/her shopping.

•	First user has to register himself with a unique username using /register [username]. Then only he can start adding items to cart and can order.
It is to be noted that he has to register only once and can’t change the username once registered.

•	/shop will show user the list of available items

•	/add [product_name] [product_quantity] will allow user to add items to his/her cart

•	/remove [product_name] [product_quantity] will allow user to remove items from his/her cart

•	/cart will show user current status of his/her cart

•	/typeo [user_choice] will let user choose between delivery and pickup. It is to be noted that the choice will be mandatory to enter before ordering and after user fill it for the first time, it will be saved for future and user can change it.

•	/phone [user_mobile_number] will let user add the mobile number, without it user can't order, once user save it user don’t have to give it every time for every order, if user wants he/she can update it using the same. Also phone number is verified for being all number and also of length 10.

•	/address [delivery_address] will let user add the address when user want delivery, without it user can't order, once user save it user don’t have to give
address every time for every order, if user want user can update it using the same. It is to be noted that address is not necessary for pickup order.

•	/order will let user finalize user order, and it is advised to user to check cart before finalising the order.

•	/accept [user_name] will let the shop owner to accept the order of the certain user.

•	/decline [user_name] will let the shop owner to decline the order of the certain user. 

### Other features:
•	The inventory used here is locally declared in the program, but it is updated with every transaction, like when user adds a certain item in the cart that amount of item is deducted from the list, and upon removing it is added back. In case the shop owner declines the order, that particular order cart’s item is added back to the list of items and there are other basic managements like user can’t remove item if it is not present in the cart or if he tries to deduct greater number of items than in the cart, or if he wants to add a item which is not present or its quantity is zero.

•	There is a time limit for pickup and delivery options like if its past 8 pm user can’t choose pickup option or if its past 12 am user can’t choose delivery either, and he is prompted that he can continue shopping after 10 am tomorrow (when shop opens).

•	If the user has already placed an order and that order’s status hasn’t been confirmed yet, then that user can’t place another order, till the previous order status has been confirmed.

•	/accept and /decline command has been reserved for shop owner only and if customer tries to use it ‘Invalid command’ is shown to him/her



