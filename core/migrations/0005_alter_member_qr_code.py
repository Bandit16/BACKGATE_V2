# Generated by Django 5.1.3 on 2025-06-06 20:13

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_member_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='qr_code',
            field=django_resized.forms.ResizedImageField(crop=None, default='qr.jpeg', force_format='JPEG', keep_meta=False, quality=95, scale=0.5, size=[1080, 1080], upload_to='qr_images/'),
        ),
    ]
