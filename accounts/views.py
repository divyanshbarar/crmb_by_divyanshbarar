from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

from django.forms import inlineformset_factory

from .forms import*

from .filter import OrderFilter

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user,allowed_user,admin_only

# Create your views here.
@unauthenticated_user
def registerPage(request):
    
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

               
            group=Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(

                user=user,
                name=user.username,

                )

            messages.success(request,'Account is created for '+username)

            return redirect('login')


    context={'form':form}
    return render(request,'register.htm',context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')
    context={}
    return render(request,'login.htm',context)

def logoutUser(request):
    logout(request)
    return redirect('login')





@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()

    total_customer=customers.count()
    total_order=orders.count()
    delievered=orders.filter(status='Delievered').count()
    pending=orders.filter(status='pending').count()


    context={'orders':orders,'customers':customers,'total_customers':total_customer,'total_orders':total_order,'delievered':delievered,'pending':pending}
    return render(request,'dashboard.htm',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()

    total_order=orders.count()
    delievered=orders.filter(status='Delievered').count()
    pending=orders.filter(status='pending').count()
    context={'orders':orders,'total_orders':total_order,'delievered':delievered,'pending':pending}
    return render(request,'user.htm',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'acount_settings.htm', context)



@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products=Products.objects.all()
    return render(request,'products.htm',{'products':products})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()
    myfilter=OrderFilter(request.GET,queryset=orders)
    orders=myfilter.qs
    context={'customer':customer,'orders':orders,'order_count':order_count,'myfilter':myfilter}
    return render(request,'customer.htm',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request,pk_test):

    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk_test)

    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    
    if request.method=='POST':
        #print('printing POST',request.POST)
        #form=OrderForm()
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'order_form.htm',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request,pk_test):

    order=Order.objects.get(id=pk_test)
    formset=OrderForm(instance=order)
    if request.method=='POST':
        formset=OrderForm(request.POST,instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'formset':formset}
    return render(request,'order_form.htm',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request,pk_test):
    order=Order.objects.get(id=pk_test)
    if request.method =='POST':
        order.delete()
        return redirect('/')


    context={'item':order}
    return render(request,'delete.htm',context)