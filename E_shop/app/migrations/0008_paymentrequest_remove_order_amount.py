# Generated by Django 4.1.3 on 2023-05-16 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_order_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('product', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pin', models.CharField(max_length=4)),
                ('is_confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='amount',
        ),
    ]
