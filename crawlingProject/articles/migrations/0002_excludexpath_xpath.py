# Generated by Django 4.0.3 on 2023-01-22 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='excludeXpath',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=20, null=True)),
                ('exclude_element_xpath', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'exclude_element_tbl',
            },
        ),
        migrations.CreateModel(
            name='Xpath',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=20, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('body', models.CharField(max_length=200, null=True)),
                ('attachment_list', models.CharField(max_length=200, null=True)),
                ('published_datetime', models.CharField(max_length=200, null=True)),
                ('time_zone', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'xpath_tbl',
            },
        ),
    ]
