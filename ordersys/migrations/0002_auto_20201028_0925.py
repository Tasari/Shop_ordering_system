# Generated by Django 3.1.2 on 2020-10-28 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordersys', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('INSERT INTO ordersys_order (id, status, date_ordered) VALUES (999, "Done", 1900-01-01)')
    ]

