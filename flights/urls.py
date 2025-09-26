from django.urls import path

from flights.views import (
    AirportDetail,
    AirportList,
    FlightDetail,
    FlightList,
    PromotionDetail,
    PromotionList,
    flight_detail,
    flight_list,
    # airport_detail,
    # airport_list,
    # promotion_detail,
    # promotion_list
    )


urlpatterns = [
    # path("airports/",airport_list),
    # path("airports/<int:id>/",airport_detail),
    # path("promotions/",promotion_list),
    # path("promotions/<int:id>/",promotion_detail),
    path("airports/",AirportList.as_view()),
    path("airports/<int:id>/",AirportDetail.as_view()),
    path("promotions/",PromotionList.as_view()),
    path("promotions/<int:id>/",PromotionDetail.as_view()),
    
    # path("flights/",flight_list),
    # path("flights/<int:id>/",flight_detail),
    path("flights/",FlightList.as_view()),
    path("flights/<int:id>/",FlightDetail.as_view())
]
