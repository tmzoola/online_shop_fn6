from django.shortcuts import render, reverse, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.http import HttpResponseRedirect



categories = Category.objects.all()


def index(request):
    products = Product.objects.all().select_related('category')
    data = {
        'products': products,
        'categories':categories
    }
    return render(request, 'store/index.html', context=data)

def category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    products = category.products.all()

    data = {
        'products': products,
        'categories':categories
    }

    return render(request, 'store/index.html', context=data)

def about(request):
    return render(request, 'store/about.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'store/login.html')
    return render(request, 'store/login.html')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def product(request, pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request, 'store/product.html', {'product': product})