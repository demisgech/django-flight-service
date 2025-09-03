from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from flights.admin import FlightAdmin,BookingAdmin
from core.models import User
from flights.models import Flight,Booking
from tags.models import TaggedItem


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username','first_name','last_name','email','is_staff']
    search_fields = ['username','first_name','last_name','email']
    list_per_page = 10
    ordering = ['id','username','email','first_name','last_name']
    
    add_fieldsets = ((
        None,
        {
            "classes":("wide",),
            "fields": ("username","email","usable_password","password1","password2")
        }
    ),)
    

class TaggedItemInline(admin.TabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    min_num = 1
    max_num = 10
    extra = 0
    

# admin.site.unregister(Booking)

# @admin.register(Booking)
# class CoreBookingAdmin(BookingAdmin):
#     inlines = [TaggedItemInline]