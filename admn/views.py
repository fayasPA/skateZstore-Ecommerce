from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.views.decorators.cache import never_cache
from .models import Category, Product, ProductImage
from website.models import *
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from django.db.models import Q


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
        user = auth.authenticate(username=useradmin, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect(admindashboard)
        else:
            messages.error(request, 'Username or Password is Incorrect')
    return render(request, 'admin/adminlogin.html')


@never_cache
def admindashboard(request):
    if request.user.is_superuser:
        orders = HistoryOrder.objects.all()
        products = Product.objects.all()
        category = Category.objects.all()
        user_count = myUser.objects.all().count()
        order_count = HistoryOrder.objects.all().count()
        delivery_count = HistoryOrder.objects.filter(
            status="Delivered").count()
        cat_count  = []
        for c in category:
            cat_count.append(Product.objects.filter(category=c.id).count())

        # 1 week sales report:
        # get pythonic way of ordered dates in distinct ascending order
        orders2 = orders.order_by('-ordered_date')
        first_date = datetime.now().date()
        last_date = first_date - timedelta(days=6)
        amntperday_list = []
        date_list = []
        for i in range(1, 8):
            tot_amnt_per_day = 0
            for order in orders2:
                if (order.ordered_date.date() == first_date):
                    tot_amnt_per_day = tot_amnt_per_day + order.amount
            amntperday_list.append(tot_amnt_per_day)
            date_list.append(first_date)
            first_date = first_date - timedelta(days=1)

        context = {
            'products': products,
            "category": category,
            "orders": orders,
            "user_count": user_count,
            "cat_count": cat_count,
            "order_count": order_count,
            "delivery_count": delivery_count,
            "amntperday_list": amntperday_list,
            "date_list": date_list,
        }
        return render(request, 'admin/admindashboard.html', context)
    return redirect(adminlogin)


@never_cache
def dailysaleschart(request):
    if request.method == 'GET':
        orders = HistoryOrder.objects.all().order_by('-ordered_date')
        start = parse_date(request.GET['start'])
        end = parse_date(request.GET['end'])
        limit = int(str(end - start).split()[0])
        amntperday_list = []
        date_list = []
        print("START", start)
        print("STARTTime", start)
        for i in range(1, limit+2):
            tot_amnt_per_day = 0
            for order in orders:
                if (order.ordered_date.date() == start):
                    tot_amnt_per_day = tot_amnt_per_day + order.amount
            amntperday_list.append(tot_amnt_per_day)
            date_list.append(start)
            start = start + timedelta(days=1)
        return JsonResponse({'date_list': date_list, 'amntperday_list': amntperday_list})


@never_cache
def adminuser(request):
    if request.user.is_superuser:
        user_list = User.objects.all()
        print(user_list)
        # p = Paginator(User.objects.all().order_by('username'),8)          #set up pagination
        # page = request.GET.get('page')
        # user_list = p.get_page(page)
        return render(request, 'admin/adminuser.html', {'user_list': user_list})
    return redirect(adminlogin)
    
@never_cache
def adminlogout(request):
    if request.user.is_superuser:
        logout(request)
    return redirect(adminlogin)


@never_cache
def adminblock(request, id):
    if request.user.is_superuser:
        user = User.objects.get(pk=id)
        if user.is_active:
            user.is_active = False
            user.save()
            return redirect(adminuser)
        else:
            user.is_active = True
            user.save()
            return redirect(adminuser)
    return redirect(adminlogin)


@never_cache
def admincategory(request):
    if request.user.is_superuser:
        categories = Category.objects.all().order_by('category_name')
        for c in categories:
            print(c.category_image)
        if request.method == 'POST':
            single_category = Category()
            single_category.category_name = request.POST['categ_name']
            single_category.category_image = request.FILES.get('categ_image',"")
            single_category.save()
            return redirect(admincategory)
        return render(request, 'admin/admincategory.html', {'categories': categories})
    return redirect(adminlogin)


@never_cache
def edit_category(request, id):
    if request.user.is_superuser:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            category.category_name = request.POST['categ_name']
            # if request.FILES.get('categ_image')!=None and category.category_image:
            #     os.remove(category.category_image.path)         # Removing Path
            category.category_image = request.FILES.get(
                'categ_image', category.category_image)
            category.save()
            return redirect(admincategory)
        return render(request, 'admin/edit_category.html', {'category': category})
    return render(adminlogin)


@never_cache
def delete_category(request, id):
    if request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect(admincategory)
    return redirect(adminlogin)


@never_cache
def adminproduct(request):
    if request.user.is_superuser:
        products = Product.objects.all().order_by('product_name')
        return render(request, 'admin/adminproduct.html', {'products': products})
    return redirect(adminlogin)


@never_cache
def admin_addproduct(request):
    if request.user.is_superuser:
        category_list = Category.objects.all()
        if request.method == 'POST':
            single_product = Product()
            single_product.product_name = request.POST['product_name']
            single_product.product_price = request.POST['product_price']
            single_product.product_description = request.POST['product_description']
            cat_id = request.POST['product_category']
            single_product.category = Category.objects.get(id=cat_id)
            single_product.product_qty = request.POST['product_qty']
            single_product.product_image = request.FILES['product_image']
            single_product.save()
            if request.FILES.get('product_images') != 0:
                images = request.FILES.getlist('product_images')
                for img in images:
                    imag = ProductImage.objects.create(
                        product=single_product, product_image=img)
                    imag.save()
            return redirect(adminproduct)
        return render(request, 'admin/admin_addproduct.html', {'category_list': category_list})
    return redirect(adminlogin)

@never_cache
def edit_product(request, id):
    if request.user.is_superuser:
        product = Product.objects.get(pk=id)
        if request.method == 'POST':
            product.product_name = request.POST['prod_name']
            product.product_price = request.POST['prod_price']
            cat_id = request.POST['prod_categ']
            product.category = Category.objects.get(id=cat_id)
            product.product_qty = request.POST['prod_qty']
            # os.remove(product.product_image.path)         # Removing Path
            product.product_image = request.FILES.get(
                'prod_img', product.product_image)
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
        return render(request, 'admin/edit_product.html', {'product': product, 'category_list': category_list})
    return redirect(adminlogin)


@never_cache
def delete_product(request, id):
    if request.user.is_superuser:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect(adminproduct)
    return redirect(adminlogin)

@never_cache
def order_list(request):
    if request.user.is_superuser:
        orders = HistoryOrder.objects.all().order_by('ordered_date')
        # choices = HistoryOrder.status.field.choices
        # choice = []
        # i = 0
        # for i in choices:
        #     choice.append(i[0])
        return render(request, 'admin/order_list.html', {'orders': orders})
    return redirect(adminlogin)

@never_cache
def status_update(request):
    if request.method == 'GET':
        id = request.GET['orderid']
        s = request.GET['stats']
        print("s",s)
        order = HistoryOrder.objects.get(id=id)
        order.status = s
        order.save()
        return JsonResponse({'status': "Status has been changed"})


@never_cache
def coupon(request):
    if request.user.is_superuser:
        coupons = Coupon.objects.all().order_by('code')
        if request.method == 'POST':
            code = request.POST['coupon_code']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            dis_amnt = request.POST['dis_amnt']
            min_amnt = request.POST['min_amnt']
            coupon_creation = Coupon.objects.create(
                code=code, valid_from=start_date, valid_to=end_date, discount_amnt=dis_amnt, min_amnt=min_amnt)
            coupon_creation.save()
        return render(request, 'admin/coupon.html', {'coupons': coupons})
    return redirect(adminlogin)

@never_cache
def edit_coupon(request, id):
    if request.user.is_superuser:
        single_coupon = Coupon.objects.get(id=id)
        start_date = single_coupon.valid_from.strftime("%Y-%m-%d")
        end_date = single_coupon.valid_to.strftime("%Y-%m-%d")
        context = {
            'single_coupon': single_coupon,
            'start_date': start_date,
            'end_date': end_date
        }
        if request.method == 'POST':
            single_coupon.code = request.POST['coupon_name']
            single_coupon.valid_from = request.POST['start_date']
            single_coupon.valid_to = request.POST['end_date']
            single_coupon.active = request.POST['active_coupon']
            single_coupon.discount_amnt = request.POST['dis_amnt']
            single_coupon.min_amnt = request.POST['min_amnt']
            single_coupon.save()
            return redirect(coupon)
        return render(request, 'admin/edit_coupon.html', context)
    return redirect(adminlogin)

@never_cache
def delete_coupon(request, id):
    Coupon.objects.get(id=id).delete()
    return redirect(coupon)

@never_cache
def block_coupon(request, id):
    c = Coupon.objects.get(id=id)
    print(c)
    if c.active:
        c.active = False
    else:
        c.active = True
    c.save()
    return redirect(coupon)

@never_cache
def offer(request):
    products = Product.objects.all()
    category = Category.objects.all()
    product_offers = ProductOffer.objects.all().order_by("id")
    category_offers = CategoryOffer.objects.all().order_by("id")
    for po in product_offers:
        # print(po.product_id)
        for p in products:
            if (po.product_id == p.id):
                p.product_offer = po.offer
                p.product_offer_price = p.product_price - \
                    (p.product_price * po.offer)/100
                p.save()
                print(p.product_offer_price)
    for co in category_offers:
        # print(po.product_id)
        for p in products:
            if (co.category_id == p.category_id):
                p.category_offer = co.offer
                p.category_offer_price = p.product_price - \
                    (p.product_price * co.offer)/100
                p.save()
                print(p.product_name, "=", p.category_offer_price)

    if request.method == 'POST':
        prod_id = request.POST['product']
        product = Product.objects.get(id=prod_id)
        start_date = request.POST['start_date']
        end_date = request.POST['expiry_date']
        offer = request.POST['offer']
        ProductOffer.objects.create(
            offer=offer, start_date=start_date, end_date=end_date, is_active=True, product=product)
        messages.info(request, "Offer Added")

    context = {
        'products': products,
        'product_offers': product_offers,
        'category': category,
        'category_offers': category_offers,
    }
    return render(request, 'admin/offer.html', context)


@never_cache
def edit_productoffer(request, id):
    if request.method == 'POST':
        # p_offer = ProductOffer.objects.get(id=id)
        prod_id = request.POST['product']
        product = Product.objects.get(id=prod_id)
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        offer1 = request.POST['offer']
        ProductOffer.objects.filter(id=id).update(
            offer=offer1, start_date=start_date, end_date=end_date, is_active=True, product=product)
        messages.info(request, "Offer Updated")
    return redirect(offer)


@never_cache
def removePoffer(request, id):
    ProductOffer.objects.get(id=id).delete()
    return redirect(offer)


@never_cache
def add_category_offer(request):
    if request.method == 'POST':
        categ_id = request.POST['categ']
        categ = Category.objects.get(id=categ_id)
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        offer1 = request.POST['offer']
        CategoryOffer.objects.create(
            offer=offer1, start_date=start_date, end_date=end_date, is_active=True, category=categ)
        messages.info(request, "Offer Added")
    return redirect(offer)


@never_cache
def removeCoffer(request, id):
    CategoryOffer.objects.get(id=id).delete()
    return redirect(offer)


@never_cache
def edit_categoryoffer(request, id):
    if request.method == 'POST':
        categ_id = request.POST['category']
        categ = Category.objects.get(id=categ_id)
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        offer1 = request.POST['offer']
        CategoryOffer.objects.filter(id=id).update(
            offer=offer1, start_date=start_date, end_date=end_date, is_active=True, category=categ)
        messages.info(request, "Offer Updated")
    return redirect(offer)

@never_cache
def salesreport(request):
    if request.user.is_superuser:
        orders = HistoryOrder.objects.all()
        if request.method == 'POST':
            start = request.POST['start']
            end = request.POST['end']
            print("type",type(start))
            orders = HistoryOrder.objects.all().filter(ordered_date__range=[start,end])
            m = "Showing results B/W " + start + ' and ' + end + " Dates"
            messages.info(request,m)
        print("FAYAS")
        return render(request, "admin/salesreport.html", {'orders': orders})
    return redirect(adminlogin)

@never_cache
def yearly_sales(request):
    orders = HistoryOrder.objects.all()
    if request.method == 'POST':
        print("FAYAS")
        year = request.POST['year']
        print("type",type(year))
        orders = orders.filter(Q(ordered_date__year=year))
        # for o in orders:
        #     print("DATE",o.ordered_date)
        print(len(orders))
        m = "Showing results for sales in " + year
        m1 = "No results found for '" + year + "'"
        if len(orders) == 0:
            messages.info(request,m1)
        else:
            messages.info(request,m)
    return render(request, "admin/salesreport.html", {'orders': orders})

@never_cache
def monthly_sales(request):
    orders = HistoryOrder.objects.all()
    if request.method == 'POST':
        month = request.POST['month']
        m = str(month).split('-')                           #splitting str value to take only month value
        orders = orders.filter(Q(ordered_date__month=m[1])) #searching for the month query
        month_names = ['Jan','Feb','March','April','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month_name = month_names[int(m[1])-1]
        print(month_name)
        m = "Showing results for sales in " + month_name
        m1 = "No results found for '" + month_name + "'"
        if len(orders) == 0:
            messages.info(request,m1)
        else:
            messages.info(request,m)
    return render(request, "admin/salesreport.html", {'orders': orders})
