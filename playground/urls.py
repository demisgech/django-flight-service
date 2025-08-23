from django.urls import path

from .views import index, say_hello

urlpatterns = [
    path("",index),
    path("hello/",say_hello)
]

