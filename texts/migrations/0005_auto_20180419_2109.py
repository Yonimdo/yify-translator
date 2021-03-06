# Generated by Django 2.0 on 2018-04-19 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0004_suggestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmartText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('text', models.TextField()),
                ('language', models.TextField(max_length=2)),
            ],
        ),
        migrations.AddIndex(
            model_name='originaltext',
            index=models.Index(fields=['original'], name='raw_original_idx'),
        ),
        migrations.AddField(
            model_name='smarttext',
            name='text_origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='texts.LenguaText'),
        ),
        migrations.AddIndex(
            model_name='smarttext',
            index=models.Index(fields=['text'], name='raw_text_idx'),
        ),
    ]
