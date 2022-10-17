from django.shortcuts import render
from .models import * 
from django.db.models import Q
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
# Create your views here.


def index(request): 
    search_query = request.GET.get('search', '')
    if search_query:
        post = Product.objects.filter(Q(name__icontains=search_query)| Q (brand__icontains=search_query))
    else:
        post = Product.objects.all()
    
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items #this is used to show cart items in bucket
    # else:
        # items = []
        # order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False} 
        # cartItems = order['get_cart_items']
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']

    context={
        'items':items,
        'post':post,
        'cartItems':cartItems,
    }
    return render(request, 'EcomWebApp/index.html', context)


def detail(request, pk):
    post = Product.objects.get(id=pk)
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all() #this order is came from above line which get or create the database of Order
    #     cartItems = order.get_cart_items
    # else:
        # items = [] #empty list(if user is not authenticated we return nothing)
        # order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False} #guest user login huda 0/0 dekhaune ho yo chai
        # cartItems = order['get_cart_items']
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    context ={
        'cartItems':cartItems,
        'post': post,
        'items':items,
    }
    return render(request, 'EcomWebApp/details.html', context)

def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all() #this order is came from above line which get or create the database of Order
    #     cartItems = order.get_cart_items  
    # else:

        # try:#this try and catch for guest user cookies cart error prevention method
        #     cart = json.loads(request.COOKIES['cart'])#this is for guest user cart items 
        # except:
        #     cart ={}
        # print('cart',cart)
        # items = [] #empty list(if user is not authenticated we return nothing)
        # order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False} #guest user login huda 0/0 dekhaune ho yo chai
        # cartItems = order['get_cart_items']

        # for i in cart:#this is for showing cart items in bucket in cart.html for i in cart means that cart which is bucket
        #     try:#product doesnot exist error occurs then try will be run and error is handled
        #         cartItems += cart[i]['quantity']
        #         product = Product.objects.get(id=i)


        #         total = (product.price - product.discount_price )* cart[i]['quantity']

        #         order['get_cart_total'] += total
        #         order['get_cart_items'] += cart[i]['quantity']

        #         item ={
        #             'product':{
        #                 'id':product.id,
        #                 'name':product.name,
        #                 'price':product.price ,
        #                 'imageURL':product.imageURL,
        #                 },
        #             'quantity':cart[i]['quantity'],
        #             'get_total':total
        #         }
        #         items.append(item)
        #         if product.digital == False: 
        #             order['shipping'] = True
        #     except:
        #         pass
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems,
    }
    return render(request, 'EcomWebApp/cart.html', context)

def checkout(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
        # items = []
        # order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False} 
        # cartItems = order['get_cart_items']
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context ={
        'items':items,
        'order':order,
        'cartItems':cartItems,
    }
    return render(request, 'EcomWebApp/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # print('Action:',action)
    # print('ProductId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False) #agadi ko customer ta attribute ho paxi ko mathillo line bata aako

    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product) #the reason here get_or_create() using is to get the orderitem value and add that value if it already exist not create new one when it's already exist

    if action =='add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe = False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # total =float(data['form']['total']) #this data came from json response and [form][total] is from checkout.html json.stringfy form is string and total is from userFormData
        # order.transaction_id = transaction_id  
        # # this is for js restriction whether user can change data from front end
        # if total == order.get_cart_total: #float(order.get_cart_total)
        #     order.complete = True
        # order.save()

        # if order.shipping == True:
        #     ShippingAddress.objects.create(# shippingaddress models ko objects haru create gareko if order model ma vayeko shipping method(property) true va vane 
        #         customer=customer,
        #         order = order,
        #         address = data['shipping']['address'],#came from json data of checkout.html
        #         city = data['shipping']['city'],
        #         state = data['shipping']['state'],
        #         postalcode = data['shipping']['postalcode'],
        #     )


    else:
        # print('User is not logged in')

        # print('COOKIES', request.COOKIES)
        # name = data['form']['name']
        # email = data['form']['email']

        # cookieData = cookieCart(request)
        # items = cookieData['items']
        # customer, created = Customer.objects.get_or_create(
        #     email = email,
        # )
        # customer.name = name
        # customer.save()

        # order = Order.objects.create(
        #     customer = customer,
        #     complete = False,
        # )
        # for item in items:
        #     product = Product.objects.get(id=item['product']['id'])
        #     orderItem = OrderItem.objects.create(
        #         product=product,
        #         order=order,
        #         quantity=item['quantity']
        #     )
        customer, order = guestOrder(request, data)

    total =float(data['form']['total']) #this data came from json response and [form][total] is from checkout.html json.stringfy form is string and total is from userFormData
    order.transaction_id = transaction_id  
        # this is for js restriction whether user can change data from front end
    if total == order.get_cart_total: #float(order.get_cart_total)
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(# shippingaddress models ko objects haru create gareko if order model ma vayeko shipping method(property) true va vane 
            customer=customer,
            order = order,
            address = data['shipping']['address'],#came from json data of checkout.html
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            postalcode = data['shipping']['postalcode'],
        )
    return JsonResponse('payment complete', safe=False)