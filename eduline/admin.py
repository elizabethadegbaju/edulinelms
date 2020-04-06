from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Checkout)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Message)
