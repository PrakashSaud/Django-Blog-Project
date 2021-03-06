# Generated by Django 4.0.4 on 2022-05-12 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField()),
                ('reporter', models.ManyToManyField(related_name='author', to='article.author')),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
    ]
