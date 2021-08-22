from django.shortcuts import render
from Home.models import Product
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == 'POST':
        name = request.POST['product']
        if name != '':
            try:
                p = Product.objects.get(product_name__iexact=name)
                return render(request,'Home/home.html',{'product':p,'PRODUCT':True})
            except Exception as e:
                print(e)
                messages.info(request, 'No Stored !')
                p = Product.objects.order_by('-rating__rate')[:5]
                return render(request,'Home/home.html',{'data':p})
        else:
            messages.warning(request, 'Name of the Product Required !')
            p = Product.objects.order_by('-rating__rate')[:5]
            return render(request,'Home/home.html',{'data':p})
    else:
        p = Product.objects.order_by('-rating__rate')[:5]
        return render(request,'Home/home.html',{'data':p})

