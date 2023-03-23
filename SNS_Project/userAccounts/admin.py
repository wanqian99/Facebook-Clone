from django.contrib import admin
from .models import *
# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
    list_display=('user', 'image', 'phone_number', 'dob')

admin.site.register(UserAccount, UserAccountAdmin)


# admin superuser
# username: admin
# email: admin@gmail.com
# password: password