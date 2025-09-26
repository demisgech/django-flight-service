from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Promotion(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    @property
    def is_active(self):
        from django.utils.timezone import now
        return "✅ Yes" if self.start_date <= now() <= self.end_date else "❌ No"

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='customer_profile')
    birth_date = models.DateField(null=True)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        blank=True,
        default='other'
    )
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    passport_expiry = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    preferred_language = models.CharField(max_length=10, choices=[('en', 'English'), ('am', 'Amharic')], default='en')
    preferred_currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    loyalty_tier = models.CharField(max_length=20, choices=[
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum')
    ], default='bronze')
    # profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=150)
    state = models.CharField(max_length=5)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.street}, {self.city}"
    
    
class Airport(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country= models.CharField(max_length=150)
    iata_code = models.CharField(max_length=3,unique=True)
    icao_code = models.CharField(max_length=4,unique=True)
    latitude = models.DecimalField(max_digits=8,decimal_places=6)
    longitude = models.DecimalField(max_digits=8,decimal_places=6)
    time_zone = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name


class FlightStatus(models.Model):
    FLIGHT_STATUS = [
        ('on_time',"On time"),
        ('delayed','Delayed'),
        ('canceled','Canceled'),
        ('boarding','Boarding')
    ]
    name = models.CharField(max_length=10,choices=FLIGHT_STATUS,default="on_time")
    
    def __str__(self):
        return self.name
    

class Flight(models.Model):
    airline = models.CharField(max_length=150)
    flight_number = models.CharField(max_length=10,unique=True)
    departure_time = models.DateTimeField()
    departure_airport = models.ForeignKey(Airport,on_delete=models.PROTECT,related_name='departure_flights')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name='arrival_flights')
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    seat_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    status = models.ForeignKey(FlightStatus,on_delete=models.CASCADE,
                               related_name="flights",default=1)
    updated_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    promotions = models.ManyToManyField(Promotion,related_name='flights')

    def __str__(self) -> str:
        return self.airline


class PaymentStatus(models.Model):
    name = models.CharField(max_length=20,choices=[
        ('paid','Paid'),
        ('pending','Pending'),
        ("failed","Failed")
    ],default='pending')
    
    def __str__(self) -> str:
        return self.name
    

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='bookings')
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.ForeignKey(PaymentStatus,on_delete=models.CASCADE,
                                       related_name="bookings",default=1)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self) -> str:
        return f"{self.user.get_full_name()} for {self.flight.airline}"
   

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3,unique=True)
    exchange_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        validators=[MinValueValidator(0)]
    )
    last_update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['-last_update']
    
    
class PaymentMethod(models.Model):
    PAYMENT_METHODS = [
        ('credit_card',"Credit Card"),
        ('paypal','PayPal'),
        ('telebirr','Tele Birr'),
        ('bank_transfer','Bank Transfer')
    ]
    name = models.CharField(max_length=255,choices=PAYMENT_METHODS,default="paypal")
    
    # transaction_id has to be refactored
    
    def __str__(self) -> str:
        return self.name
    
    
class Payment(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.PROTECT)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_id = models.CharField(max_length=100,unique=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f"${self.amount} successfully paid with {self.payment_method.name}"


class SeatClass(models.Model):
    name = models.CharField(max_length=20,choices=[
        ('economy','Economy'),
        ('business','Business')
    ],default='economy')
    
    def __str__(self) -> str:
        return self.name
    
class Seat(models.Model):
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_class = models.ForeignKey(SeatClass,on_delete=models.CASCADE,
                                   related_name="seats",default=1)
    availability = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('flight', 'seat_number')
    

class Review(models.Model):
    RATINGS = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="reviews")
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS, default=0)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'flight')
        ordering = ['-date']


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wishlist_items")
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'flight')
        ordering = ['-created_at']

