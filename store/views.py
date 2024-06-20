from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .form import ExtendedUserCreationForm, ProductSearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    search_form = ProductSearchForm(request.GET)

    if search_form.is_valid() and search_form.cleaned_data['search_query']:
        search_query = search_form.cleaned_data['search_query']
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'cartItems': cartItems,
        'search_form': search_form,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    print("QUI RELOAD?")
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    orderItems = order.orderitem_set.all()
    for item in orderItems:
        item.delete()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def productDetail(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']

    product = get_object_or_404(Product, id=product_id)
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/product_detail.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = ExtendedUserCreationForm()

        if request.method == 'POST':
            form = ExtendedUserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')  # Password from form

                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    messages.error(request, 'Username or Email already exists')
                else:

                    user = form.save()
                    user.set_password(password)
                    user.save()

                    customer, created = Customer.objects.get_or_create(email=email)
                    if created:
                        customer.name = username
                    customer.user = user
                    customer.save()

                    login(request, user)
                    messages.success(request, 'Account created successfully')
                    return redirect('store')

        context = {'form': form}
        return render(request, 'store/register.html', context)
