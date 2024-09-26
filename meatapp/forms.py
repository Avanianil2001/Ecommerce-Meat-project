from django import forms
from .models import *

# Create your formss here.

class UserProfileForm(forms.Form):
    u_name = models.CharField(max_length=20)
    email = models.EmailField()
    u_phno = models.IntegerField()
    u_img = models.FileField()
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=10)
    u_address = models.CharField(max_length=100)
    u_district = models.CharField(max_length=20)
    u_city = models.CharField(max_length=20)
    u_pincode = models.IntegerField()

class DelboyProfileForm(forms.Form):
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