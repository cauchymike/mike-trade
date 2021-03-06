# Generated by Django 3.2.8 on 2021-11-20 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eccomerce', '0008_rename_productid_orders_productsid'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyersInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('buyersID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eccomerce.buyers')),
                ('productsID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eccomerce.products')),
            ],
        ),
    ]
