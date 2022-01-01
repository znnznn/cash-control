# Generated by Django 2.2.16 on 2022-01-01 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easycontrol', '0007_auto_20211113_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='debit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]
