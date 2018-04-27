# Generated by Django 2.0 on 2018-04-27 13:22

import uuid

import django.db.models.deletion
import django.db.models.functions.base
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.TimeField(auto_created=True, default=django.db.models.functions.base.Now)),
                ('func_name', models.TextField()),
                ('request', models.TextField()),
                ('response', models.TextField()),
                ('error_message', models.TextField()),
                ('passed', models.BooleanField(default=False)),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.TimeField(auto_created=True, default=django.db.models.functions.base.Now)),
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4)),
                ('request', models.TextField()),
                ('request_body', models.TextField()),
                ('response', models.TextField()),
                ('error_message', models.TextField()),
                ('passed', models.BooleanField(default=False)),
                ('note', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='audit',
            name='log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dauditlog.Log'),
        ),
    ]
