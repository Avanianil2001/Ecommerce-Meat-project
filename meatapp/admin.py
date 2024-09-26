from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(u_register)
admin.site.register(d_register)
admin.site.register(add_product)
# admin.site.register(add_employee)
# admin.site.register(add_offer)
admin.site.register(Cart)
admin.site.register(Feedback)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(orderitem)