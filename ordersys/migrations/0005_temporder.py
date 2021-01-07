# Generated by Django 3.1.2 on 2021-01-07 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordersys', '0004_auto_20210105_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_of_product', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordersys.product')),
            ],
        ),
    ]
