from django.contrib import admin

from .models import Promotion

admin.site.site_header = "Flight Service Administration"

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title','discount','start_date','end_date']
    

class CustomerAdmin(admin.ModelAdmin): ...
