from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .forms import productform
from django.views import View
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from store import forms
from django.contrib import messages

from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator 
from django.db.models import Sum
from django.core.mail import send_mail

def store(request):


    products= Product.objects.all()

    context ={'products': products}
    return render(request, 'store/store.html', context)

def product_upload(request):
    print(request.POST)
    
    if request.method == "POST":
        name = request.POST['name']
        
        price = request.POST['price']
        digital = request.POST['digital']
        image = request.FILES['image']
        
        Product.objects.create(name=name,price=price,digital=digital,image=image)
        
    return render(request, 'store/product-upload.html')



class myclassview(View):
    template = 'store/product-upload.html'
    context = {}
    def get(self, request):
        print("get request")
        context = self.context
        return render(request, self.template, context)
    
    def post(self, request):
        print(" in post request ")
        name = request.POST['name']
        
        price = request.POST['price']
        digital = request.POST['digital']
        image = request.FILES['image']
        
        Product.objects.create(name=name,price=price,digital=digital,image=image)
        context = self.context
        return render(request, self.template, context)







def home_view(request):
    context ={}
    context['form']= productform()

    if request.method == "POST":
        form = productform(request.POST)
        form.save()
    return render(request, 'store/product-upload.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
       items=[]
       cartItems=order['get_cart_item']




    context ={'items':items, 'order':order, 'cartItems':cartItems }
    return render(request, 'store/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems = order.get_cart_items

        

    else:
       items=[]
       order= {'get_cart_total':0,'get_cart_item':0}
       cartItems=order['get_cart_item']



    context ={'items':items, 'order':order, 'cartItems':cartItems }
    return render(request, 'store/checkout.html',context)



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

    return JsonResponse('Item was added', safe=False)



def specs(request):
    return render(request, 'store/specs.html')



def registerPage(request):
    print("here")
 
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')
            

    context = {'form':form}
    return render(request, 'store/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

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




def stock(request):

    Products = Product.objects.all()
    
    
    context = {
        
        "Products": Products,
        
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        Products = Product.objects.filter(name__icontains=name)

                                        
        context = {
        "Products": Products,
    }


    return render(request, "store/stock.html", context)




class Contact_us(View):
    template = 'store/contact-us.html'
    context = {}
    def get(self, request):
        print(" i am in get")
        context={}
        return render(request, self.template, context)
    
    def post(self, request):
        message=request.POST["message"]
        email=request.POST["email"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        message = f"Hi! This is {firstname}\n \n \n {message}\n \n Regards: \n {firstname} {lastname}\n Email:  {email}  "
        send_mail(
            'This User wants to contact with you',
            message,
            email,
            ['mirza.abdulrehman.336@gmail.com'],
    fail_silently=False,
)
        # messages.success(request,"Message submitted successfully! Thanks for contacting.")
        return render(request=request, template_name=self.template)


