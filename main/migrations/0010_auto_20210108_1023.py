# Generated by Django 3.0.5 on 2021-01-08 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_merge_20210108_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_X', models.FloatField()),
                ('pos_Y', models.FloatField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('design_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Design')),
                ('pdt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Product')),
            ],
        ),
    ]
