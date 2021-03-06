# Generated by Django 2.2.7 on 2020-03-29 23:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import eduline.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='No information available about this author')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('quantity_total', models.IntegerField(default=0)),
                ('quantity_collected', models.IntegerField(default=0)),
                ('quantity_reserved', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, default='book.gif', upload_to=eduline.models.get_upload_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduline.Author')),
            ],
            options={
                'ordering': ['quantity_collected', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(max_length=20)),
                ('program', models.CharField(max_length=100)),
                ('outstanding_fine', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['matric_number'],
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved', models.BooleanField(default=False)),
                ('collected', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('reserved_date', models.DateTimeField(blank=True, null=True)),
                ('collected_date', models.DateTimeField(blank=True, null=True)),
                ('returned_date', models.DateTimeField(blank=True, null=True)),
                ('fine', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduline.Book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eduline.Student')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(to='eduline.Category'),
        ),
    ]
