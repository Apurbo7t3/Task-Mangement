from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("<h1 style='color:red'>This is Home Page</h1>")
def showTask(request):
    return HttpResponse('This is task page')