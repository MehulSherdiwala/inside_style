from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as adminUser
from django.core.paginator import Paginator, EmptyPage, InvalidPage
# Create your views here.
from django.template import RequestContext
from django.views.generic.base import View
from .utils import render_to_pdf

from main.forms import DesignForm
from main.models import City, State, User, Designer, Address, Contact, Product, Category, Cart, Order, OrderItemPdt, \
    Payment, DesignElement, Design, ChatMessage, OrderItemDesign


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
            request.session['type'] = 0
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
            request.session['type'] = 0
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
            return render(request, 'login.html', {'redirect': '/login/'})


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
    des = Design.objects.all()

    return render(request, 'designs.html', {'design': des})


def product_list(request):
    pdt = Product.objects.all()

    page_data = Paginator(pdt, 9)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        pdt_list = page_data.page(page)
    except(EmptyPage, InvalidPage):
        pdt_list = page_data.page(page_data.num_pages)
    data = {
        'pdt': pdt_list
    }
    print(data)
    return render(request, 'product_list.html', data)


@staff_member_required
def design_element(request):
    return render(request, 'admin/design_element.html')


def fetch_pdt(request):
    pdt_id = request.GET['pdt_id']
    # pdt = Category.objects.all().product_set.all()
    pdt = Product.objects.filter(pk=pdt_id)
    print(pdt)
    data = serializers.serialize('json', pdt)
    d = {
        'pdt': serializers.serialize('json', pdt),
        'cat': serializers.serialize('json', Category.objects.filter(pk=pdt[0].category_id))
    }
    return JsonResponse(d)


def product(request, pdt_id):
    pdt = Product.objects.filter(pk=pdt_id)
    return render(request, 'product.html', {'pdt': pdt[0]})

    # return render(request, 'product_list.html')


# def product(request):
#   return render(request, 'product.html')


# cart

def cart(request):
    if 'id' in request.session:
        user_id = request.session['id']
        cart = Cart.objects.filter(user=user_id)

        data = {}
        i = 0
        for c in cart:
            if c.type == 1:
                item = Product.objects.filter(pk=c.product.id)[0]
            else:
                item = Design.objects.filter(pk=c.design.id)[0]

            data.update({i: {
                'item': item,
                'cart': c,
                'price': item.price * c.qty,
                'type': 'Product' if c.type == 1 else 'Design'
            }})
            i += 1
        return render(request, 'cart.html', {'data': data})
    else:
        return redirect('/login')


def addtocart(request):
    if 'id' in request.session:
        pdt_id = request.GET['id']
        type = request.GET['type']
        qty = int(request.GET['qty'])

        if type == '1':

            cart_count = Cart.objects.filter(product=pdt_id, user=request.session['id']).count()

            if cart_count > 0:
                cart_item = Cart.objects.get(product=pdt_id, user=request.session['id'])
                cart_item.qty += qty
                cart_item.save()
            else:
                pdt = Product.objects.filter(pk=pdt_id)
                user = User.objects.filter(pk=request.session['id'])
                c = Cart.objects.create(qty=qty, type=type, product=pdt[0], user=user[0])
                c.save()

        else:
            cart_count = Cart.objects.filter(design=pdt_id, user=request.session['id']).count()

            if cart_count > 0:
                cart_item = Cart.objects.get(design=pdt_id, user=request.session['id'])
                cart_item.qty += qty
                cart_item.save()
            else:
                design = Design.objects.filter(pk=pdt_id)
                user = User.objects.filter(pk=request.session['id'])
                c = Cart.objects.create(qty=qty, type=type, design=design[0], user=user[0])
                c.save()

        d = {
            'status': 'done'
        }
    else:
        d = {'redirect': 'login'}
    return JsonResponse(d)


def update_addtocart(request):
    type = request.GET['type']

    if type == 'update':
        cart_id = request.GET['cart_id']
        qty = request.GET['qty']

        cart_item = Cart.objects.get(pk=cart_id)
        cart_item.qty = qty
        cart_item.save()
        d = {
            'status': 'done'
        }
    else:
        cart_id = request.GET['cart_id']

        cart_item = Cart.objects.get(pk=cart_id)
        cart_item.delete()
        d = {
            'status': 'done'
        }
    return JsonResponse(d)


def checkout(request):
    if 'id' in request.session:
        addr = Address.objects.filter(user=request.session['id'])
        state = State.objects.all()
        cart = Cart.objects.filter(user=request.session['id'])

        data = {
            'addr': addr,
            'state': state,
            'cart': cart,
            'total': 0
        }
        return render(request, "checkout.html", data)
    else:
        return redirect('/login')


def order(request):
    if 'id' in request.session:
        user = User.objects.filter(pk=request.session['id'])[0]

        # order = OrderItemPdt.objects.select_related()
        # order = OrderItemPdt.objects.filter(order__user=user)

        order = Order.objects.filter(user=user)
        data = {}
        i = 0
        for o in order:
            oi = OrderItemPdt.objects.filter(order=o)
            if oi.count() > 0:
                for item in oi:
                    data.update({i: {
                        'image': item.product.image,
                        'name': item.product.pdt_name,
                        'price': item.product.price,
                        'status': o.status,
                        'order_no': o.id,
                        'datetime': o.datetime,
                        'category': 'Product',
                    }})
                    i += 1

            oi = OrderItemDesign.objects.filter(order=o)
            if oi.count() > 0:
                for item in oi:
                    data.update({i: {
                        'image': item.design.image,
                        'name': item.design.design_name,
                        'price': item.design.price,
                        'status': o.status,
                        'order_no': o.id,
                        'datetime': o.datetime,
                        'category': 'Design',
                    }})
                    i += 1

        # data = {
        #     'order': order,
        # }

        return render(request, "order.html", {'data': data})

    else:
        return redirect('/login')


def addAddress(request):
    if request.method == 'POST':
        user_id = request.session['id']
        user = User.objects.filter(pk=user_id)[0]
        addr = Address.objects.create(addr=request.POST['addr'], phone=request.POST['phone'],
                                      pincode=request.POST['pincode'],
                                      name=request.POST['name'],
                                      city=City.objects.filter(pk=request.POST['city'])[0],
                                      user=user)
        addr.save()
    return redirect('/checkout')


def placeOrder(request):
    if request.method == 'POST':
        print(request.POST)
        user = User.objects.filter(pk=request.session['id'])[0]
        addr = Address.objects.filter(pk=request.POST['address'])[0]

        order = Order.objects.create(addr=addr, user=user)
        order.save()
        print(order.id)

        for c in request.POST.getlist('cart'):
            cart = Cart.objects.get(pk=c)
            if cart.type == 1:
                orderItem = OrderItemPdt.objects.create(qty=cart.qty, price=cart.product.price, product=cart.product,
                                                        order=order)
                orderItem.save()
            else:
                orderItem = OrderItemDesign.objects.create(price=cart.design.price, design=cart.design, order=order)
                orderItem.save()
            cart.delete()
            print(orderItem)

        pay = Payment.objects.create(amount=request.POST['amount'], payment_method=request.POST['payment_method'],
                                     order=order)
        pay.save()

    return redirect('/order')


def designProduct(request, design_id):
    desEle = DesignElement.objects.filter(design_id=design_id)

    design = Design.objects.filter(pk=design_id)

    data = {}
    i = 0
    for d in desEle:
        data.update({i: {
            'pos_X': d.pos_X,
            'pos_Y': d.pos_Y,
            'width': d.width,
            'height': d.height,
            'pdt': Product.objects.filter(pk=d.pdt_id.id)[0],
        }})
        i += 1

    data.update({'design': {'d': design[0]}})

    return render(request, 'designProduct.html', {'data': data})

    # return render(request, "order.html")


def chat(request):
    if 'type' in request.session:
        if request.session['type'] == 1:
            return redirect("login")
        else:
            return render(request, "chat.html")
    else:
        return redirect("login")


def getMsgs(request, user_id):
    if request.session['type'] == 0:
        user = User.objects.filter(pk=request.session['id'])[0]
        msgs = ChatMessage.objects.filter(designer=user_id, user=user)
        chatUser = Designer.objects.filter(pk=user_id)[0].designer_name
    else:
        designer = Designer.objects.filter(pk=request.session['id'])[0]
        msgs = ChatMessage.objects.filter(designer=designer, user=user_id)
        chatUser = User.objects.filter(pk=user_id)[0].username

    data = {
        'msg': serializers.serialize('json', msgs),
        'chatUser': chatUser
    }
    msgs.update(status=1)

    return JsonResponse(data)


def getChatList(request):
    data = {}

    if request.session['type'] == 0:
        user = User.objects.filter(pk=request.session['id'])[0]
        msgs = ChatMessage.objects.filter(user=user).values('designer').annotate(dcount=Count('designer'))
        for m in msgs:
            data.update({m['designer']: {
                'username': Designer.objects.filter(pk=m['designer'])[0].designer_name
            }})
    else:
        designer = Designer.objects.filter(pk=request.session['id'])[0]
        msgs = ChatMessage.objects.filter(designer=designer).values('user').annotate(dcount=Count('user'))
        for m in msgs:
            data.update({m['user']: {
                'username': User.objects.filter(pk=m['user'])[0].username
            }})

    return JsonResponse(data)


def send_msg(request):
    msg = request.GET['msg']
    sender = request.session['type']
    if request.session['type'] == 0:
        designer = Designer.objects.filter(pk=request.GET['user_id'])[0]
        user = User.objects.filter(pk=request.session['id'])[0]
    else:
        designer = Designer.objects.filter(pk=request.session['id'])[0]
        user = User.objects.filter(pk=request.GET['user_id'])[0]

    chat = ChatMessage.objects.create(msg=msg, sender=sender, type=0, status=0,
                                      user=user,
                                      designer=designer)
    chat.save()

    return JsonResponse({})


def getUnseenMsg(request):
    if request.session['type'] == 0:
        user_id = request.session['id']
        designer_id = request.GET['user_id']
    else:
        user_id = request.GET['user_id']
        designer_id = request.session['id']

    user = User.objects.filter(pk=user_id)[0]
    designer = Designer.objects.filter(pk=designer_id)[0]

    msgs = ChatMessage.objects.filter(user=user, designer=designer, status=0,
                                      sender=(0 if request.session['type'] == 1 else 1))

    data = serializers.serialize('json', msgs)
    msgs.update(status=1)

    return HttpResponse(data, content_type="application/json")


def unseenCnt(request):
    if request.session['type'] == 0:
        user = User.objects.filter(pk=request.session['id'])[0]
        msgs = ChatMessage.objects.filter(user=user, sender=1, status=0,
                                          designer__in=request.POST.getlist('from[]')).values('designer').annotate(
            count=Count('designer'))
    else:
        designer = Designer.objects.filter(pk=request.session['id'])[0]
        msgs = ChatMessage.objects.filter(designer=designer, sender=0, status=0,
                                          user__in=request.POST.getlist('from[]')).values('user').annotate(
            count=Count('user'))

    data = {}
    for m in msgs:
        if 'designer' in m:
            data.update({m['designer']: {
                'count': m['count']
            }})
        else:
            data.update({m['user']: {
                'count': m['count']
            }})

    return JsonResponse(data)


def designer_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        designer = Designer.objects.filter(email=email, password=password)

        if designer.exists():
            request.session['email'] = designer[0].email
            request.session['type'] = 1
            request.session['username'] = designer[0].designer_name
            request.session['id'] = designer[0].id
            return redirect('/')

        else:
            messages.info(request, "Invalid Email or Password")
            return redirect('login')

    else:
        if 'username' in request.session:
            return redirect('/')
        else:
            return render(request, 'login.html', {'redirect': '/designer/login/'})


def designer_chat(request):
    if 'type' in request.session:
        if request.session['type'] == 0:
            return redirect("login")
        else:
            return render(request, "chat.html")

    return redirect("login")


def sendAttach(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)

    msg = fs.url(filename)
    sender = request.session['type']
    if request.session['type'] == 0:
        designer = Designer.objects.filter(pk=request.POST['user_id'])[0]
        user = User.objects.filter(pk=request.session['id'])[0]
    else:
        designer = Designer.objects.filter(pk=request.session['id'])[0]
        user = User.objects.filter(pk=request.POST['user_id'])[0]

    chat = ChatMessage.objects.create(msg=msg, sender=sender, type=1, status=0,
                                      user=user,
                                      designer=designer)
    chat.save()

    data = {
        'url': msg,
        'ext': 2
    }
    return JsonResponse(data)


def designer_dashboard(request):
    if 'id' in request.session:
        designer_id = request.session['id']
        if request.method == "POST":
            designer = Designer.objects.filter(pk=designer_id)[0]
            designer.designer_name = request.POST['username']
            designer.description = request.POST['description']
            designer.phone = request.POST['phone']

            designer.save()

            return redirect("designer_dashboard")

        else:
            designer = Designer.objects.filter(pk=designer_id)[0]

            data = {
                'username': designer.designer_name,
                'email': designer.email,
                'phone': designer.phone,
                'description': designer.description,
            }

            return render(request, "designer_dashboard.html", data)
    else:
        return redirect('login')


def designer_design(request):
    if 'id' in request.session:
        design = Design.objects.all()
        ins_choice = {
            1: "Admin",
            2: "Designer"
        }

        return render(request, 'designer_design.html', {'data': design})
    else:
        return redirect('designer_login/')


def designer_design_add(request):
    if 'id' in request.session:
        if request.method == 'POST':
            form = DesignForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                print('success')

            return render('designer_design')
        else:
            return render(request, 'designer_design_add.html')
    else:
        return render('designer_login')


def designer_design_edit(request, design_id):
    if 'id' in request.session:
        if request.method == 'POST':
            design = Design.objects.filter(pk=design_id)[0]
            design.design_name = request.POST['design_name']
            design.price = request.POST['price']
            design.description = request.POST['description']
            if 'image' in request.FILES:
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                design.image = filename
            design.save()

            return redirect('designer_design')
        else:
            design = Design.objects.filter(pk=design_id)[0]
            return render(request, 'designer_design_edit.html', {'design': design})
    else:
        return redirect('designer_login')


def designer_design_delete(request, design_id):
    if 'id' in request.session:
        design = Design.objects.filter(pk=design_id)[0]
        design.delete()
        return redirect('designer_design')
    else:
        return redirect('designer_login')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        design = Design.objects.all()
        data = {
            'design': design
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
