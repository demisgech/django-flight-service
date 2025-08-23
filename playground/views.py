from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request:HttpRequest)->HttpResponse:
    return HttpResponse("Ok")


def say_hello(request:HttpRequest)->HttpResponse:
    return render(request=request,template_name="index.html",context={"name":"Yohannis"})