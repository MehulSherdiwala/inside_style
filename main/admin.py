from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite, SimpleListFilter
from django import forms
from django.contrib.auth.models import User as adminUser
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from djongo import models

from main.models import State, City, Designer, User, Branch, Category, Product, Design, Contact, Address, DesignElement, \
    Order, OrderItemPdt, OrderItemDesign

from . import views
# Headers
from main.views import contact
from .utils import render_to_pdf

AdminSite.site_header = "Inside Style"
AdminSite.site_title = "Inside Style"


# State
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("state_name", "total_cities")
    search_fields = ("state_name__startswith",)

    def total_cities(self, obj):
        result = obj.city_set.count()
        return result


# State
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_name", "state")
    list_filter = ("state",)
    search_fields = ("city_name",)

    def state(self, obj):
        result = State.objects.filter(pk=obj)
        return result['state_name']

    state.short_description = "State Name"


# Designer --start--
def get_state():
    state_list = State.objects.all()

    select = tuple(((0, "--------"),))
    state_list = tuple((j.id, j.state_name) for j in state_list)

    state_list = select + state_list

    return state_list


class DesignerForm(forms.ModelForm):
    state = forms.ChoiceField()

    class Meta:
        model = Designer
        fields = (
            'designer_name', 'email', 'phone', 'password', 'description', 'join_date', 'state', 'city', 'admin',
            'status')

    # def __init__(self, *args, **kwargs):
    #     super(DesignerForm, self).__init__(*args, **kwargs)
    #     initial = kwargs.get('initial', {})
    # d = {**initial, **args}
    # print(self.instance.city.state_id)
    def __init__(self, *args, **kwargs):
        super(DesignerForm, self).__init__(*args, **kwargs)

        if hasattr(self.instance, 'city'):
            state_initial = self.instance.city.state_id
            self.fields['city'].queryset = City.objects.filter(state=state_initial)
        else:
            state_initial = 0
            self.fields['city'].queryset = City.objects.all()

        self.fields['state'] = forms.ChoiceField(
            choices=get_state(),
            initial=state_initial
        )


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    form = DesignerForm
    change_list_template = "admin/designer_list.html"
    add_form_template = 'admin/designer_form.html'
    change_form_template = 'admin/designer_form.html'
    list_display = ("designer_name", "email", "phone", "status")
    list_filter = ("status", "join_date")
    search_fields = ("designer_name__startswith", "email__startswith")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('designer_report/', self.designer_report, name="designer_report"),
        ]
        return my_urls + urls

    def designer_report(self, request):
        if request.method == 'POST':
            type = request.POST['type']
            designer = {}

            if type == '1':
                designer = Designer.objects.all()

            elif type == '2':
                designer = Designer.objects.filter(status=request.POST['status'])

            data = {
                'data': designer
            }
            pdf = render_to_pdf('admin/designer_report.html', data)
            return HttpResponse(pdf, content_type='application/pdf')


# Designer --end--

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "status")
    list_filter = ("status", "join_date")
    search_fields = ("username__startswith", "email__startswith",)

    def has_add_permission(self, request, obj=None):
        return False


# Branch Starts
class BranchForm(forms.ModelForm):
    state = forms.ChoiceField()

    class Meta:
        model = Branch
        fields = ('branch_name', 'addr', 'state', 'city', 'admin')

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields['state'] = forms.ChoiceField(
            choices=get_state()
        )
        self.fields['city'].queryset = City.objects.all()


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    form = BranchForm
    change_list_template = "admin/branch_list.html"
    add_form_template = 'admin/designer_form.html'
    change_form_template = 'admin/designer_form.html'
    list_display = ("branch_name", "addr", "city")
    list_filter = ("city", "created_at")
    search_fields = ("branch_name__startswith", "city__startswith",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('branch_report/', self.branch_report, name="branch_report"),
        ]
        return my_urls + urls

    def branch_report(self, request):
        branch = Branch.objects.all()
        data = {
            'data': branch
        }
        pdf = render_to_pdf('admin/branch_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Branch Ends

class Catadmin(admin.ModelAdmin):
    list_display = ("cat_name", "total_product")
    search_fields = ("cat_name__startswith",)
    change_list_template = "admin/cat_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('cat_report/', self.cat_report, name="cat_report"),
        ]
        return my_urls + urls

    def cat_report(self, request):
        cat = Category.objects.all()
        data = {
            'data': cat
        }
        pdf = render_to_pdf('admin/cat_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    def total_product(self, obj):
        result = obj.product_set.count()
        return result


admin.site.register(Category, Catadmin)


# Product Start
class CatFilter(SimpleListFilter):
    title = 'Category'
    parameter_name = 'Category'

    def lookups(self, request, model_admin):
        cat = Category.objects.all()
        cat_list = tuple((j.id, j.cat_name) for j in cat)
        return cat_list

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        else:
            return queryset.filter(category=self.value())


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = "admin/product_list.html"
    fields = ("pdt_name", "description", "price", "image", "prodImg", "category", "status")
    list_display = ("pdt_name", "price", "prodImg", "category", "status")
    list_filter = (CatFilter, "status", "created_at")
    search_fields = ("pdt_name", "category")
    readonly_fields = ("prodImg",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('product_report/', self.product_report, name="product_report"),
        ]
        return my_urls + urls

    def product_report(self, request):
        if request.method == 'POST':
            type = request.POST['type']
            product = {}

            if type == '1':
                product = Product.objects.all()

            elif type == '2':
                cat = Category.objects.filter(cat_name=request.POST['category'])
                product = Product.objects.filter(category=cat[0])

            elif type == '3':
                product = Product.objects.filter(status=request.POST['status'])

            data = {
                'data': product
            }
            pdf = render_to_pdf('admin/product_report.html', data)
            return HttpResponse(pdf, content_type='application/pdf')

    def catagory(self, obj):
        result = Category.objects.filter(pk=obj)
        return result['cat_name']


# Product End

def get_creator(user):
    if user == 1:
        user_list = adminUser.objects.all()
        user_list = tuple((j.id, j.username) for j in user_list)
    else:
        user_list = Designer.objects.all()
        user_list = tuple((j.id, j.designer_name) for j in user_list)

    select = tuple(((0, "--------"),))

    user_list = select + user_list

    return user_list


class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ('design_name', 'description', 'image', 'price', 'inserted_by', 'creator_id', 'status')

        # readonly_fields = ("prodImg",)

    def __init__(self, *args, **kwargs):
        super(DesignForm, self).__init__(*args, **kwargs)

        if hasattr(self.instance, 'inserted_by'):
            ins_by = self.instance.inserted_by
            # self.fields['city'].queryset = City.objects.filter(state=state_initial)
        else:
            ins_by = 1
            # self.fields['city'].queryset = City.objects.all()

        self.fields['creator_id'] = forms.ChoiceField(
            choices=get_creator(ins_by),
        )


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    form = DesignForm
    change_list_template = "admin/design_list.html"
    add_form_template = "admin/design_form.html"
    change_form_template = "admin/design_form.html"
    list_display = ('design_name', 'prodImg', "inserted_by", 'creator', 'status')
    list_filter = ('inserted_by', 'created_at', 'status')
    search_fields = ("design_name", "category")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('design_report/', self.design_report, name="design_report"),
            path('admin_design_report/', self.admin_design_report, name="admin_design_report"),
            path('designer_design_report/', self.designer_design_report, name="designer_design_report"),
        ]
        return my_urls + urls

    def design_report(self, request):
        design = Design.objects.all()
        data = {
            'design': design
        }
        pdf = render_to_pdf('admin/design_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    def admin_design_report(self, request):
        design = Design.objects.filter(inserted_by=1)
        data = {
            'design': design
        }
        pdf = render_to_pdf('admin/admin_design_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    def designer_design_report(self, request):
        design = Design.objects.filter(inserted_by=2)
        data = {
            'design': design
        }
        pdf = render_to_pdf('admin/designer_design_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    def creator(self, obj):
        if obj.inserted_by == 1:
            return adminUser.objects.filter(pk=obj.creator_id)[0].username
        else:
            return Designer.objects.filter(pk=obj.creator_id)[0].designer_name


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'addr', "pincode", 'phone', 'city')
    list_filter = ('user', 'city')

    def has_add_permission(self, request, obj=None):
        return False


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ("name__startswith", "email__startswith")

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Contact, ContactAdmin)


# my dummy model
class DesignEle(models.Model):
    class Meta:
        # model = DesignElement
        verbose_name_plural = 'Design Element'
        app_label = 'main'


# def my_custom_view(request):
#     return HttpResponse(request, '<h1>hello</h1>')

# class DesignEleAdmin(admin.ModelAdmin):
#     model = DesignEle
#
#     def get_urls(self):
#         view_name = '{}_{}_changelist'.format(
#             self.model._meta.app_label, self.model._meta.model_name)
#         return [
#             path('my_admin_path/', my_custom_view, name=view_name),
#         ]


# admin.site.register(DesignEle, DesignEleAdmin)


class DesignEleAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.display_list, name="display_list"),
            path('add/', self.map_product, name="map_product"),
        ]
        return my_urls + urls

    def display_list(self, request):

        dEle = DesignElement.objects.values('design_id').annotate(dcount=Count('design_id'))

        data = {}
        i = 0

        for d in dEle:
            design = Design.objects.filter(pk=d['design_id'])[0]
            data.update({i: {
                'design': design,
                'count': d['dcount'],
            }})
            print(data)
            i += 1

        context = dict(
            self.admin_site.each_context(request),
            data=data
        )

        return TemplateResponse(request, "admin/design_element_list.html", context)

    def map_product(self, request):
        if request.method == 'POST':
            print(request.POST)
            i = 0
            image = request.POST.get('image')
            pdt_id = request.POST.getlist('pdt_id')
            x = request.POST.getlist('x')
            y = request.POST.getlist('y')
            height = request.POST.getlist('height')
            width = request.POST.getlist('width')

            design = Design.objects.filter(image=image)[0]

            # print(x)
            # print(request.POST['x'])
            for p in pdt_id:
                pdt = Product.objects.filter(pk=p)
                dEle = DesignElement.objects.create(pos_X=x[i], pos_Y=y[i], width=width[i], height=height[i],
                                                    pdt_id=pdt[0], design_id=design)
                dEle.save()
                i += 1

            return redirect('/admin/main/designele/')

        else:
            pdt = Product.objects.filter(status=True)
            design = Design.objects.filter(status=True)

            context = dict(
                self.admin_site.each_context(request),
                pdt=pdt,
                design=design
            )

            return TemplateResponse(request, "admin/design_element.html", context)


admin.site.register(DesignEle, DesignEleAdmin)


class ItemPdt(admin.TabularInline):
    model = OrderItemPdt
    extra = 0
    readonly_fields = ('qty', 'price', 'product')

    def has_add_permission(self, request, obj=None):
        return False


class ItemDesign(admin.TabularInline):
    model = OrderItemDesign
    extra = 0
    readonly_fields = ('price', 'design')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('status',)
    list_display = ('id', 'user', 'addr', 'datetime', 'items', 'status')
    list_filter = ('user', 'status')
    inlines = [
        ItemPdt,
        ItemDesign,
    ]
    change_list_template = "admin/order_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('order_report/', self.order_report, name="order_report"),
        ]
        return my_urls + urls

    def order_report(self, request):
        if request.method == 'POST':
            type = request.POST['type']
            order = {}
            data = {}
            c = 0

            if type == '1':
                order = Order.objects.all()
                for o in order:
                    orderItem = OrderItemPdt.objects.filter(order=o)
                    if len(orderItem) > 0:
                        for i in orderItem:
                            data.update({c: {
                                'order': o.id,
                                'price': i.price,
                                'name': i.product.pdt_name,
                                'type': 'Product',
                                'qty': i.qty
                            }})
                            c += 1

                    orderItem = OrderItemDesign.objects.filter(order=o)
                    if len(orderItem) > 0:
                        for i in orderItem:
                            data.update({c: {
                                'order': o.id,
                                'price': i.price,
                                'name': i.design.design_name,
                                'type': 'Design',
                                'qty': 1
                            }})
                            c += 1

            elif type == '2':
                user = User.objects.filter(username=request.POST['username'])
                order = Order.objects.filter(user=user[0])
                for o in order:
                    orderItem = OrderItemPdt.objects.filter(order=o)
                    if len(orderItem) > 0:
                        for i in orderItem:
                            data.update({c: {
                                'order': o.id,
                                'price': i.price,
                                'name': i.product.pdt_name,
                                'type': 'Product',
                                'qty': i.qty
                            }})
                            c += 1

                    orderItem = OrderItemDesign.objects.filter(order=o)
                    if len(orderItem) > 0:
                        for i in orderItem:
                            data.update({c: {
                                'order': o.id,
                                'price': i.price,
                                'name': i.design.design_name,
                                'type': 'Design',
                                'qty': 1
                            }})
                            c += 1

            elif type == '3':
                order = Order.objects.filter(status=request.POST['status'])
                for o in order:
                    orderItem = OrderItemPdt.objects.filter(order=o)
                    if len(orderItem) > 0:
                        for i in orderItem:
                            data.update({c: {
                                'order': o.id,
                                'price': i.price,
                                'name': i.product.pdt_name,
                                'type': 'Product',
                                'qty': i.qty
                            }})
                            c += 1

                    orderItem = OrderItemDesign.objects.filter(order=o)
                    if len(orderItem) > 0:
                        for i in orderItem:
                            data.update({c: {
                                'order': o.id,
                                'price': i.price,
                                'name': i.design.design_name,
                                'type': 'Design',
                                'qty': 1
                            }})
                            c += 1
            data.update({
                'data': order,
            })
            pdf = render_to_pdf('admin/order_report.html', {'data' : data})
            return HttpResponse(pdf, content_type='application/pdf')

    def items(self, obj):
        pdt = OrderItemPdt.objects.filter(order=obj.id).values('order').annotate(dcount=Count('id'))
        count = 0
        if len(pdt) > 0:
            count += pdt[0]['dcount']

        design = OrderItemDesign.objects.filter(order=obj.id).values('order').annotate(dcount=Count('id'))
        if len(design) > 0:
            count += design[0]['dcount']

        return count

    def has_add_permission(self, request, obj=None):
        return False
