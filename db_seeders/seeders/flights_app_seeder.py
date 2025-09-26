from django.db import transaction

from flights.factories import (
    AddressFactory,
    AirportFactory,
    BookingFactory,
    CurrencyFactory,
    CustomerFactory,
    FlightFactory,
    FlightStatusFactory,
    PaymentFactory,
    PaymentMethodFactory,
    PaymentStatusFactory,
    PromotionFactory,
    ReviewFactory,
    SeatClassFactory,
    SeatFactory,
    WishlistFactory,
    )


# @transaction.atomic
def run(data=200):
    
    CurrencyFactory.create_batch(30)
    PromotionFactory.create_batch(100)
    CustomerFactory.create_batch(data)
    AddressFactory.create_batch(data)
    AirportFactory.create_batch(data)
    
    FlightStatusFactory.create_batch(4)
    FlightFactory.create_batch(data)
    
    SeatClassFactory.create_batch(2)
    SeatFactory.create_batch(data)
    
    PaymentStatusFactory.create_batch(3)
    BookingFactory.create_batch(data)
    
    PaymentMethodFactory.create_batch(4)
    PaymentFactory.create_batch(data)
    ReviewFactory.create_batch(data)
    WishlistFactory.create_batch(data)

    
    