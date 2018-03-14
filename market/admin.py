from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Items)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(CartItem)
admin.site.register(Review)