# Generated by Django 3.1.3 on 2021-10-14 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('easycontrol', '0005_auto_20211014_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(blank=True, null=True, upload_to='uploads/report')),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easycontrol.transaction')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
