
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from .models import User

def user_list(request:HttpRequest)->HttpResponse:
    queryset = User.objects.all()
    return render(request,template_name="static/users.html",context={"users":list(queryset)})


