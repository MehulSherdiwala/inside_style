from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session

# Create your views here.
from django.template import RequestContext

from main.models import City, State, User


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


# Registration
def registration(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email is already exist.")
            return redirect('/registration')

        else:
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
            request.session['email'] = user.email
            request.session['username'] = user.username
            request.session['id'] = user.id

        return redirect('/')

    else:
        if 'username' in request.session:
            return redirect('/')
        else:
            return render(request, 'registration.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email, password=password)

        if user.exists():
            request.session['email'] = user[0].email
            request.session['username'] = user[0].username
            request.session['id'] = user[0].id
            return redirect('/')

        else:
            messages.info(request, "Invalid Email or Password")
            return redirect('login')

    else:
        if 'username' in request.session:
            return redirect('/')
        else:
            return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('/')


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, 'contact.html')

def userdash(request):
    return render(request, "userdash.html")


