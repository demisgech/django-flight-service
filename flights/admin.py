from django.contrib import admin
from django.db.models.query import QuerySet
from rest_framework.request import Request

from .filters import CustomerLoyaltyPointsFilter
from .models import (
    Address, Airport, Booking, Currency, Customer, Flight,
    FlightStatus, Payment, PaymentMethod, Promotion, Review, Seat, WishList
    )



admin.site.site_header = "Flight Booking Administration"
admin.site.site_title = "Flight Booking Admin"
admin.site.index_title = "Welcome To Flight Booking Admin"


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title','discount','start_date','end_date','is_active']
    list_per_page = 10
    search_fields = ['title','start_date','end_date']
    list_filter = ['start_date','end_date']
    

class AddressInline(admin.StackedInline):
    model = Address
    min_num = 1
    max_num = 10
    extra = 0
    
    
@admin.register(Customer)
class CustomerProfileAdmin(admin.ModelAdmin):
    autocomplete_fields =['user','preferred_currency']
    list_display = ['user','birth_date','phone_number','passport_number',
                    'nationality','loyalty_points','preferred_currency','loyalty_tier'
                    ]
    inlines = [AddressInline]
    list_filter = ['preferred_language','loyalty_tier',CustomerLoyaltyPointsFilter]
    list_per_page = 10
    list_select_related = ['user','preferred_currency']
    ordering = ['loyalty_points','birth_date']
    search_fields = ['user__username__icontains','birth_date__icontains',
                     'phone_number__icontains','passport_number__icontains']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['street','city','state','zip','customer']
    list_per_page = 10
    search_fields = ['city','street','state','zip',
                     'customer__user__username__icontains',
                     'customer__user__first_name__icontains'
                     ]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name','code','exchange_rate','last_update']
    list_per_page = 20
    ordering = ['name','last_update']
    search_fields = ['name','code']
    

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name','city','country','iata_code','icao_code']
    list_per_page = 10
    search_fields = ['name','city','iata_code','icao_code']
    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','flight']
    list_display = ['user','flight','booking_date','seats','price_at_booking','payment_status']
    list_select_related = ['user','flight']
    list_per_page = 10
    actions = [
        'make_payment_status_paid',
        'make_payment_status_failed',
        'make_payment_status_pending'
        ]
    list_filter = ['payment_status','booking_date']
    search_fields = ['user__username__icontains','flight__flight_number']
    date_hierarchy = 'booking_date'
    
    @admin.action(description="Make payment status paid")
    def make_payment_status_paid(self,request,queryset:QuerySet):
        queryset.update(payment_status="paid")
    
    def make_payment_status_failed(self,request, queryset:QuerySet):
        queryset.update(payment_status='failed')
    
    def make_payment_status_pending(self,request, queryset:QuerySet):
        queryset.update(payment_status='pending')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['booking','payment_method','currency']
    list_display = ['booking','payment_method','payment_date'
                    ,'amount','transaction_id','currency']
    # list_select_related = ['booking','currency','payment_method']
    list_filter = ['payment_method','payment_date']
    list_per_page = 10
    search_fields = ['transaction_id']


class FlightStatusInline(admin.TabularInline):
    model = FlightStatus
    min_num = 1
    max_num = 10
    extra = 0
    

class SeatInline(admin.TabularInline):
    model = Seat
    min_num = 1
    max_num = 10
    extra = 0
    

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    autocomplete_fields = ['departure_airport','arrival_airport']
    list_display = ['airline','flight_number','departure_airport',
                    'arrival_airport','arrival_time','departure_time',
                    'duration','price','seat_capacity'
                    ]
    search_fields = ['airline','flight_number',
                     'arrival_airport__name__icontains',
                     'departure_airport__name__icontains']
    inlines = [FlightStatusInline, SeatInline]
    list_per_page = 10
    list_editable = ['price','seat_capacity','duration']
    list_filter = ['arrival_time','departure_time']
    filter_horizontal = ['promotions']
    date_hierarchy = 'departure_time'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','flight']
    list_display = ['user','flight','rating','description','date']
    list_per_page = 10
    list_filter = ['rating','date']
    

@admin.register(WishList)
class WishlistAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','flight']
    list_display = ['user','flight','created_at']
    list_per_page = 10
    list_filter = ['created_at']
    search_fields = ['user__username__icontains',
                     'user__first_name__icontains',
                     'user__last_name__icontains',
                     'flight__airline__icontains']
    

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    actions = ['mark_available','mark_unavailable']
    autocomplete_fields = ['flight']
    list_display = ['seat_number','seat_class','flight','availability']
    list_filter = ['seat_class','availability']
    list_per_page = 10
    search_fields = ['seat_number','flight__flight_number']
    
    @admin.action(description='Mark Available')
    def mark_available(self,request:Request,queryset:QuerySet):
        queryset.update(availability=True)
    
    @admin.action(description='Mark unavailable')
    def mark_unavailable(self,request:Request,queryset:QuerySet):
        queryset.update(availability=False)
        
        