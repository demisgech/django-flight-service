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
    PromotionFactory,
    ReviewFactory,
    SeatFactory,
    WishlistFactory,
    )


# @transaction.atomic
def run(data=200):
    # CurrencyFactory.create_batch(data)
    # CurrencyFactory.create_batch(30)
    # PromotionFactory.create_batch(data)
    # CustomerFactory.create_batch(data)
    # AddressFactory.create_batch(data)
    # AirportFactory.create_batch(data)
    # FlightFactory.create_batch(data)
    # FlightStatusFactory.create_batch(data)
    # FlightStatusFactory.create_batch(4)
    # SeatFactory.create_batch(data)
    # BookingFactory.create_batch(data)
    # PaymentMethodFactory.create_batch(data)
    # PaymentMethodFactory.create_batch(4)
    PaymentFactory.create_batch(data)
    # ReviewFactory.create_batch(data)
    # WishlistFactory.create_batch(data)

    
    