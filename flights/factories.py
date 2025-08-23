
import random, string
from django.utils import timezone
from factory import django, faker, declarations
import factory

from core.factories import UserFactory
from .models import (
    Address, Airport, Booking, 
    Currency, Customer, Flight, 
    FlightStatus, Payment, PaymentMethod,
    Promotion, Review, Seat, WishList
    )


class PromotionFactory(django.DjangoModelFactory):
    
    class Meta:
        model = Promotion
        
    title = faker.Faker('catch_phrase', nb_words=3)
    discount = faker.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    start_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=random.randint(1,25)))
    end_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=random.randint(30, 400)))
    

class CurrencyFactory(django.DjangoModelFactory):
    class Meta:
        model = Currency
    
    code = faker.Faker('currency_code')
    name = faker.Faker('currency_name')
    exchange_rate = faker.Faker('pydecimal', left_digits=1, right_digits=4, positive=True, min_value=0.01, max_value=3.0)
    
    
class CustomerFactory(django.DjangoModelFactory):
    class Meta:
        model = Customer
    
    user = declarations.SubFactory(UserFactory)
    birth_date = faker.Faker('date_of_birth',minimum_age=18, maximum_age=90)
    phone_number = faker.Faker('phone_number')
    gender = factory.Iterator(['Male',"Female","Other"])
    passport_number = factory.Sequence(lambda n: f'PASS{1000 + n}')
    passport_expiry = faker.Faker('future_date',end_date="+10y")
    nationality = faker.Faker('country')
    preferred_language = factory.Iterator(['en','am'])
    loyalty_points = faker.Faker('random_int', min=0, max=10000)
    loyalty_tier = factory.Iterator(['bronze', 'silver', 'gold', 'platinum'])
    preferred_currency = declarations.SubFactory(CurrencyFactory)


class AddressFactory(django.DjangoModelFactory):
    class Meta:
        model = Address
    
    street = faker.Faker('street_address')
    city = faker.Faker('city')
    zip = faker.Faker('postcode')
    state = faker.Faker('state_abbr')
    customer = declarations.SubFactory(CustomerFactory)
    

class AirportFactory(django.DjangoModelFactory):
    class Meta:
        model = Airport
    name = faker.Faker('city')
    city = faker.Faker('city')
    country = faker.Faker('country')
    iata_code = factory.LazyFunction(lambda: ''.join(random.choices(string.ascii_uppercase, k=3)))
    icao_code = factory.LazyFunction(lambda: ''.join(random.choices(string.ascii_uppercase, k=4)))
    latitude = faker.Faker('pydecimal', left_digits=2, right_digits=6, positive=False)
    longitude = faker.Faker('pydecimal', left_digits=3, right_digits=6, positive=False)
    time_zone = faker.Faker('timezone')


class FlightFactory(django.DjangoModelFactory):
    class Meta:
        model = Flight
    
    airline = faker.Faker('company')
    flight_number = factory.declarations.Sequence(lambda n: f'FL{1000 + n}')
    departure_time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=1))
    departure_airport = factory.SubFactory(AirportFactory)
    arrival_time = factory.LazyAttribute(lambda obj: obj.departure_time + timezone.timedelta(hours=2))
    arrival_airport = factory.SubFactory(AirportFactory)
    duration = factory.LazyAttribute(lambda obj: obj.arrival_time - obj.departure_time)
    seat_capacity = faker.Faker('random_int', min=50, max=300)
    price = faker.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    
    
    @factory.post_generation
    def promotions(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for promo in extracted:
                self.promotions.add(promo)
        else:
            self.promotions.add(PromotionFactory())
            
class FlightStatusFactory(django.DjangoModelFactory):
    class Meta:
        model = FlightStatus
    
    flight = factory.SubFactory(FlightFactory)
    status = factory.Iterator(['on_time','boarding', 'delayed', 'cancelled'])



class BookingFactory(django.DjangoModelFactory):
    class Meta:
        model = Booking
    
    user = factory.SubFactory(UserFactory)
    flight = factory.SubFactory(FlightFactory)
    booking_date = factory.LazyFunction(timezone.now)
    seats = faker.Faker('random_int', min=1, max=5)
    price_at_booking = factory.LazyAttribute(lambda obj: obj.seats * obj.flight.price)
    payment_status = factory.Iterator(['pending', 'completed', 'failed'])
    
    

class PaymentMethodFactory(django.DjangoModelFactory):
    class Meta:
        model = PaymentMethod
    
    name = factory.Iterator(['credit_card','paypal','telebirr','bank_transfer'])
    

class PaymentFactory(django.DjangoModelFactory):
    class Meta:
        model = Payment
    
    booking = factory.SubFactory(BookingFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    amount = faker.Faker('pydecimal',left_digits=3,right_digits=2,positive=True)
    transaction_id = factory.Sequence(lambda n: f"TX{1000 + n}")
    currency = factory.SubFactory(CurrencyFactory)
    
    
class SeatFactory(django.DjangoModelFactory):
    class Meta:
        model = Seat
    
    flight = factory.SubFactory(FlightFactory)
    seat_number = factory.Sequence(lambda n: f"{(n // 6) + 1}{chr(65 + (n % 6))}")
    seat_class = factory.Iterator(['economy','business'])
    availability = faker.Faker('boolean')


class ReviewFactory(django.DjangoModelFactory):
    class Meta:
        model = Review
    
    user = factory.SubFactory(UserFactory)
    flight = factory.SubFactory(FlightFactory)
    rating = factory.Iterator([0,1,2,3,4,5])
    description = faker.Faker('sentence')
    

class WishlistFactory(django.DjangoModelFactory):
    class Meta:
        model = WishList
    
    user = factory.SubFactory(UserFactory)
    flight = factory.SubFactory(FlightFactory)
    
