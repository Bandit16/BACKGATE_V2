# Generated by Django 5.1.3 on 2025-05-15 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_posts_post_video_alter_posts_post_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('members', models.ManyToManyField(to='core.member')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultLiability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='rent', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('due_date', models.DateField()),
                ('user', models.ForeignKey(limit_choices_to={'membergroup__isnull': False}, on_delete=django.db.models.deletion.PROTECT, to='core.member')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.membergroup')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(default='khaja kharcha', max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='transactions.membergroup')),
                ('initiated_by', models.ForeignKey(limit_choices_to={'membergroup__isnull': False}, on_delete=django.db.models.deletion.PROTECT, related_name='initiated_transactions', to='core.member')),
                ('involved_members', models.ManyToManyField(limit_choices_to={'membergroup__isnull': False}, related_name='involved_transactions', to='core.member')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paid_transactions', to='core.member')),
            ],
        ),
    ]
