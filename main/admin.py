from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django import forms

from main.models import State, City, Designer, User

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
        fields = ('designer_name', 'email', 'phone', 'description', 'join_date', 'state', 'city', 'admin', 'status')

    def __init__(self, *args, **kwargs):
        super(DesignerForm, self).__init__(*args, **kwargs)
        self.fields['state'] = forms.ChoiceField(
            choices=get_state()
        )
        self.fields['city'].queryset = City.objects.all()


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
    list_display = ("username", "email",  "status")
    list_filter = ("status", "join_date")
