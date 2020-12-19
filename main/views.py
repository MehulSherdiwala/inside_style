from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html', {'name': 'Mehul Sherdiwala'})


def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def log(request):
    return render(request, 'log.html')

def index(request):
    return render(request, "index.html")