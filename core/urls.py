from django.urls import path, include

from .views import user_list

urlpatterns = [
    path("users/",user_list),
]
