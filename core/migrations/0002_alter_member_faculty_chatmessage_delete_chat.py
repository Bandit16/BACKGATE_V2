# Generated by Django 5.1.3 on 2025-02-10 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='faculty',
            field=models.CharField(choices=[('BCT', 'BCT'), ('BME', 'BME'), ('BCE', 'BCE'), ('BAG', 'BAG'), ('BARCH', 'BARCH'), ('CA', 'CA')], default='BME', max_length=200),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='chat_files/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.member')),
            ],
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
    ]
