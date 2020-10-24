# Generated by Django 3.1.2 on 2020-10-22 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, null=True)),
                ('author', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, null=True)),
                ('phone_no', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_librarian', models.BooleanField(default=False)),
                ('designation', models.CharField(max_length=1000, null=True)),
                ('curr_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='type_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField()),
                ('book_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.book')),
                ('customer_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_order', to='main.customer')),
            ],
        ),
    ]
