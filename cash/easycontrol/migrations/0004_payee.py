# Generated by Django 3.1.3 on 2021-10-13 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('easycontrol', '0003_transaction_date_of_close'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_payee', models.EmailField(max_length=254, verbose_name='email address')),
                ('code', models.IntegerField()),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('confirmed_date', models.DateField()),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
