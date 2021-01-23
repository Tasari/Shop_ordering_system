# Generated by Django 3.1.2 on 2021-01-21 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordersys', '0005_temporder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('position', models.CharField(max_length=32)),
                ('employment_date', models.DateField()),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('minimum_salary', models.DecimalField(decimal_places=2, max_digits=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
