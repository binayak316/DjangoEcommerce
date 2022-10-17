import json


import json
from .models import *

def cookieCart(request):
    try:#this try and catch for guest user cookies cart error prevention method
        cart = json.loads(request.COOKIES['cart'])#this is for guest user cart items 
    except:
        cart ={}
    print('cart',cart)
    items = [] #empty list(if user is not authenticated we return nothing)
    order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False} #guest user login huda 0/0 dekhaune ho yo chai
    cartItems = order['get_cart_items']

    for i in cart:#this is for showing cart items in bucket in cart.html for i in cart means that cart which is bucket
        try:#product doesnot exist error occurs then try will be run and error is handled
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)


            total = (product.price - product.discount_price )* cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price ,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
            if product.digital == False: 
                order['shipping'] = True
        except:
            pass
    return { 'items':items,'order':order,'cartItems':cartItems}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'items':items,'order':order,'cartItems':cartItems}


def guestOrder(request,data):
    print('User is not logged in')

    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order