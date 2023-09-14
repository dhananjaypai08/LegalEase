from django.contrib import admin
from .models import User, Expert

# Register your models here.
admin.site.register(User)
admin.site.register(Expert)