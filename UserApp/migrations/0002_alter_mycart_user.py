# Generated by Django 4.1.2 on 2023-01-24 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0004_userinfor'),
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.userinfor'),
        ),
    ]
