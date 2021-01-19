import datetime

from django.contrib.auth.models import User as admin
from django.utils.safestring import mark_safe
from djongo import models


# Create your models here.
class State(models.Model):
    state_name = models.CharField(max_length=50)

    def __str__(self):
        return self.state_name


class City(models.Model):
    city_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class Designer(models.Model):
    designer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=100)
    description = models.TextField()
    join_date = models.DateField()
    status = models.BooleanField(default=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    admin = models.ForeignKey(admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.designer_name


class Customer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    join_date = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    join_date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    addr = models.TextField(verbose_name="Address")
    pincode = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.addr


class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    addr = models.TextField(verbose_name="Address")
    created_at = models.DateField(default=datetime.date.today)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    admin = models.ForeignKey(admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch_name


class Category(models.Model):
    cat_name = models.CharField(max_length=100, verbose_name="Category Name")

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    pdt_name = models.CharField(max_length=100, verbose_name="Product Name")
    description = models.TextField()
    image = models.ImageField(upload_to='img')
    price = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateField(default=datetime.date.today)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def prodImg(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))

    prodImg.short_description = "Image"
    prodImg.allow_tags = True

    def __str__(self):
        return self.pdt_name


class Design(models.Model):
    ins_choice = (
        (1, "Admin"),
        (2, "Designer")
    )
    design_name = models.CharField(max_length=100, verbose_name="Design Name")
    description = models.TextField()
    image = models.ImageField(upload_to='img')
    status = models.BooleanField(default=True)
    inserted_by = models.PositiveIntegerField(choices=ins_choice, default=1)
    creator_id = models.IntegerField(verbose_name="Creator Name")
    created_at = models.DateField(default=datetime.date.today)

    def prodImg(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))

    prodImg.short_description = "Image"
    prodImg.allow_tags = True

    def __str__(self):
        return self.design_name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class DesignElement(models.Model):
    pos_X = models.FloatField()
    pos_Y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    pdt_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    design_id = models.ForeignKey(Design, on_delete=models.CASCADE)

    def __str__(self):
        return self.design_id.design_name


class Cart(models.Model):
    qty = models.IntegerField()
    datetime = models.DateField(default=datetime.date.today)
    type = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.pdt_name


class Order(models.Model):
    datetime = models.DateField(default=datetime.date.today)
    status = models.IntegerField(default=0)
    addr = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItemPdt(models.Model):
    qty = models.IntegerField()
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class OrderItemDesign(models.Model):
    price = models.FloatField()
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Payment(models.Model):
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    datetime = models.DateField(default=datetime.date.today)
    status = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
