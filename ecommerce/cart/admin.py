from django.contrib import admin
from cart.models import Cart,Payment,Order_table

admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Order_table)