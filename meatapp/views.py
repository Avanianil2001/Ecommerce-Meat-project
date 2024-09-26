from django.shortcuts import render,redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponse,JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import *
from .forms import *
from django.contrib import messages
import datetime
import random
import re
# import razorpay

# Create your views here.

def index(re):
    return render(re, 'index.html')

def home(re):
    return render(re, 'index.html')

def about(re):
    return render(re, 'about.html')

def usr_abt(re):
    return render(re, 'user_about.html')

def contact_feedback(re):
    feedback = Feedback.objects.all()
    return render(re, 'contact.html', {'data': feedback})


# ---------------------------- REGISTRATIONS  ---------------------------

def rgstr(request):
    if request.method=='POST':
        uname = request.POST.get('name', '')
        email = request.POST.get('email', '')
        uphno = request.POST.get('nmbr', '')
        img = request.FILES.get('user_img', None)
        addrs = request.POST.get('adrss','')
        dist = request.POST.get('udistrict')
        city = request.POST.get('ucity','')
        pncd = request.POST.get('upincode','')
        usname = request.POST.get('usname', '')
        pwd = request.POST.get('password', '')
        try:
            u = u_register.objects.get(username=usname)
            if u is not None:
                messages.error(request,'...Username Already Exist...')
                return redirect(request,rgstr)
        except Exception:
            u = u_register.objects.create(u_name=uname,email=email,u_phno=uphno,u_img=img,u_address=addrs,u_district=dist,u_city=city,u_pincode=pncd,username=usname,password=pwd)
            u.save()
            messages.success(request,'...Profile Details added Successfully...')
    return render(request, 'register.html')

def delboy_reg(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        demail = request.POST['d_email']
        dadrs = request.POST['d_adrs']
        dphno = request.POST['d_nmbr']
        dimg = request.FILES['d_photo']
        dlcnc = request.FILES['d_licence']
        dbio = request.FILES['d_bio']
        dusname = request.POST['d_usname']
        dpwd = request.POST['d_password']
        try:
            d = d_register.objects.get(d_username=dusname)
            if d is not None:
                messages.error(request,'...Username Already Exist...')
        except Exception:
            d = d_register.objects.create(df_name=fname,dl_name=lname,d_email=demail,d_adrs=dadrs,d_phno=dphno,d_img=dimg,d_lcnc=dlcnc,d_bio=dbio,d_username=dusname,d_password=dpwd)
            d.save()
            messages.success(request,'...Profile Details added Successfully...')
    return render(request, 'delboy_reg.html')



# ---------------------------- LOGIN/LOGOUT  ---------------------------

def login(re):
    if re.method=='POST':
        username=re.POST['username']
        password=re.POST['password']
        try:
            data=u_register.objects.get(username=username)
            if username == data.username and password == data.password:
                re.session['uid'] = username
                return redirect(usr_home)
            else:
                messages.error(re,'...Invalid Username or Password...')
        except Exception:
            if username == 'admin' and password == 'admin':
                re.session['aid'] = username
                return redirect(admn_home)
            else:
                messages.error(re,'...Invalid Username or Password...')
    return render(re, 'login.html')

def login_del(re):
    if re.method=='POST':
        username = re.POST['username']
        password = re.POST['password']
        try:
            data = d_register.objects.get(d_username=username)
            if username == data.d_username and password == data.d_password:
                re.session['did'] = username
                return redirect(delboy_home)
            else:
                messages.error(re, '...Invalid Username or Password...')
        except Exception:
            if username == 'admin' and password == 'admin':
                re.session['aid'] = username
                return redirect(admn_home)
            else:
                messages.error(re, '...Invalid Username or Password...')
    return render(re,'login_delivery.html')

def logout(re):
    if 'uid' in re.session and 'aid' in re.session and 'did' in re.session:
        re.session.flush()
        return redirect(home)

# ---------------------------- ADMIN HOME  ---------------------------

def admn_home(re):
    return render(re, 'admin_home.html')


# ---------------------------- ADMIN-ADD ITEMS ---------------------------

# chicken
def add_prod(request):
    if 'aid' in request.session:
        if request.method=='POST':
            pid = request.POST['pid']
            pname = request.POST['pname']
            description = request.POST['shrtdes']
            quantity = request.POST['quant']
            price = request.POST['price']
            pimg = request.FILES['pimg']
            product = add_product(pro_id=pid,pro_name=pname,description=description,quantity=quantity,price=price,pro_img=pimg)
            product.save()
            messages.success(request,'...Product added Successfully...')
            return redirect(add_prod)
        return render(request, 'add_product.html')
    return redirect(admn_home)

# def add_emply(request):
#     if 'aid' in request.session:
#         if request.method=='POST':
#             eid = request.POST['eid']
#             ename = request.POST['e_name']
#             dob = request.POST['dob']
#             eadrs = request.POST['e_adrs']
#             ephno = request.POST['e_phno']
#             eimg = request.FILES['e_img']
#             e = add_employee(emp_id=eid,emp_name=ename,emp_dob=dob,emp_adrs=eadrs,emp_phno=ephno,emp_img=eimg)
#             e.save()
#             messages.success(request,'...Employee Profile details added Successfully...')
#             return redirect(add_emply)
#         return render(request,'add_employee.html')
#     return redirect(admn_home)

# def add_ofr(request):
    # if 'aid' in request.session:
    #     if request.method=='POST':
    #         oid = request.POST['o_id']
    #         odt = request.POST['o_date']
    #         oimg = request.FILES['o_img']
    #         oexp = request.POST['o_exp']
    #         o = add_offer(ofr_id=oid,ofr_date=odt,ofr_img=oimg,ofr_exp=oexp)
    #         o.save()
    #         messages.success(request,'...Offer added Successfully...')
    #         return redirect(add_ofr)
    #     return render(request, 'add_ofr.html')
    # return redirect(admn_home)


# ---------------------------- ADMIN-VIEW ITEMS ---------------------------
def view_prdct(re):
    if 'aid' in re.session:
        data = add_product.objects.all()
        return render(re, 'view_product.html',{'d':data})
    return redirect(admn_home)

# def view_emply(re):
#     if 'aid' in re.session:
#         data = add_employee.objects.all()
#         return render(re,'view_employee.html',{'d':data})
#     return redirect(admn_home)

# def view_ofr(re):
#     if 'aid' in re.session:
#         data = add_offer.objects.all()
#         return render(re, 'view_offer.html',{'d':data})
#     return redirect(admn_home)

def view_del(re):
    if 'aid' in re.session:
        data = d_register.objects.all()
        return render(re,'view_delivery.html',{'d':data})
    return redirect(admn_home)

def view_user(re):
    if 'aid' in re.session:
        data = u_register.objects.all()
        return render(re,'view_user.html',{'d':data})
    return redirect(admn_home)

def view_feedback(re):
    if 'aid' in re.session:
        data = Feedback.objects.all()
        return render(re,'view_feedback.html',{'d':data})
    return redirect(admn_home)

# def view_orders(re):
#     if 'aid' in re.session:
#         data = Order.objects.all()
#         return render(re,'view_order.html',{'order' : data})
#     return redirect(admn_home)
def view_orders(request):
    if 'aid' in request.session:
        orders = Order.objects.select_related('delivery_person').all()
        return render(request, 'view_order.html', {'order': orders})
    return redirect('admn_home')

# ---------------------------- ADMIN-UPDATE  ---------------------------
# -------------- Update Order-Status --------------
def admin_statusup(re,sts):
    if re.method == "POST":
        st = Order.objects.get(id=sts)
        st.status = re.POST.get('status')
        st.save()
        return redirect(view_orders)

# -------------- Update Product --------------
def update(re,id):
    if 'aid' in re.session:
        data = add_product.objects.get(pk=id)
        return render(re,'up_product.html',{'d':data})

def updating(re,id):
    if 'aid' in re.session:
        nm = re.POST['upname']
        dtn = re.POST['updescription']
        qty = re.POST['upquan']
        pce = re.POST['upprice']
        add_product.objects.filter(pk=id).update(pro_name=nm,description=dtn,quantity=qty,price=pce)
        return redirect(updis)
    return render(re,'up_product.html')

def updis(re):
    updata = add_product.objects.all()
    messages.success(re,'...Product Updated Successfully...')
    return render(re,'up_display.html',{'udp':updata})

def delete(re,id):
    if 'aid' in re.session:
        data = add_product.objects.get(pk=id)
        data.delete()
        messages.success(re,'...Product Deleted...')
        return redirect(view_prdct)

# -------------- Delete Employee  --------------

# def delete_emp(re,id):
#     if 'aid' in re.session:
#         data = add_employee.objects.get(pk=id)
#         data.delete()
#         messages.success(re,'...Employee details Deleted...')
#         return redirect(view_emply)

# -------------- Accept/Reject Delivery-person  --------------
# def accept_delivery_person(request, id):
#     if 'aid' in request.session:  # Check if the session ID matches the admin session
#         delivery_person = get_object_or_404(d_register, id=id)
#         delivery_person.accepted = True  # Assuming you have an 'accepted' field in the model
#         delivery_person.save()
#         messages.success(request, 'Delivery person accepted successfully!')
#         return redirect(view_del)
#     else:
#         return redirect(login)
#
# def reject_delivery_person(request, id):
#     if 'aid' in request.session:  # Check if the session ID matches the admin session
#         delivery_person = get_object_or_404(d_register, id=id)
#         delivery_person.accepted = False  # Assuming you have an 'accepted' field in the model
#         delivery_person.save()
#         messages.success(request, 'Delivery person rejected successfully!')
#         return redirect(view_del)
#     else:
#         return redirect(login)

# def delete_dely(re,id):
#     if 'aid' in re.session:
#         data = d_register.objects.get(pk=id)
#         data.delete()
#         messages.success(re,'...Delivery Person Deleted...')
#         return redirect(view_del)

# -------------- Delete Offer --------------
# def delete_offer(re,id):
#     if 'aid' in re.session:
#         data = add_offer.objects.get(pk=id)
#         data.delete()
#         messages.success(re,'...Offer Deleted Successfully...')
#         return redirect(view_ofr)

# -------------- Delete Feedback --------------
def delete_feedback(re,id):
    if 'aid' in re.session:
        data = Feedback.objects.get(pk=id)
        data.delete()
        messages.success(re,'...Feedback Deleted...')
        return redirect(view_feedback)

# ---------------------------- ORDER DISTRIBUTION ---------------------------
def distri(request, order_id):
    if 'aid' in request.session:  # Ensure admin is logged in
        order = get_object_or_404(Order, id=order_id)
        available_delivery_persons = d_register.objects.filter(d_status='available')

        if request.method == "POST":
            delivery_person_id = request.POST.get('delivery_person_id')

            if delivery_person_id:
                delivery_person = get_object_or_404(d_register, id=delivery_person_id)

                # Assign the delivery person to the order
                order.delivery_person = delivery_person
                order.status = 'Out For Shipping'
                delivery_person.d_status = 'in-duty'

                order.save()
                delivery_person.save()

                return redirect(view_orders)  # Assuming you have a 'view_orders' URL

        context = {
            'order': order,
            'delivery_persons': available_delivery_persons
        }
        return render(request, 'order_distribution.html', context)

    return redirect(admn_home)

# ---------------------------- USER HOME  ---------------------------

def usr_home(re):
    return render(re, 'user_home.html')


# ---------------------------- USER VIEWS ---------------------------


def usr_category(re):
    if 'uid' in re.session:
        data = add_product.objects.all()
        user = u_register.objects.get(username=re.session['uid'])
        wish = Wishlist.objects.filter(user_details=user)
        wish_its = [item.item_details.id for item in wish]
        return render(re, 'user_category.html', {'d1': data, 'wish_its': wish_its})
    return redirect(re, login)

def usr_category_view(re, id):
    if 'uid' in re.session:
        product = add_product.objects.get(pk=id)
        user = u_register.objects.get(username=re.session['uid'])
        cart_item_exists = Cart.objects.filter(user_details=user, product_details=product).exists()
        return render(re, 'usr_category_view.html', {'d1': product, 'cart_item_exists': cart_item_exists})
    return redirect(re, login)


def user_feedback(re):
    if 'uid' in re.session:
        if re.method=='POST':
            name = re.POST['fb_name']
            fmail = re.POST['fb_email']
            phone = re.POST['fb_phno']
            msg = re.POST['message']
            feedback = Feedback.objects.create(name=name,email=fmail,phone=phone,message=msg)
            feedback.save()
            messages.success(re,'...Feedbcak Submitted Successfully...','THANK YOU FOR YOUR FEEDBACK')
        return render(re, 'user_feedback.html')
    return redirect(login)

def my_ordrs(re):
    if 'uid' in re.session:
        user = u_register.objects.get(username=re.session['uid'])
        order = Order.objects.filter(customer=user)
        return render(re, 'user_my_orders.html', {'data': order})
    return redirect(login)


# ---------------------------- INDEX VIEWS ---------------------------

def category(re):
    data = add_product.objects.all()
    return render(re, 'category.html',{'d1':data})

def category_view(re, id):
    data = add_product.objects.get(pk=id)
    return render(re, 'home_category_view.html',{'d1':data})

# def home_offer(re):
#     data = add_offer.objects.all()
#     return render(re, 'offers.html',{'d':data})


# ---------------------------- CART ---------------------------
def cart1(request):
    if 'uid' in request.session:
        user = get_object_or_404(u_register, username=request.session['uid'])
        datas = Cart.objects.filter(user_details=user)
        return render(request, 'cart.html', {'d1': datas})
    return redirect(usr_home)

def display_product(request):
    if 'uid' in request.session:
        user = get_object_or_404(u_register, username=request.session['uid'])
        cart_items = Cart.objects.filter(user_details=user)
        total = sum(item.product_details.price * item.quantity for item in cart_items)
        return render(request, 'display-product.html', {'data': cart_items, 'total': total})
    return redirect(usr_home)

def addcart(request, id):
    if 'uid' in request.session:
        user = get_object_or_404(u_register, username=request.session['uid'])
        product = get_object_or_404(add_product, pk=id)
        cart_item, created = Cart.objects.get_or_create(
            product_details=product,
            user_details=user,
            defaults={'quantity': 1, 'total_price': product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.quantity * product.price
            cart_item.save()
        messages.success(request, 'Cart added successfully')
        return redirect(usr_category)
    return redirect(usr_home)

def decrement_quantity(request, cart_id):
    if 'uid' in request.session:
        cart_item = get_object_or_404(Cart, id=cart_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.total_price = cart_item.quantity * cart_item.product_details.price
            cart_item.save()
        else:
            cart_item.delete()
    return redirect(display_product)

def increment_quantity(request, cart_id):
    if 'uid' in request.session:
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.product_details.price
        cart_item.save()
    return redirect(display_product)

def remove_cart(request, id):
    if 'uid' in request.session:
        cart_item = get_object_or_404(Cart, pk=id)
        cart_item.delete()
        messages.success(request, 'Item removed successfully')
    return redirect(display_product)

# ---------------------------- WISHLIST ---------------------------

def wish(re):
    return render(re,'wishlist.html')

# def addwish(re,id):
#     if 'uid' in re.session:
#         u = u_register.objects.get(username=re.session['uid'])
#         print(u)
#         item = add_product.objects.get(pk=id)
#         print(item)
#         data = Wishlist.objects.create(item_details=item,user_details=u)
#         data.save()
#         messages.success(re,'...Product added to Wishlist...')
#     return redirect(usr_category)

def addwish(re, id):
    if 'uid' in re.session:
        u = u_register.objects.get(username=re.session['uid'])
        item = add_product.objects.get(pk=id)
        existing_wish = Wishlist.objects.filter(item_details=item, user_details=u)
        if existing_wish.exists():
            messages.info(re, '...Product already in Wishlist...')
        else:
            data = Wishlist.objects.create(item_details=item, user_details=u)
            data.save()
            messages.success(re, '...Product added to Wishlist...')
    return redirect(usr_category)


def display_wishlist(re):
    if 'uid' in re.session:
        details = u_register.objects.get(username=re.session['uid'])
        usr = u_register.objects.get(username=details.username)
        w = Wishlist.objects.all()
        cart_items = Cart.objects.filter(user_details=usr)
        l = []
        cart_product_ids = cart_items.values_list('product_details_id', flat=True)

        for i in w:
            if i.user_details == usr:
                l.append({
                    'wishlist_item': i,
                    'in_cart': i.item_details.pk in cart_product_ids
                })

        return render(re, 'wishlist.html', {'l': l})
    return redirect(login)


def delete_wish(re,id):
    if 'uid' in re.session:
        data = Wishlist.objects.get(pk=id)
        data.delete()
        messages.success(re,'...Item Removed...')
        return redirect(display_wishlist)


# ---------------------------- USER PROFILE ---------------------------

def usr_profile(re):
    if 'uid' in re.session:
        u = u_register.objects.get(username=re.session['uid'])
        return render(re,'my_profile.html',{'user':u})

def pro_edit(re,id):
    if 'uid' in re.session:
        u = u_register.objects.get(pk=id)
        if re.method == 'POST':
            u.u_name = re.POST['name']
            u.email = re.POST['email']
            u.u_phno = re.POST['nmbr']
            u.u_address = re.POST['adrss']
            u.u_district = re.POST['udistrict']
            u.u_city = re.POST['ucity']
            u.u_pincode  = re.POST['upincode']
            try:
                u.u_img = re.FILES['user_img']
                import os
                os.remove()
                u.save()
            except:
                u.save()
                return redirect(update_profile,id)
        return render(re,'user_profile_update.html',{'d':u})


def update_profile(re,id):
    if 'uid' in re.session:
        if re.method == 'POST':
            form=UserProfileForm(re.POST,re.FILES)
            if form.is_valid():
                a = form.cleaned_data['name']
                b = form.cleaned_data['email']
                c = form.cleaned_data['nmbr']
                d = form.cleaned_data['adrss']
                e = form.cleaned_data['udistrict']
                f = form.cleaned_data['ucity']
                g = form.cleaned_data['user_img']
                h= form.cleaned_data['upincode ']
                u_register.objects.filter(pk=id).update(u_name=a,email=b,u_phno=c,u_address=d,u_district=e,u_city=f,u_img=g,u_pincode=h)
                messages.success(re,'...Profile Updated Successfully...')
                return redirect(usr_profile)
            data = u_register.objects.all()
            return render(re,'user_profile_update.html',{'d':data})
            form=UserProfileForm()
            return render(re,'user_profile_update.html',{'form':form})
        return redirect(usr_profile)


# ---------------------------- SINGLE BOOKING ---------------------------
def singles(request, d):
    if 'uid' in request.session:
        user = u_register.objects.get(username=request.session['uid'])
        product = add_product.objects.get(pk=d)
        return render(request, 'single_booking.html', {'data': user, 'pdata': product})
    return redirect(login)

def single_booking(request, product_id):
    if 'uid' in request.session:
        product = get_object_or_404(add_product, pk=product_id)
        user = get_object_or_404(u_register, username=request.session['uid'])
        crt = Cart.objects.filter(user_details=user).first()

        if request.method == "POST":
            so_fname = request.POST.get('sofname', '')
            so_lname = request.POST.get('solname', '')
            so_email = request.POST.get('semail', '')
            so_phone = int(request.POST.get('sphone', 10))
            so_address = request.POST.get('sadrs', '')
            so_district = request.POST.get('sdistrict', '')
            so_city = request.POST.get('scity', '')
            so_pincode = int(request.POST.get('spincode', 6))
            add_message = request.POST.get('add_det', '')
            quantity = int(request.POST.get('singleqty', 1))
            # total_price = float(request.POST.get('total', 0))
            total_price=product.price
            paymode = request.POST.get('payment_mode', '')

            order_id = 'ordid' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(order_id=order_id).exists():
                order_id = 'ordid' + str(random.randint(1111111, 9999999))

            tracking_no = 'meat' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=tracking_no).exists():
                tracking_no = 'meat' + str(random.randint(1111111, 9999999))

            single_booking = Order.objects.create(
                customer=user,
                product=product,
                so_fname=so_fname,
                so_lname=so_lname,
                so_email=so_email,
                so_phone=so_phone,
                so_address=so_address,
                so_district=so_district,
                so_city=so_city,
                so_pincode=so_pincode,
                add_message=add_message,
                quantity=quantity,
                status='Pending',
                payment_mode=paymode,
                payment_id=None,
                order_id=order_id,
                tracking_no=tracking_no,
                total_price=total_price,
            )
            single_booking.save()
            messages.success(request, 'Your order has been placed successfully')
            return redirect(usr_home)
    return render(request,'single_booking')


# razorpay

def single_razor(request, product_id):
    if 'uid' in request.session:
        product = get_object_or_404(add_product, pk=product_id)
        user = get_object_or_404(u_register, username=request.session['uid'])
        crt = Cart.objects.filter(user_details=user).first()

        if request.method == "POST":
            print("hello")
            so_fname = request.POST.get('sofname', '')
            so_lname = request.POST.get('solname', '')
            so_email = request.POST.get('semail', '')
            so_phone = int(request.POST.get('sphone', 10))
            so_address = request.POST.get('sadrs', '')
            so_district = request.POST.get('sdistrict', '')
            so_city = request.POST.get('scity', '')
            so_pincode = int(request.POST.get('spincode', 6))
            add_message = request.POST.get('notes', '')
            quantity = int(request.POST.get('singleqty', 1))
            # total_price = float(request.POST.get('total', 0))
            paymode = request.POST.get('payment_mode', '')
            # print(paymode,total_price)
            total_price = product.price

            order_id = 'ordid' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(order_id=order_id).exists():
                order_id = 'ordid' + str(random.randint(1111111, 9999999))

            tracking_no = 'meat' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=tracking_no).exists():
                tracking_no = 'meat' + str(random.randint(1111111, 9999999))

            single_booking = Order.objects.create(
                customer=user,
                product=product,
                so_fname=so_fname,
                so_lname=so_lname,
                so_email=so_email,
                so_phone=so_phone,
                so_address=so_address,
                so_district=so_district,
                so_city=so_city,
                so_pincode=so_pincode,
                add_message=add_message,
                quantity=quantity,
                status='Pending',
                payment_mode=paymode,
                payment_id=None,
                order_id=order_id,
                tracking_no=tracking_no,
                total_price=total_price,
            )
            single_booking.save()
        # if paymode == 'RazorPay':
        return redirect(razorpaycheck,product.price)
    #     return JsonResponse({'status': 'Your order has been placed successfully'})
    #
    # return redirect(usr_home)


# ---------------------------- RAZOR PAY ---------------------------

def razorpaycheck(request,price):
    if 'uid' in request.session:
        u = u_register.objects.get(username=request.session['uid'])
        s = Order.objects.filter(customer=u)
        t = price*100
        return render(request, "payment.html", {'amount': t})

    return render(request, "payment.html")


def success(re):
    return redirect(my_ordrs)
# ---------------------------- MULTIPLE BOOKING  ---------------------------
def checkout(request):
    # c = d
    mp = []
    t = 0
    if 'uid' in request.session:
        user = u_register.objects.get(username=request.session['uid'])
        mp = Cart.objects.filter(user_details=user)
        c = mp
        t = 0
        print(mp)
        for i in c:
            t = t + (i.product_details.price * i.quantity)
        return render(request, 'multiple_booking.html', {'data': user, 'pdata':mp,'t':t})
    return redirect(usr_home)

def multiple_booking(request):
    if 'uid' not in request.session:
        return redirect('usr_home')

    user = get_object_or_404(u_register, username=request.session['uid'])
    crt = Cart.objects.filter(user_details=user)
    # crt = mycart.object.filter(usr=user).delete()
    t=0
    for i in crt:
        t = t + (i.product_details.price * i.quantity)
        total = t
        quty=i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(usr_home)
    if request.method == "POST":
        m_fname = request.POST.get('sofname', '')
        m_lname = request.POST.get('solname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_city = request.POST.get('scity', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('add_det', '')
        m_quantity = int(request.POST.get('multyqty', 1))
        m_quantity =quty
        total_price = int(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        total_price =total
        product_id =crt_i. product_details.pk
        product = get_object_or_404(add_product, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        for i in crt:
            multiple_booking =Order.objects.create(
                customer=user,
                product=i.product_details ,
                cart=crt_i ,
                so_fname=m_fname,
                so_lname=m_lname,
                so_email=m_email,
                so_phone=m_phone,
                so_address=m_address,
                so_district=m_district,
                so_city=m_city,
                so_pincode=m_pincode,
                add_message=m_add_message,
                quantity=m_quantity,
                status='Pending',
                payment_mode=paymode,
                payment_id=None,
                order_id=order_id,
                tracking_no=tracking_no,
                total_price=total_price,
            )
        multiple_booking.save()
        # crt.delete()
        messages.success(request, 'Your order has been placed successfully')
        return redirect(usr_home)

    return redirect(checkout)


def multiple_razor(request):
    if 'uid' not in request.session:
        return redirect(usr_home)

    user = get_object_or_404(u_register, username=request.session['uid'])
    crt = Cart.objects.filter(user_details=user)
    t=0
    for i in crt:
        t = t + (i.product_details.price * i.quantity)
        total = t
        quty = i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(usr_home)


    if request.method == "POST":
        print("hello")
        m_fname = request.POST.get('sofname', '')
        m_lname = request.POST.get('solname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_city = request.POST.get('scity', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('notes', '')
        m_quantity = int(request.POST.get('singleqty', 1))
        m_quantity=quty
        # total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        # print(paymode,total_price)
        total_price =total
        product_id = crt_i.product_details.pk
        product = get_object_or_404(add_product, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        for i in crt:
            multiple_booking = Order.objects.create(
                customer=user,
                product=i.product_details,
                cart=crt_i ,
                so_fname=m_fname,
                so_lname=m_lname,
                so_email=m_email,
                so_phone=m_phone,
                so_address=m_address,
                so_district=m_district,
                so_city=m_city,
                so_pincode=m_pincode,
                add_message=m_add_message,
                quantity=m_quantity,
                status='Pending',
                payment_mode=paymode,
                payment_id=None,
                order_id=order_id,
                tracking_no=tracking_no,
                total_price=total_price,
            )
        multiple_booking.save()
        # if paymode == 'RazorPay':
        messages.success(request, 'Your order has been placed successfully')

        return redirect(razorpaycheck2)
        # return redirect(razorpaycheck2
    return redirect(checkout)

def razorpaycheck2(request):
    if 'uid' in request.session:
        u = u_register.objects.get(username=request.session['uid'])
        s = Order.objects.filter(customer=u)
        mp = Cart.objects.filter(user_details=u)
        c = mp
        t = 0
        print(mp)
        for i in c:
            t = t + (i.product_details.price * i.quantity)
            total = t * 100
        return render(request, "payment2.html", {'amount': total})

    return render(request, "payment2.html")

def success2(re):
    return redirect(my_ordrs)

# ---------------------------- CANSEL-BOOKING ---------------------------
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
     # Check if the order is Cash on Delivery
    if order.payment_mode == 'COD':
        # If the user confirms, proceed with cancellation
        if request.method == 'POST':
            if order.status != 'Cancelled':
                order.status = 'Cancelled'
                order.save()
                messages.success(request, 'Order has been successfully cancelled.')
            else:
                messages.info(request, 'Order is already cancelled.')
            return redirect(my_ordrs)
        else:
            # Render a confirmation page with a message
            return render(request, 'confirm_cancel.html', {'order': order})
    else:
        messages.error(request, 'Order cancellation is only available for Cash on Delivery orders.')
        return redirect(my_ordrs)

# ---------------------------- DELBOY HOME ---------------------------

def delboy_home(re):
    return render(re, 'delboy_home.html')

def del_view_orders(request):
    if 'did' in request.session:
        delivery_person = d_register.objects.get(d_username=request.session['did'])
        if request.method == 'POST':
            status = request.POST.get('d_status')
            delivery_person.d_status = status
            delivery_person.save()
            return redirect(del_view_orders)

        orders = Order.objects.filter(delivery_person=delivery_person)
        return render(request, 'del_view_order.html', {'order': orders, 'delivery_person': delivery_person})
    return redirect(login_del)

# -------------- Update Order --------------

def statusup(re,sts):
    if re.method == "POST":
        st = Order.objects.get(id=sts)
        st.status = re.POST.get('status')
        st.save()
        return redirect(del_view_orders)

# ---------------------------- DELBOY PROFILE ---------------------------

def dlby_profile(re):
    if 'did' in re.session:
        u = d_register.objects.get(d_username=re.session['did'])
        return render(re,'delboy_profile.html',{'user':u})

def dlby_pro_edit(re,id):
    if 'did' in re.session:
        d = d_register.objects.get(pk=id)
        if re.method == 'POST':
            d.df_name = re.POST['dfname']
            d.dl_name = re.POST['dlname']
            d.d_email = re.POST['demail']
            d.d_phno = re.POST['dnmbr']
            d.d_adrs = re.POST['dadrss']
            try:
                d.d_img = re.FILES['dimg']
                d.d_lcnc = re.FILES['dlcnc']
                d.d_bio = re.FILES['dbio']
                import os
                os.remove()
                d.save()
            except:
                d.save()
                return redirect(update_delprofile,id)
        return render(re,'delboy_profile_update.html',{'d':d})


def update_delprofile(re,id):
    if 'did' in re.session:
        if re.method == 'POST':
            form=DelboyProfileForm(re.POST,re.FILES)
            if form.is_valid():
                a = form.cleaned_data['dfname']
                b = form.cleaned_data['dlname']
                c = form.cleaned_data['demail']
                d = form.cleaned_data['dnmbr']
                e = form.cleaned_data['dadrss']
                f = form.cleaned_data['dlcnc']
                g = form.cleaned_data['udbio']
                h = form.cleaned_data['dimg']
                d_register.objects.filter(pk=id).update(df_name=a,dl_name=b,d_email=c,d_phno=d,d_adrs=e,d_lcnc=f,d_bio=g,d_img=h)
                messages.success(re,'...Profile Updated Successfully...')
                return redirect(dlby_profile)
            data = d_register.objects.all()
            return render(re,'delboy_profile_update.html',{'d':data})
            form=DelboyProfileForm()
            return render(re,'delboy_profile_update.html',{'form':form})
        return redirect(dlby_profile)


# ---------------------------- FORGOT/RESET PASSWORD -USER  ---------------------------

def forgot_password_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = u_register.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password_user)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            messages.success(request, "Password reset email sent successfully.")
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password_user)

    return render(request, 'frgt.html')

def reset_password_user(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            messages.success(request, "Password has been reset successfully.")
            return redirect(login)
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'rest-pass.html',{'token':token})


# ---------------------------- FORGOT/RESET PASSWORD - DELBOY  ---------------------------

def forgot_password_delivery_person(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            delivery_person = d_register.objects.get(d_email=email)
        except d_register.DoesNotExist:
            messages.info(request, "Email ID not registered")
            return redirect(forgot_password_delivery_person)

        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordResets.objects.create(delivery_person=delivery_person, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/d_reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            messages.success(request, "Password reset email sent successfully.")
        except:
            messages.info(request, "Network connection failed")
            return redirect(forgot_password_delivery_person)

    return render(request, 'frgt_delivery.html')


def reset_password_delivery_person(request, token):
    try:
        password_reset = PasswordResets.objects.get(token=token)
    except PasswordResets.DoesNotExist:
        messages.error(request, "Invalid reset token.")
        return redirect(forgot_password_delivery_person)

    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if new_password == repeat_password:
            password_reset.delivery_person.d_password = new_password
            password_reset.delivery_person.save()
            password_reset.delete()
            messages.success(request, "Password has been reset successfully.")
            return redirect(login_del)
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'reset_delivery_pass.html', {'token': token})