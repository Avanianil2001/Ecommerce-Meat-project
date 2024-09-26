"""
URL configuration for meatproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meatapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

# --------------- INDEX ---------------
    path("",views.index),
    path('home',views.home),
    path('about',views.about),
    # path('offers',views.home_offer),
    path('contact',views.contact_feedback),
    path('user_my_orders',views.my_ordrs),

# --------------- REGISTER -----------------
    path('register', views.rgstr),
    path('delboy_reg', views.delboy_reg),

# --------------- LOGIN/LOGOUT -----------------
    path('login',views.login),
    path('login_delivery',views.login_del),
    path('logout',views.logout),

# --------------- USER HOME -----------------
    path('user_home',views.usr_home),
    path('user_about', views.usr_abt),
    path('user_feedback', views.user_feedback),
    # path('user_offer', views.user_ofr),

# --------------- ADMIN HOME -----------------
    path('admin_home', views.admn_home),

# --------------- ADMIN ADD/VIEW OTHERS -----------------
    path('add_product', views.add_prod),
    path('view_product', views.view_prdct),
    path('ordr_distri/<int:order_id>/', views.distri, name='ordr_distri'),
    path('view_delivery', views.view_del),
    path('view_user', views.view_user),
    path('view_feedback', views.view_feedback),
    path('view_order', views.view_orders),
    # path('add_employee',views.add_emply),
    # path('view_employee',views.view_emply),
    # path('add_offer',views.add_ofr),
    # path('view_offer',views.view_ofr),

# --------------- UPDATE PRODUCT -----------------
    path('update_product/<int:id>',views.update),
    path('updp/<int:id>',views.updating),
    path('updis',views.updis),
    path('delete_product/<int:id>',views.delete),

# --------------- UPDATE EMPLOYEE -----------------
#     path('update_employee/<int:id>',views.update_emp),
#     path('upde/<int:id>',views.emp_updating),
#     path('updis_emp',views.updis_emp),
#     path('delete_employee/<int:id>',views.delete_emp),

# --------------- DELETE/ACCEPT,REJECTED -----------------
    #path('accept_delivery/<int:id>/', views.accept_delivery_person, name='accept_delivery_person'),
    #path('reject_delivery/<int:id>/', views.reject_delivery_person, name='reject_delivery_person'),
    # path('delete_offer/<int:id>',views.delete_offer),
    # path('delete_feedback/<int:id>',views.delete_feedback),


# --------------- DELBOY HOME -----------------
    path('delboy_home',views.delboy_home),
    path('del_order_view', views.del_view_orders),

# --------------- DELBOY-PROFILE -----------------
    path('del_profile',views.dlby_profile),
    path('delboy_profile_update/<int:id>', views.dlby_pro_edit, name='delboy_profile_update'),
    path('delboy_profile_update/<int:id>',views.update_delprofile),


# --------------- CATEGORY -----------------
    path('user_category', views.usr_category),
    path('view_det/<int:id>',views.usr_category_view),

    path('category', views.category),
    path('hom_view/<int:id>',views.category_view),

# --------------- CART -----------------
    path('cart/',views.display_product),
    path('addcart/<int:id>', views.addcart),
    path('increment/<int:cart_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement/<int:cart_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('deletecart/<int:id>', views.remove_cart),

# --------------- WISHLIST -----------------
    path('wishlist/',views.display_wishlist),
    path('addwish/<int:id>',views.addwish),
    path('delete_wish/<int:id>',views.delete_wish),

# --------------- USER-PROFILE -----------------
    path('my_profile',views.usr_profile),
    path('user_profile_update/<int:id>', views.pro_edit, name='user_profile_update'),
    path('user_profile_update/<int:id>',views.update_profile),

# --------------- SINGLE BOOKING -----------------
    path('singles/<int:d>/', views.singles, name='single'),
    path('single_booking/<int:product_id>', views.single_booking, name='single_booking'),
    path('single_razor/<int:product_id>', views.single_razor, name='single_razor'),
    path('razor_pay/<int:price>', views.razorpaycheck),
    path('success', views.success, name='success'),

# --------------- MULTIPLE BOOKING -----------------
    path('checkout', views.checkout, name='checkout'),
    path('multiple_booking', views.multiple_booking, name='multiple_booking'),
    path('multiple_razor', views.multiple_razor, name='multiple_razor'),
    path('razor_pay2', views.razorpaycheck2),
    path('successs',views.success2),

# --------------- BOOKING-STATUS UPDATE -----------------
    # ----------- Admin -----------
    path('admin_statusup/<sts>',views.admin_statusup, name="admin_statusup"),
    # ----------- delboy -----------
    path('statusup/<sts>',views.statusup, name="statusup"),

# --------------- FORGOT/RESET PASSWORD -----------------
    path('forgot', views.forgot_password_user, name="forgot"),
    path('reset/<token>', views.reset_password_user, name='reset_password'),
    path('d_forgot_password/', views.forgot_password_delivery_person, name='forgot_password_delivery_person'),
    path('d_reset/<str:token>/', views.reset_password_delivery_person, name='reset_password_delivery_person'),

# --------------- RAZOR PAY -----------------
    # path('multiple_razor/<int:id>',views.multiple_razor, name='multiple_razor'),
    # path('razor_pay2/<int:price>',views.razorpaycheck2),

# --------------- CANSEL BOOKING -----------------
    path('cancel/<int:order_id>/',views.cancel_order, name='cancel_order'),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)