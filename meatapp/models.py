from datetime import datetime

from django.db import models

# Create your models here.

# -------------------------------- REGISTERS -------------------------------

class u_register(models.Model):
    u_name = models.CharField(max_length=20)
    email = models. EmailField()
    u_phno = models.IntegerField()
    u_img = models.FileField()
    username = models.CharField(max_length=10,unique=True)
    password = models.CharField(max_length=10)
    u_address = models.CharField(max_length=100)
    u_district = models.CharField(max_length=20)
    u_city = models.CharField(max_length=20)
    u_pincode = models.IntegerField()

class d_register(models.Model):
    df_name = models.CharField(max_length=10)
    dl_name = models.CharField(max_length=15)
    d_email = models.EmailField()
    d_adrs = models.CharField(max_length=50)
    d_phno = models.IntegerField()
    d_img = models.FileField()
    d_lcnc = models.FileField()
    d_bio = models.FileField()
    d_username = models.CharField(max_length=10, unique=True)
    d_password = models.CharField(max_length=10)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in-duty', 'In-Duty'),
        ('off-duty', 'Off-Duty'),
    ]
    d_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='off-duty')

# -------------------------------- ADD PRODUCT -------------------------------

class add_product(models.Model):
    pro_id = models.CharField(max_length=10)
    pro_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price = models.IntegerField()
    pro_img = models.FileField()

# -------------------------------- ADD EMPLOYEE -------------------------------

# class add_employee(models.Model):
#     emp_id = models.CharField(max_length=10)
#     emp_name = models.CharField(max_length=20)
#     emp_dob = models.DateField()
#     emp_adrs = models.CharField(max_length=50)
#     emp_phno = models.IntegerField()
#     emp_img = models.FileField()

# -------------------------------- ADD OFFER -------------------------------

# class add_offer(models.Model):
#     ofr_id = models.CharField(max_length=10)
#     ofr_date = models.DateField()
#     ofr_img = models.FileField()
#     ofr_exp = models.CharField(max_length=10)

# -------------------------------- CART -------------------------------

class Cart(models.Model):
    product_details = models.ForeignKey(add_product,on_delete=models.CASCADE)
    user_details = models.ForeignKey(u_register,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()

# -------------------------------- FEEDBACK -------------------------------

class Feedback(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField()
    message = models.CharField(max_length=250)

# -------------------------------- WISHLIST -------------------------------

class Wishlist(models.Model):
    user_details = models.ForeignKey(u_register,on_delete=models.CASCADE)
    item_details = models.ForeignKey(add_product,on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    status = models.IntegerField(default=0)

# -------------------------------- BOOKINGS -------------------------------

class Order(models.Model):
    customer = models.ForeignKey(u_register, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True,blank=True)  # Adjust according to your requirements
    product = models.ForeignKey(add_product, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(d_register, on_delete=models.SET_NULL, null=True, blank=True)
    so_fname = models.CharField(max_length=20, null=False)
    so_lname = models.CharField(max_length=20)
    so_email = models.EmailField(null=False)
    so_phone = models.IntegerField(null=False)
    so_address = models.TextField(null=False)
    so_district = models.CharField(max_length=20, null=False)
    so_city = models.CharField(max_length=20, null=False)
    so_pincode = models.IntegerField(null=False)
    add_message = models.CharField(max_length=250)
    order_status = (
        ('Pending', 'Pending'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=150, choices=order_status, default='Pending')
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    order_id = models.CharField(max_length=150, null=False)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class orderitem(models.Model):
    orderdet = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(add_product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


# -------------------------------- FORGOT PASSWORD -------------------------------

class PasswordReset(models.Model):
    user=models.ForeignKey(u_register,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)


class PasswordResets(models.Model):
    delivery_person = models.ForeignKey(d_register, on_delete=models.CASCADE)
    token = models.CharField(max_length=4)
