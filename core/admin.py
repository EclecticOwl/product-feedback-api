from django.contrib import admin
from .models import CustomUser, Product, Feedback


admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Feedback)