# Generated by Django 3.0.5 on 2021-06-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_postitem_geo_full_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='postitem',
            name='help_type',
            field=models.CharField(blank=True, choices=[('services', 'services'), ('help', 'time'), ('goods', 'goods'), ('information', 'information'), ('others', 'others')], max_length=255, null=True),
        ),
    ]
