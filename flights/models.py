from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Promotion(models.Model):
    title = models.CharField(max_length=150)
    discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15,null=True)
    birth_date = models.DateField(null=True)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=150)
    state = models.CharField(max_length=5)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

    
class AirPort(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country= models.CharField(max_length=150)
    iata_code = models.CharField(max_length=3,unique=True)
    inca_code = models.CharField(max_length=4,unique=True)
    latitude = models.DecimalField(max_digits=4,decimal_places=2)
    longitude = models.DecimalField(max_digits=4,decimal_places=2)
    time_zone = models.CharField(max_length=50)
    

class Flight(models.Model):
    FLIGHT_STATUS = [
        ('On time',"On Time"),
        ('delayed','Delayed'),
        ('canceled','Canceled')
    ]
    airline = models.CharField(max_length=150)
    flight_number = models.CharField(max_length=10,unique=True)
    departure_airport = models.ForeignKey(AirPort,on_delete=models.PROTECT)
    departure_time = models.DateTimeField()
    arrival_airport = models.ForeignKey(AirPort, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    seat_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=10,choices=FLIGHT_STATUS,default="On Time")
    promotions = models.ManyToManyField(Promotion,related_name='flights')


class FlightStatus(models.Model):
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    current_status  = models.CharField(max_length=50)
    status_update_time = models.DateTimeField(auto_now=True)
    

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20,choices=[
        ('paid','Paid'),
        ('pending','Pending'),
        ("failed","Failed")
    ],default='Pending')
   

class PaymentMethod(models.Model):
    PAYMENT_METHODS = [
        ('credit_card',"Credit Card"),
        ('paypal','PayPal'),
        ('telebirr','Tele Birr'),
        ('bank_transfer','Bank Transfer')
    ]
    name = models.CharField(max_length=255,choices=PAYMENT_METHODS,default="PayPal")
    
    
class Payment(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.PROTECT)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_id = models.CharField(max_length=100,unique=True)
    currency_code = models.CharField(max_length=3)
    

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3,unique=True)
    exchange_rate = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    last_update = models.DateTimeField(auto_now_add=True)
    

class Seat(models.Model):
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_class = models.CharField(max_length=20,choices=[
        ('economic','Economic'),
        ('business','Business')
    ],default='Economic')
    availablity = models.BooleanField(default=True)
    

class Review(models.Model):
    RATINGS = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS, default=0)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
