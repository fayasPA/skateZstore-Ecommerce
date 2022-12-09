from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.views.decorators.cache import never_cache
from website.mixins import messageHandler
from admn.models import *
from .models import *
# from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta


# Create your views here.
User = get_user_model()

@never_cache
def index(request):
    product = Product.objects.all().order_by('-product_offer')
    for p in product:
        print('prod',p.product_offer)
    if 'term' in request.GET:
        search_product = Product.objects.filter(product_name__istartswith=request.GET.get('term'))
        search_sugg = []
        for sp in search_product:
            search_sugg.append(sp.product_name)
        return JsonResponse(search_sugg,safe=False)         #safe argument is present inorder to send any other python datatype other than dictionaries
    return render(request, 'index.html',{'product':product})

@never_cache
def search(request):
    if request.method == 'GET':
        q = request.GET['search']
        query_list = Product.objects.filter(Q(product_name__icontains=q))
        if query_list is not None and query_list.count() != 0:
            p = Paginator(Product.objects.filter(product_name__icontains=q).order_by(
                'product_name'), 10)  # set up pagination
            page = request.GET.get('page')
            queries = p.get_page(page)
            return render(request, 'search.html', {'queries': queries, 'q': q})
        else:
            return render(request, 'search.html', {'message': "No result found", 'q': q})

@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        global phNo, username, email, first_name, password1
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phNo = request.POST['phone_number']
        country_code = request.POST['country_code']

        if len(username) < 3 or len(username) > 10:
            messages.error(
                request, 'Username must be atleast 3 and less than 10 characters ')
            return redirect(signup)
        if not username.isalnum():
            messages.error(
                request, 'Username must contain only numbers and letters')
            return redirect(signup)
        if not first_name.isalpha():
            messages.error(request, 'Only letters are to be entered in name')
            return redirect(signup)
        if len(phNo) < 10 or len(phNo) > 12:
            messages.error(request, 'Mobile Or Phone number is wrong')
            return redirect(signup)
        if password1 != password2:
            messages.error(request, 'Passwords does not match')
            return redirect(signup)

        if User.objects.filter(username=username).exists() or User.objects.filter(phone_number=phNo).exists():
            messages.error(request, 'Already taken user')
            return redirect(signup)

        else:
            mobsignup = country_code+phNo
            messageHandler(mobsignup).send_otp_on_phone()
            context = {
                'username' : username,
                'email' : email,
                'first_name' : first_name,
                'password1' : password1,
                'password2' : password2,
                'phNo' : phNo,
                'country_code' : country_code,
            }
            return render(request, 'signupotpver.html',context)
            # return redirect(signupotpver,context)
    return render(request, 'signup.html')

@never_cache
def signupotpver(request):
    if request.method == 'POST' and request.POST['otp']:
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phNo = request.POST['phone_number']
        country_code = request.POST['country_code']
        otp = request.POST['otp']
        mobsignup = country_code+phNo
        validation = messageHandler(mobsignup).validate(otp)
        if validation == 'approved':
            credentials = User.objects.create_user(
                username=username, email=email, password=password1, first_name=first_name, phone_number=phNo)  # creating user in database
            credentials.save()              # Saving user details in Database
            return redirect(LogIn)
        else:
            messages.error(request, 'OTP is Incorrect')
            context = {
                'username' : username,
                'email' : email,
                'first_name' : first_name,
                'password1' : password1,
                'password2' : password2,
                'phNo' : phNo,
                'country_code' : country_code,
            }
            return render(request, 'signupotpver.html',context)
            
@never_cache
def LogIn(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                guestuser = User.objects.get(username=request.COOKIES['cart'])
            except:
                guestuser = None
            print("usersCookie",guestuser)
            if guestuser is not None:
                guestcart = Cart.objects.filter(user=guestuser)
                for item in guestcart:
                    print(item.user.username,"item.product_idGusest",item.product_id)
                    usercart_count = Cart.objects.filter(user=user,product=item.product).count()
                    if Cart.objects.filter(user=user,product=item.product):
                        user_item = Cart.objects.get(user=user, product=item.product)
                        user_item.quantity = user_item.quantity + item.quantity                               # if user has same order that order item's quantity is increased
                        user_item.save()
                        item.delete()
                    else:
                        item.user_id = user.id
                        item.save()
                guestuser.delete()
            login(request, user)
            return redirect(index)
        else:
            messages.error(request, 'Username or Password is Incorrect')
    return render(request, 'LogIn.html')

@never_cache
def otplogin(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST' and request.POST['phone_number']:
        global phone_number
        phone_number = request.POST['phone_number']
        country_code = request.POST['country_code']

        try:  # User with No phone no is present thus error will show up
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = None
        if user is not None:
            global mob
            mob = country_code+phone_number
            messageHandler(mob).send_otp_on_phone()
            return redirect(otpver)
        else:
            messages.error(request, 'Phone Number is not registered with us')
    return render(request, 'otplogin.html')

@never_cache
def otpver(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST' and request.POST['otp']:
        otp = request.POST['otp']
        validation = messageHandler(mob).validate(otp)
        if validation == 'approved':
            user = User.objects.get(phone_number=phone_number)
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.error(request, 'OTP is Incorrect')
    return render(request, 'otpver.html')

@never_cache
def user_details(request):
    if request.user.is_authenticated:

        return render(request, 'user_details.html')
    return redirect(LogIn)

@never_cache
def edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            firstname = request.POST['firstname']
            email = request.POST['email']
            phonenumber = request.POST['phonenumber']
            password = request.POST['password']
            User.objects.filter(id=request.user.id).update(
                username=username, first_name=firstname, email=email, phone_number=phonenumber, password=password)
            return redirect(user_details)
        return render(request, 'edit_user.html')
    return redirect(index)

@never_cache
def add_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            type = request.POST['type']
            address = request.POST['address']
            pin = request.POST['pin']
            district = request.POST['district']
            state = request.POST['state']
            landmark = request.POST['landmark']
            phone_number = request.POST['phone_number']
            new_address = Address.objects.create(user=request.user, type=type, address=address,
                                                 pin=pin, district=district, state=state, landmark=landmark, phone_number=phone_number)
            new_address.save()
            return redirect(user_details)
        return render(request, 'add_address.html')

    return redirect(LogIn)

@never_cache
def edit_address(request, id):
    if request.user.is_authenticated:
        adrs = Address.objects.get(id=id)
        if request.method == 'POST':
            type = request.POST['type']
            address = request.POST['address']
            pin = request.POST['pin']
            district = request.POST['district']
            state = request.POST['state']
            landmark = request.POST['landmark']
            phone_number = request.POST['phone_number']
            new_address = Address.objects.filter(id=id).update(
                type=type, address=address, pin=pin, district=district, state=state, landmark=landmark, phone_number=phone_number)
            return redirect(user_details)
        return render(request, 'edit_address.html', {'adrs': adrs})
    return redirect(LogIn)

@never_cache
def delete_address(request, id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id)
        address.delete()
        return redirect(user_details)
    return redirect(index)

@never_cache
def LogOut(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(LogIn)

@never_cache
def prod_deck(request):
    p = Paginator(Product.objects.filter(category__category_name__contains="Decks").order_by(
        'product_name'), 10)  # set up pagination
    page = request.GET.get('page')
    products = p.get_page(page)
    return render(request, 'prod_deck.html', {'products': products})

@never_cache
def prod_wheel(request):
    p = Paginator(Product.objects.filter(category__category_name__contains="Wheels").order_by(
        'product_name'), 10)  # set up pagination
    page = request.GET.get('page')
    products = p.get_page(page)
    return render(request, 'prod_wheel.html', {'products': products})

@never_cache
def prod_trucks(request):
    p = Paginator(Product.objects.filter(category__category_name__contains="Trucks").order_by(
        'product_name'), 10)  # set up pagination
    page = request.GET.get('page')
    products = p.get_page(page)
    return render(request, 'prod_trucks.html', {'products': products})

@never_cache
def prod_details(request, id):
    prod_detail = Product.objects.get(id=id)
    prod_img_count = range(1, prod_detail.productimage_set.all().count() + 2)
    prod_img = []
    prod_img.append(prod_detail.product_image)
    prod_imgs = ProductImage.objects.filter(product=prod_detail.id)
    for i in prod_imgs:
        prod_img.append(i.product_image)
    print(prod_img)
    print(prod_img_count)
    context = {'prod_detail': prod_detail,
               'prod_img_count': prod_img_count,
               'prod_img': prod_img,
               }
    return render(request, 'prod_details.html', context)

@never_cache
def add_to_cart(request, id):
    product = Product.objects.get(id=id)                                # get product of given id
    if request.user.is_authenticated:
        user = request.user    
    else:
        device = request.COOKIES['cart']
        print(device)
        if User.objects.filter(username=request.COOKIES['cart']):
            user = User.objects.get(username=request.COOKIES['cart'])
        else:
            user = User.objects.create_user(username=request.COOKIES['cart'],phone_number=request.COOKIES['cart'])
    if Cart.objects.filter(user=user, product=product):         # Check whether this user has same order or not
        item = Cart.objects.get(user=user, product=product)
        item.quantity = item.quantity + 1                               # if user has same order that order item's quantity is increased
        item.save()
        return redirect(prod_details, id=id)
    else:                                                               # if user has no similar order creates a new order
        Cart.objects.create(user=user, product=product)
        return redirect(prod_details, id=id)

@never_cache
def cart(request):
    if request.user.is_authenticated:
        user = request.user    
    else:
        device = request.COOKIES['cart']
        try:
            user = User.objects.get(username=request.COOKIES['cart'],phone_number=request.COOKIES['cart'])
        except:
            user=None
    if Cart.objects.filter(user=user):
        orders = Cart.objects.filter(user=user).order_by('id')
        count = orders.count()
        tot_amount = 0
        for order in orders:
            tot_amount = tot_amount + order.get_final_price()
        return render(request, 'cart.html', {'orders': orders, 'tot_amount': tot_amount, 'count': count})
    return render(request, 'cart.html', {'message': "Your cart is empty"})
@never_cache
def qty_minus(request, id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.get(username=request.COOKIES['cart'])
    order_item = Cart.objects.get(id=id)
    qty = order_item.quantity-1
    Cart.objects.filter(id=id).update(quantity=qty)
    updated_price = Cart.objects.get(id=id).get_final_price()
    orders = Cart.objects.filter(user=user)
    tot_amount = 0
    for order in orders:
        tot_amount = tot_amount + order.get_final_price()
    return JsonResponse({'qty': qty, 'tot_amount': tot_amount, 'updated_price': updated_price})

@never_cache
def qty_plus(request, id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.get(username=request.COOKIES['cart'])
    order_item = Cart.objects.get(id=id)
    qty = order_item.quantity+1
    Cart.objects.filter(id=id).update(quantity=qty)
    updated_price = Cart.objects.get(id=id).get_final_price()
    orders = Cart.objects.filter(user=user)
    tot_amount = 0
    for order in orders:
        tot_amount = tot_amount + order.get_final_price()
    return JsonResponse({'qty': qty, 'tot_amount': tot_amount, 'updated_price': updated_price})

@never_cache
def removeitem(request, id):
    order_item = Cart.objects.get(id=id)
    order_item.delete()
    messages.info(request, "Item has been removed")
    return redirect(cart)

@never_cache
def checkout(request):
    if request.user.is_authenticated:
        orders = Cart.objects.filter(user=request.user)
        count = orders.count()
        tot_amount = 0
        for order in orders:
            tot_amount = tot_amount + order.get_final_price()
        return render(request, 'checkout.html', {'tot_amount': tot_amount, 'count': count, })
    return redirect(index)

@never_cache
def discount_coupon(request, code):
    now = datetime.now()
    orders = Cart.objects.filter(user=request.user)
    tot_amnt = 0
    try:
        coupon = Coupon.objects.get(Q(code__icontains=code))
    except:
        coupon = None
    for single_order in orders:
        tot_amnt = tot_amnt + single_order.get_final_price()
    if (coupon == None) or (tot_amnt < coupon.min_amnt) or (not coupon.active) or (now.date() < coupon.valid_from.date() or now.date() > coupon.valid_to.date()):
        if coupon == None:
            return JsonResponse({'errormessage': "INVALID coupon", 'coupon': None})
        elif (now.date() < coupon.valid_from.date() and now.date() > coupon.valid_to.date()):
            return JsonResponse({'errormessage': "Coupon Has Expired", 'coupon': None})
        elif tot_amnt < coupon.min_amnt:
            remaining_amnt = coupon.min_amnt - tot_amnt
            return JsonResponse({'errormessage': "Purchase for Rs." + str(remaining_amnt) + " more to apply this coupon", 'coupon': None})
        return JsonResponse({'errormessage': "Coupon is not VALID", 'coupon': None})
    else:
        new_tot_amnt = tot_amnt - coupon.discount_amnt
        dis_amnt = coupon.discount_amnt / orders.count()
        return JsonResponse({'tot_amnt': tot_amnt, 'new_tot_amnt': new_tot_amnt, 'message': "Coupon has been applied", 'coupon_amnt': coupon.discount_amnt, 'dis_amnt': dis_amnt, 'coupon': coupon.id})

@never_cache
def place_order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            orders = Cart.objects.filter(user=request.user)
            method = request.POST['paymentmethod']
            address_id = request.POST['address_chose']
            coupon_id = request.POST['couponid']
            if len(coupon_id) == 0:
                coupon = ""
            else:
                coupon = Coupon.objects.get(id=coupon_id)
            address = Address.objects.get(id=address_id)
            tot_amnt = 0
            if coupon == "":                                                   # if condition to pass correct amnt
                for single_order in orders:
                    tot_amnt = tot_amnt + single_order.get_final_price()
            else:                                                              # else condition to pass discounted amnt
                dis_amnt = round(coupon.discount_amnt / orders.count(),3)
                for single_order in orders:
                    tot_amnt = tot_amnt + \
                        (single_order.get_final_price() - dis_amnt)
                print("tot_amnt", tot_amnt)
            context = {
                "address_id": address_id,
                "coupon_id": coupon_id,
                "tot_amnt": tot_amnt,
            }
            if method == "COD":
                if coupon == "":
                    for single_order in orders:
                        p = Product.objects.get(id=single_order.product.id)
                        p.product_qty = p.product_qty - single_order.quantity
                        p.save()
                        HistoryOrder.objects.create(coupon_code=coupon, user=request.user, is_ordered=True,
                                                    method=method, product=single_order.product, quantity=single_order.quantity, amount=single_order.get_final_price(), address=address)
                else:
                    print("dis_amnt", dis_amnt)
                    for single_order in orders:
                        p = Product.objects.get(id=single_order.product.id)
                        tot_amnt = single_order.get_final_price() - dis_amnt
                        p.product_qty = p.product_qty - single_order.quantity
                        p.save()
                        HistoryOrder.objects.create(coupon_code=coupon.code, user=request.user, is_ordered=True,
                                                    method=method, product=single_order.product, quantity=single_order.quantity, amount=tot_amnt, address=address)
                orders.delete()
                messages.error(request, 'Order has been placed')
                return redirect(index)
            elif method == "paypal":
                return render(request, 'paypal.html', context)
            else:
                return render(request, 'razorpay.html', context)
    return redirect(index)

@never_cache
def razorpay(request):
    if request.method == 'GET':
        address_id = request.GET['address_id']
        coupon_id = request.GET['coupon_id']
        transaction_id = request.GET['trans_id']
        orders = Cart.objects.filter(user=request.user)
        address = Address.objects.get(id=address_id)
        if len(coupon_id) == 0:
            coupon = ""
        else:
            coupon = Coupon.objects.get(id=coupon_id)
        if coupon == "":
            for single_order in orders:
                p = Product.objects.get(id=single_order.product.id)
                p.product_qty = p.product_qty - single_order.quantity
                p.save()
                HistoryOrder.objects.create(coupon_code=coupon, user=request.user, is_ordered=True,
                                            method="razorpay", product=single_order.product, quantity=single_order.quantity, amount=single_order.get_final_price(), address=address)
        else:
            dis_amnt = round(coupon.discount_amnt / orders.count(),3)
            for single_order in orders:
                p = Product.objects.get(id=single_order.product.id)
                tot_amnt = single_order.get_final_price() - dis_amnt
                p.product_qty = p.product_qty - single_order.quantity
                p.save()
                HistoryOrder.objects.create(coupon_code=coupon.code, user=request.user, is_ordered=True,
                                            method="razorpay", product=single_order.product, quantity=single_order.quantity, amount=tot_amnt, address=address)
        orders.delete()
        return JsonResponse({'status': "Thank you for purchasing...pls Check My Orders for updates."})

@never_cache
def paypal(request):
    if request.method == 'GET':
        address_id = request.GET['address_id']
        coupon_id = request.GET['coupon_id']
        orderid = request.GET['orderid']
        orders = Cart.objects.filter(user=request.user)
        address = Address.objects.get(id=address_id)
        if len(coupon_id) == 0:
            coupon = ""
        else:
            coupon = Coupon.objects.get(id=coupon_id)
        if coupon == "":
            for single_order in orders:
                p = Product.objects.get(id=single_order.product.id)
                p.product_qty = p.product_qty - single_order.quantity
                p.save()
                HistoryOrder.objects.create(coupon_code=coupon, user=request.user, is_ordered=True,
                                            method="razorpay", product=single_order.product, quantity=single_order.quantity, amount=single_order.get_final_price(), address=address)
        else:
            dis_amnt = coupon.discount_amnt / orders.count()
            for single_order in orders:
                p = Product.objects.get(id=single_order.product.id)
                tot_amnt = single_order.get_final_price() - dis_amnt
                p.product_qty = p.product_qty - single_order.quantity
                p.save()
                HistoryOrder.objects.create(coupon_code=coupon.code, user=request.user, is_ordered=True,
                                            method="razorpay", product=single_order.product, quantity=single_order.quantity, amount=tot_amnt, address=address)
        orders.delete()
        return JsonResponse({'status': "Thank you for purchasing...pls Check My Orders for updates."})


@never_cache
def user_orders(request):
    if request.user.is_authenticated:
        orders = HistoryOrder.objects.filter(user=request.user).order_by('-id')
        return render(request, 'user_orders.html', {'orders': orders})
    return redirect(index)

@never_cache
def order_cancel(request, id):
    order = HistoryOrder.objects.get(id=id)
    order.status = "Cancel"
    order.amount = 0
    p = Product.objects.get(id=order.product_id)
    p.product_qty = p.product_qty + order.quantity
    p.save()
    order.save()
    return redirect(user_orders)

@never_cache
def order_return(request, id):
    order = HistoryOrder.objects.filter(id=id).update(status="Return")
    return redirect(user_orders)
@never_cache
def orderinvoice(request, id):
    order = HistoryOrder.objects.get(id=id)
    return render(request, 'orderinvoice.html', {'order': order})
