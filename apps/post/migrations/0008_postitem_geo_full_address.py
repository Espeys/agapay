# Generated by Django 3.0.5 on 2021-06-22 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_postcomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='postitem',
            name='geo_full_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
