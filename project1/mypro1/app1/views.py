from django.shortcuts import render
from django.http import HttpResponse

def app1(request):
    return HttpResponse("Hello world!")