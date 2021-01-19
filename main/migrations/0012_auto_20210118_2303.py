# Generated by Django 3.0.5 on 2021-01-18 17:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210111_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateField(default=datetime.date.today)),
                ('status', models.IntegerField(default=0)),
                ('addr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('payment_method', models.CharField(max_length=50)),
                ('datetime', models.DateField(default=datetime.date.today)),
                ('status', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemPdt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Design')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
            ],
        ),
    ]
