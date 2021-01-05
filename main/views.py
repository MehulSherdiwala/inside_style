from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as adminUser
# Create your views here.
from django.template import RequestContext

from main.models import City, State, User, Designer, Address, Contact


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
        # password = pbkdf2_sha256.encrypt(request.POST['password'])

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

        # password = pbkdf2_sha256.encrypt(request.POST['password'])
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


def load_creator(request, ins_by):
    if int(ins_by) == 1:
        users = adminUser.objects.all()
    else:
        users = Designer.objects.all()
    data = serializers.serialize('json', users)
    return HttpResponse(data, content_type="application/json")


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Contact.name=name
        # Contact.email=email
        # Contact.message=message
        c = Contact.objects.create(name=name, email=email, message=message)
        c.save()

        return render(request, 'contact.html', {'name': name})

    else:
        return render(request, 'contact.html')


def user_dashboard(request):
    if 'id' in request.session:
        user_id = request.session['id']
        if request.method == "POST":
            user = User.objects.filter(pk=user_id)[0]
            user.username = request.POST['username']

            if not request.POST['addr']:
                addr = Address.objects.filter(user=user_id)[0]
                addr.addr = request.POST['addr']
                addr.phone = request.POST['phone']
                addr.pincode = request.POST['pincode']
                addr.city = City.objects.filter(pk=request.POST['city'])[0]

            else:
                addr = Address.objects.create(addr=request.POST['addr'], phone=request.POST['phone'],
                                              pincode=request.POST['pincode'],
                                              city=City.objects.filter(pk=request.POST['city'])[0],
                                              user=user)

            user.save()
            addr.save()

            return redirect("user_dashboard")

        else:
            user = User.objects.filter(pk=user_id)[0]

            data = {
                'username': user.username,
                'email': user.email,
            }
            addr = Address.objects.filter(user=user_id)

            state = State.objects.all()
            city = None
            if addr.count() > 0:
                city = City.objects.filter(state=addr[0].city.state_id)
                data.update({
                    'addr': addr[0].addr,
                    'phone': addr[0].phone,
                    'pincode': addr[0].pincode,
                    'selected_city': addr[0].city,
                    'addr_id': addr[0].id
                })

            data.update({'state': state, 'city': city})

            return render(request, "user_dashboard.html", data)
    else:
        return redirect('login')


def designs(request):
    return render(request, 'designs.html')