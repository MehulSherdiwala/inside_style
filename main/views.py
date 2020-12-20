from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from main.models import City, State


def home(request):
    return render(request, 'home.html', {'name': 'Mehul Sherdiwala'})


def about(request):
    return render(request, 'about.html')


def load_city(request):
    state = request.GET['state']
    cities = City.objects.filter(state=state)
    data = serializers.serialize('json', cities)
    return HttpResponse(data, content_type="application/json")


def load_state(request):
    city = request.GET['city']
    cities = City.objects.filter(pk=city)
    # state = State.objects.filter(pk=cities['state'])
    # state = State.objects.all()
    data = serializers.serialize('json', cities)
    return HttpResponse(data, content_type="application/json")
