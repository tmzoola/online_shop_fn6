from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render,get_object_or_404,reverse
from .cart import Cart
from store.models import Product,Order,OrderItem
from django.http import JsonResponse
import uuid
from decimal import Decimal
from django.http import HttpResponseRedirect
from .telegram import main
import asyncio
def cart_summary(request):
    cart = Cart(request)
    cart_prods = cart.get_products()
    prod_count = cart.get_quantity()

    total = cart.get_total()

    data = {
        'cart_prods': cart_prods,
        'prod_count': prod_count,
        'total': total
    }

    return render(request, 'cart/cart_summary.html',context=data)

def cart_add(request):
    #getcart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_count = int(request.POST.get('prod_count'))
        product = get_object_or_404(Product,id=product_id)

        #save to session
        cart.add(product=product, quantity=product_count)

        cart_quantity = cart.__len__()

        return JsonResponse({'quantity':cart_quantity})

    return render(request, 'cart/add')
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product_id=product_id)

        return JsonResponse({'status':'success'})

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_count = int(request.POST.get('prod_count'))

        cart.update(product=product_id, quantity=product_count)

        return JsonResponse({'quantity':product_count})

def order_details(request):
    cart = Cart(request)
    all_info =cart.get_all_info()

    if request.user.id is None:
        return HttpResponseRedirect(reverse('login_page'))
    else:
        order = Order()
        order.user_id = request.user
        order.order_id = uuid.uuid4()
        order.total_price = cart.get_total()
        order.save()

        for info in all_info:
            order_item = OrderItem(
                order=order,
                product_id=int(info['id']),
                name=info['name'],
                price=Decimal(info['price']),
                quantity=int(info['quantity'])
            )
            order_item.save()

        cart.cart_clear()
        asyncio.run(main(f"{all_info}"))
        return HttpResponseRedirect(reverse('index'))

@login_required
def order_info(request):
    orders = Order.objects.filter(user_id=request.user)

    result = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        data = {'order': order.order_id, 'items': order_items}
        result.append(data)

    data = {'orders': result}

    return render(request, 'cart/orders.html',context=data)