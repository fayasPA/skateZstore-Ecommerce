from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model,login,logout
from django.views.decorators.cache import never_cache
from .models import Category,Product, ProductImage
from website.models import *
from django.http import JsonResponse,HttpResponse

import os
# paginator stuff
from django.core.paginator import Paginator

# Create your views here.
User = get_user_model()
@never_cache
def adminlogin(request):
    if request.user.is_superuser:               # Checking if user is logged in already
        return redirect(admindashboard)

    if request.method == 'POST':
        useradmin = request.POST['useradmin']
        password = request.POST['password']
        user = auth.authenticate(username=useradmin,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect(admindashboard)
        else:
            messages.error(request, 'Username or Password is Incorrect')
    return render(request,'admin/adminlogin.html')

@never_cache
def admindashboard(request):
    if request.user.is_superuser:
        orders = HistoryOrder.objects.all()
        products = Product.objects.all()
        category = Category.objects.all()
        user_count = myUser.objects.all().count()
        order_count = HistoryOrder.objects.all().count()
        delivery_count = HistoryOrder.objects.filter(status="Delivery").count()
        cat_count = []
        for c in category:
            cat_count.append(Product.objects.filter(category=c.id).count())
        
        ordered_dates = orders.order_by('ordered_date').distinct()         #get pythonic way of ordered dates in distinct ascending order
        for i in ordered_dates:
            print(i.ordered_date.strftime('%Y-%m-%d'))
            print(i.ordered_date)
        
        # for od in ordered_dates:

        context = {
            'products' : products,
            "category" : category,
            "orders" : orders,
            "user_count" : user_count,
            "cat_count" : cat_count,
            "order_count" : order_count,
            "delivery_count" : delivery_count,
        }
        return render(request,'admin/admindashboard.html',context)
    return redirect(adminlogin)

@never_cache
def adminuser(request):
    if request.user.is_superuser:
        user_list=User.objects.all()
        print(user_list)
        # p = Paginator(User.objects.all().order_by('username'),8)          #set up pagination
        # page = request.GET.get('page')
        # user_list = p.get_page(page)
        return render(request,'admin/adminuser.html',{'user_list':user_list})
    return redirect(adminlogin)
    
@never_cache
def adminlogout(request):
    if request.user.is_superuser:
        logout(request)
    return redirect(adminlogin)

@never_cache
def adminblock(request,id):
    if request.user.is_superuser:
        user = User.objects.get(pk=id)
        if user.is_active:
            user.is_active=False
            user.save()
            return redirect(adminuser)
        else:
            user.is_active=True
            user.save()
            return redirect(adminuser)
    return redirect(adminlogin)

@never_cache
def admincategory(request):
    if request.user.is_superuser:
        categories = Category.objects.all().order_by('category_name')
        if request.method=='POST':
            single_category = Category()
            single_category.category_name = request.POST['categ_name']
            single_category.category_image = request.FILES['categ_image']
            single_category.save()
            return redirect(admincategory)
        return render(request,'admin/admincategory.html',{'categories':categories})
    return redirect(adminlogin)

@never_cache
def edit_category(request,id):
    if request.user.is_superuser:
        category = Category.objects.get(id=id)
        if request.method=='POST':
            category.category_name = request.POST['categ_name']
            # if request.FILES.get('categ_image')!=None and category.category_image:
            #     os.remove(category.category_image.path)         # Removing Path
            category.category_image = request.FILES.get('categ_image',category.category_image)
            category.save()
            return redirect(admincategory)
        return render(request,'admin/edit_category.html',{'category':category})
    return render(adminlogin)


@never_cache
def delete_category(request,id):
    if request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(admincategory)
    return redirect(adminlogin)



@never_cache
def adminproduct(request):
    if request.user.is_superuser:
        products = Product.objects.all()
        # p = Paginator(Product.objects.all().order_by('product_name'),3)          #set up pagination
        # page = request.GET.get('page')
        # products = p.get_page(page)
        return render(request,'admin/adminproduct.html',{'products':products})
    return redirect(adminlogin)


@never_cache
def admin_addproduct(request):
    if request.user.is_superuser:
        category_list = Category.objects.all()
        if request.method=='POST':
            single_product = Product()
            single_product.product_name = request.POST['product_name']
            single_product.product_price = request.POST['product_price']
            single_product.product_description = request.POST['product_description']
            cat_id = request.POST['product_category']                               
            single_product.category = Category.objects.get(id=cat_id)
            single_product.product_qty = request.POST['product_qty']
            single_product.product_image = request.FILES['product_image']
            single_product.save()
            if request.FILES.get('product_images')!=0:
                images = request.FILES.getlist('product_images')
                for img in images:
                    imag = ProductImage.objects.create(product=single_product,product_image=img)
                    imag.save()
            return redirect(adminproduct)
        return render(request,'admin/admin_addproduct.html',{'category_list':category_list})
    return redirect(adminlogin)



def edit_product(request,id):
    if request.user.is_superuser:
        product = Product.objects.get(pk=id)
        if request.method=='POST':
            product.product_name = request.POST['prod_name']
            product.product_price = request.POST['prod_price']
            cat_id = request.POST['prod_categ']
            product.category = Category.objects.get(id=cat_id)
                    # os.remove(product.product_image.path)         # Removing Path
            product.product_image = request.FILES.get('prod_img',product.product_image)
            # EXTRA IMAGES
            ei = ProductImage.objects.filter(product_id=id)
            imag = request.FILES.getlist('extra_images')
            count = len(imag)
            i = 0
            for im in ei:
                if count == 0:
                    break
                im.product_image = imag[i]
                print(im.product_image)
                count = count-1
                i = i+1
                im.save()           
            # EXTRA IMAGES
            product.save()
            return redirect(adminproduct)
        # Cart.objects.filter(id=id).update(quantity=qty)
        category_list = Category.objects.all()
        return render(request, 'admin/edit_product.html',{'product':product,'category_list':category_list})
    return redirect(adminlogin)

@never_cache
def delete_product(request,id):
    if request.user.is_superuser:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect(adminproduct)
    return redirect(adminlogin)

@never_cache
def order_list(request):
    if request.user.is_superuser:
        orders = HistoryOrder.objects.all()
        choices = HistoryOrder.status.field.choices
        choice = []
        i=0
        for i in choices:
            choice.append(i[0])
        return render(request,'admin/order_list.html',{'orders':orders,'choice':choice})
    return redirect(adminlogin)

@never_cache
def status_update(request):
    if request.method == 'GET':
        id = request.GET['orderid']
        status = request.GET['stats']
        HistoryOrder.objects.filter(id=id).update(status=status)
        return JsonResponse({'status':"Status has been changed"})
