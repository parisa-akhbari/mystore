# Generated by Django 5.1.2 on 2025-01-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newpayment', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'در انتظار پرداخت'), ('Processing', 'در حال پردازش'), ('Shipped', 'ارسال شده به پست'), ('Delivered', 'تحویل داده شده')], default='Pending', max_length=50),
        ),
    ]
