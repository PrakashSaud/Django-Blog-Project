# Generated by Django 4.0.4 on 2022-04-30 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_alter_blogs_date_updated_alter_comments_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='date_updated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date_updated'),
        ),
    ]
