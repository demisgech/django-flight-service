from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','email']
    search_fields = ['username','first_name','last_name','email']
    list_per_page = 10
    ordering = ['id','username','email']
    
    