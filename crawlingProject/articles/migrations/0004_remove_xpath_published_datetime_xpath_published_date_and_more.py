# Generated by Django 4.0.3 on 2023-01-23 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_xpath_link_liet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xpath',
            name='published_datetime',
        ),
        migrations.AddField(
            model_name='xpath',
            name='published_date',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='attachment_list',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='body',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='link_liet',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='site_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='time_zone',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='xpath',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
