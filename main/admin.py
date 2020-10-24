from django.contrib import admin
from .models import OrderList,Book,Customer,UserType
admin.site.register(OrderList)
admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(UserType)

# Register your models here.
