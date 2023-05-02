import telegram
from telegram.ext import Updater, CommandHandler
import datetime

TOKEN = 'YOUR-TOKEN'
USER_ID_A = 'USER-ID-OF-SHOP-OWNER'
USER_LIST={}
USER_ID_LIST={}
ORDER_LIST={}
ACTIVE_ORDER={}
CARTS = {}


ITEMS =[
    {'name': 'UncleChips', 'quantity': 120, 'price': 20,'weight':'50 gms','type':'chips'},
    {'name': 'Coke', 'quantity': 51, 'price': 90,'weight':'120 gms','type':'cold drink'},
    {'name': 'Mars', 'quantity': 71, 'price': 45,'weight':'20 gms','type':'choclate'},
    {'name': 'KitKat', 'quantity': 82, 'price': 60,'weight':'35 gms','type':'choclate'},
    {'name': 'Pepsi', 'quantity': 43, 'price': 90,'weight':'100 gms','type':'colddrink'},
    {'name': 'Snickers', 'quantity': 62, 'price': 60,'weight':'50 gms','type':'choclate'},
    {'name': 'Lays', 'quantity': 19, 'price': 20,'weight':'32 gms','type':'chips'},
    {'name': 'Fanta', 'quantity': 33, 'price': 20,'weight':'30 gms','type':'cold drink'},
    {'name': 'Twix', 'quantity': 71, 'price': 45,'weight':'15 gms','type':'chocltae'},
    {'name': 'Sprite', 'quantity': 34, 'price': 35,'weight':'40 gms','type':'cold drink'},
    {'name': 'Pears', 'quantity': 40, 'price': 60,'weight':'60 gms','type':'soap'},
    {'name': 'Axe', 'quantity': 23, 'price': 120,'weight':'120 gms','type':'deodrant'},
]


def gettime():
    now = datetime.datetime.now()
    k=2
    if now.hour >= 20:
        k=1
    if now.hour >=0 and now.hour < 10:
        k=2
    if now.hour >=10 and now.hour < 20:
        k=3
    return k




def help(update,context):
    user_id = update.message.from_user.id
    message="""
     First register yourself with a unique username using /register [username]. Then only you can start adding items to your cart and can order.
    
    /shop will show you list of available items
    
    /add [product_name] [product_quantity] will allow you to add items to your cart
    
    /remove [product_name] [product_quantity] will allow you to remove items from your cart
    
    /cart will show you current status of your cart
    
    /typeo [your_choice] will let you choose between delivery and pickup
    
    /phone [your_mobile_number] will let you add the mobile number, without it you can't order, once you save it you dont have to give it every time for every order, if you want you can update it using the same.
    
    /address [delivery_address] will let you add the address where you want delivery, without it you can't place delivery order, once you save it you dont have to give address every time for every order, if you want you can update it using the same.
    
    /order will let you finalize your order, please make sure to comfirm your order details by viewing /cart
    """
    context.bot.send_message(chat_id=user_id, text=message)

def start(update,context):
    user_id = update.message.from_user.id
    message="""
     Welcome to the e-portal of our shop.
    
    Here  you can order things from wide range of products.
    
    You can choose between either delivery or pickup methods.
    
    use /help to know how to order.
    """
    context.bot.send_message(chat_id=user_id, text=message)

def register(update,context):
    user_id = update.message.from_user.id
    if user_id in USER_LIST:
        message=f'You have already registered with this {USER_LIST.get(user_id)}'
        context.bot.send_message(chat_id=user_id, text=message)
    else:
        text=reg_text = update.message.text
        text=str(text)
        if(text=="/register"):
            context.bot.send_message(chat_id=user_id, text="User name can't be empty")
            return
        reg_text = update.message.text.replace('/register ', '')
        if reg_text!="":
            if reg_text in USER_ID_LIST:
                context.bot.send_message(chat_id=user_id, text=f"The user-name '{reg_text}' already exists")
                return
            USER_LIST[user_id]=reg_text
            ACTIVE_ORDER[user_id]=0
            USER_ID_LIST[reg_text]=user_id
            context.bot.send_message(chat_id=user_id, text="Successfully registered")
        else:
            context.bot.send_message(chat_id=user_id, text="User name can't be empty")
            return


def remove(update, context):
    user_id = update.message.from_user.id
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
        return
    if user_id not in CARTS:
        context.bot.send_message(chat_id=user_id, text="Your cart is already empty")
        return
    if ACTIVE_ORDER[user_id]==1:
        context.bot.send_message(chat_id=user_id, text="Your cart is empty")
        return
    message = update.message.text
    item_name = message.split()[1]
    item_quantity = int(message.split()[2])
    if item_name not in CARTS[user_id]:
        context.bot.send_message(chat_id=user_id, text="This item is not in your cart")
        return
    else:
        if item_quantity>CARTS[user_id][item_name]:
            context.bot.send_message(chat_id=user_id, text=f"You only have {CARTS[user_id][item_name]} in your cart. Please remove valid quantity")
        elif item_quantity==CARTS[user_id][item_name]:
            del CARTS[user_id][item_name]
            for item in ITEMS:
                if item['name'].lower() == item_name.lower():
                    item['quantity'] +=item_quantity
            context.bot.send_message(chat_id=user_id, text=f"Successfully removed {item_name} from your cart")
        else:
            CARTS[user_id][item_name]-=item_quantity
            for item in ITEMS:
                if item['name'].lower() == item_name.lower():
                    item['quantity'] +=item_quantity
            context.bot.send_message(chat_id=user_id, text=f"Successfully removed {item_quantity} {item_name} from your cart")
        return

def add(update, context):
    user_id = update.message.from_user.id
    if ACTIVE_ORDER[user_id]==1:
        context.bot.send_message(chat_id=user_id, text="Your previous order hasn't been confirmed yet, please wait for the order to be confirmed to continue shopping")
        return
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
        return
    if user_id not in CARTS:
        CARTS[user_id] = {}
    message = update.message.text
    item_name = message.split()[1]
    item_quantity = int(message.split()[2])
    for item in ITEMS:
        if item['name'].lower() == item_name.lower():
            if item_quantity <= item['quantity']:
                if item_name not in CARTS[user_id]:
                    CARTS[user_id][item_name] = 0
                CARTS[user_id][item_name] += item_quantity
                item['quantity'] -= item_quantity
                context.bot.send_message(chat_id=user_id, text=f"{item_quantity} {item_name} added to cart!")
            else:
                context.bot.send_message(chat_id=user_id, text=f"Sorry, only {item['quantity']} {item_name} available!")
            break
    else:
        context.bot.send_message(chat_id=user_id, text=f"Sorry, {item_name} not found!")

def cart(update, context):
    user_id = update.message.from_user.id
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
        return
    if ACTIVE_ORDER[user_id]==1:
        context.bot.send_message(chat_id=user_id, text="Your cart is empty")
        return
    if user_id not in CARTS or not CARTS[user_id]:
        context.bot.send_message(chat_id=user_id, text="Your cart is empty!")
        return
    else:
        total_price = 0
        message = "Your cart:\n\n"
        for item_name, item_quantity in CARTS[user_id].items():
            for item in ITEMS:
                if item['name'].lower() == item_name.lower():
                    message += f"{item_name} - {item_quantity} - Rs.{item['price']} each\n"
                    total_price += item_quantity * item['price']
                    break
        message += f"Total price: Rs.{total_price}\n\n"
        if 'typeo' in context.user_data:
            if context.user_data['typeo']=='delivery' and 'address' in context.user_data:
                message+=f"It is a {context.user_data['typeo']} order\n\n"
                message += f"Address: {context.user_data['address']}\n\n"
            elif context.user_data['typeo']=='delivery' and 'address' not in context.user_data:
                message+=f"It is a {context.user_data['typeo']} order\n\n"
            elif context.user_data['typeo']=='pickup':
                message+=f"It is a {context.user_data['typeo']} order\n\n"
        if 'phone' in context.user_data:
            message += f"Mobile number: {context.user_data['phone']}\n\n"
        message += f"User-name: {USER_LIST[user_id]}"
        context.bot.send_message(chat_id=user_id, text=message)

def shop(update, context):
    user_id = update.message.from_user.id
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
        return
    if ACTIVE_ORDER[user_id]==1:
        context.bot.send_message(chat_id=user_id, text="Your previous order hasn't been confirmed yet, please wait for the order to be confirmed to continue shopping")
        return
    context.bot.send_message(chat_id=user_id, text="Welcome to the store! Here's the list of items:")
    for item in ITEMS:
        context.bot.send_message(chat_id=user_id, text=f"{item['name']} - {item['quantity']} available - Rs.{item['price']} each - type: {item['type']} - weight: {item['weight']}")


def address(update, context):
    user_id = update.message.from_user.id
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
    address_text = update.message.text.replace('/address ', '')
    context.user_data['address'] = address_text
    context.bot.send_message(chat_id=user_id, text="Your address has been saved!")

def phone(update, context):
    user_id = update.message.from_user.id
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
    phone_text = update.message.text.replace('/phone ', '')
    if(phone_text.isdigit() and len(phone_text)== 10):
        context.user_data['phone'] = phone_text
        context.bot.send_message(chat_id=user_id, text="Your mobile number has been saved!")
    else:
        context.bot.send_message(chat_id=user_id, text="Please enter valid mobile number")



def order(update, context):
    user_id = update.message.from_user.id
    k=gettime()
    if k==2:
        context.bot.send_message(chat_id=user_id, text="Delivery and pickup options are closed for now, please order after 10 am tomorrow")
        return
    if user_id not in USER_LIST:
        context.bot.send_message(chat_id=user_id, text="""Please register your self first using /register [Your unique username]""")
        return
    if 'typeo' not in context.user_data:
        context.bot.send_message(chat_id=user_id, text="Please choose either delivery or pickup using /typeo [your_choice]")
        return
    if context.user_data['typeo']=='delivery' and 'address' not in context.user_data:
        context.bot.send_message(chat_id=user_id, text="Please enter your address first using /address {your address}")
        return
    if 'phone' not in context.user_data:
        context.bot.send_message(chat_id=user_id, text="Please enter your mobile number first using /phone [your_mobile_number]")
        return
    if user_id not in CARTS or not CARTS[user_id]:
        context.bot.send_message(chat_id=user_id, text="Your cart is empty!")
    else:
        message = "Order:\n\n"
        total_price = 0
        for item_name, item_quantity in CARTS[user_id].items():
            for item in ITEMS:
                if item['name'].lower() == item_name.lower():
                    message += f"{item_name} - {item_quantity} - Rs.{item['price']} each\n"
                    total_price += item_quantity * item['price']
                    break
        message += f"\nTotal price: Rs.{total_price}\n\n"
        if context.user_data['typeo']=='delivery' and 'address' in context.user_data:
                message+=f"It is a {context.user_data['typeo']} order\n\n"
                message += f"Address: {context.user_data['address']}\n\n"
        elif context.user_data['typeo']=='delivery' and 'address' not in context.user_data:
                message+=f"It is a {context.user_data['typeo']} order\n\n"
        elif context.user_data['typeo']=='pickup':
                message+=f"It is a {context.user_data['typeo']} order\n\n"
        message += f"Mobile number: {context.user_data['phone']}\n\n"
        message += f"User-name: {USER_LIST[user_id]}"
        ORDER_LIST[USER_LIST[user_id]]=message
        context.bot.send_message(chat_id=user_id, text=message)

        context.bot.send_message(chat_id=USER_ID_A, text=f"NEW ORDER RECEIVED\n\n{message}")
        context.bot.send_message(chat_id=user_id, text="Your order has been received!")
        ACTIVE_ORDER[user_id]=1

def accept(update, context):
    user_id = update.message.from_user.id
    if int(user_id) != int(USER_ID_A):
        context.bot.send_message(chat_id=user_id, text="Invalid command")
    else:
        text = update.message.text.replace('/accept ', '')
        if text not in ORDER_LIST:
                message = "No order by this user has been received"
                context.bot.send_message(chat_id=USER_ID_A, text=message)
        else:
                send_id=USER_ID_LIST[text]
                ACTIVE_ORDER[send_id]=0
                del CARTS[send_id]
                message= "Your order has been accepted"
                context.bot.send_message(chat_id=send_id, text=message)
                message=f"You accepted {text}'s order"
                context.bot.send_message(chat_id=USER_ID_A, text=message)
                del ORDER_LIST[text]

def decline(update, context):
    user_id = update.message.from_user.id
    if int(user_id) != int(USER_ID_A):
        context.bot.send_message(chat_id=user_id, text="Invalid command")
    else:
        text = update.message.text.replace('/decline ', '')
        if text not in ORDER_LIST:
                message = "No order by this user has been received"
                context.bot.send_message(chat_id=USER_ID_A, text=message)
        else:
                send_id=USER_ID_LIST[text]
                message= "We are sorry to say that, we cannot fullfill your order at the moment"
                for item_name, item_quantity in CARTS[send_id].items():
                    for item in ITEMS:
                        if item['name'].lower()==item_name:
                            item['quantity']+=item_quantity
                ACTIVE_ORDER[send_id]=0
                del CARTS[send_id]
                context.bot.send_message(chat_id=send_id, text=message)
                message=f"You declined {text}'s order"
                context.bot.send_message(chat_id=USER_ID_A, text=message)
                del ORDER_LIST[text]


def typeo(update, context):
    k=gettime()
    user_id = update.message.from_user.id
    text = update.message.text.replace('/typeo ', '')
    text=str(text).lower()
    if text=='delivery':
        if(k==2):
            context.bot.send_message(chat_id=user_id, text=f"Delivery and pickup options are closed for now, please order after 10 am tomorrow")
            return
        context.user_data['typeo']=text
        context.bot.send_message(chat_id=user_id, text=f"You chose {text}")
    elif text=='pickup':
        if(k==2):
            context.bot.send_message(chat_id=user_id, text=f"Delivery and pickup options are closed for now, please order after 10 am tomorrow")
            return
        if(k==1):
            context.bot.send_message(chat_id=user_id, text=f"Pickup option is closed till 10 am tomorrow, please choose delivery")
            return
        context.user_data['typeo']=text
        context.bot.send_message(chat_id=user_id, text=f"You chose {text}")
    else:
        context.bot.send_message(chat_id=user_id, text="Please choose either delivery or pickup")



updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('shop', shop))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('remove', remove))
updater.dispatcher.add_handler(CommandHandler('cart', cart))
updater.dispatcher.add_handler(CommandHandler('order', order))
updater.dispatcher.add_handler(CommandHandler('accept', accept))
updater.dispatcher.add_handler(CommandHandler('decline', decline))
updater.dispatcher.add_handler(CommandHandler('address', address))
updater.dispatcher.add_handler(CommandHandler('register', register))
updater.dispatcher.add_handler(CommandHandler('phone', phone))
updater.dispatcher.add_handler(CommandHandler('typeo', typeo))
updater.start_polling()
updater.idle()