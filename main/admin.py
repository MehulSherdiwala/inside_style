from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite, SimpleListFilter
from django import forms
from django.contrib.auth.models import User as adminUser

from main.models import State, City, Designer, User, Branch, Category, Product, Design

# Headers
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
    add_form_template = 'admin/designer_form.html'
    change_form_template = 'admin/designer_form.html'
    list_display = ("designer_name", "email", "phone", "status")
    list_filter = ("status", "join_date")


# Designer --end--

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "status")
    list_filter = ("status", "join_date")


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
    add_form_template = 'admin/designer_form.html'
    change_form_template = 'admin/designer_form.html'
    list_display = ("branch_name", "addr", "city")
    list_filter = ("city", "created_at")


# Branch Ends

admin.site.register(Category)


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
    fields = ("pdt_name", "description", "price", "image", "prodImg", "category", "status")
    list_display = ("pdt_name", "price", "prodImg", "category", "status")
    list_filter = (CatFilter, "status", "created_at")
    search_fields = ("pdt_name",)
    readonly_fields = ("prodImg",)

    def catagory(self, obj):
        result = Category.objects.filter(pk=obj)
        return result['cat_name']


# Product End

# TODO: Edit Design creator Box Pending
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
        fields = ('design_name', 'description', 'image', 'inserted_by', 'creator_id', 'status')
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
    add_form_template = "admin/design_form.html"
    change_form_template = "admin/design_form.html"
    list_display = ('design_name', 'prodImg', "inserted_by", 'creator', 'status')
    list_filter = ('inserted_by', 'created_at', 'status')

    def creator(self, obj):
        if obj.inserted_by == 1:
            return adminUser.objects.filter(pk=obj.creator_id)[0].username
        else:
            return Designer.objects.filter(pk=obj.creator_id)[0].designer_name

