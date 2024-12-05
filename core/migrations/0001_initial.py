# Generated by Django 5.1.3 on 2024-12-03 10:59

import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.IntegerField(default=2078)),
                ('faculty', models.CharField(choices=[('BCT', 'BCT'), ('BME', 'BME'), ('BCE', 'BCE'), ('BAG', 'BAG')], default='BME', max_length=200)),
                ('profile_pic', django_resized.forms.ResizedImageField(crop=['middle', 'center'], default='default.webp', force_format='JPEG', keep_meta=False, quality=95, scale=0.5, size=[1080, 1080], upload_to='customer_images/')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=200)),
                ('post_picture', models.ImageField(blank=True, default='', null=True, upload_to='chat_images/')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.member')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('post_picture', models.ImageField(blank=True, default='', null=True, upload_to='post_images/')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.member')),
            ],
        ),
    ]
