# Generated by Django 3.0.5 on 2021-06-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_postreport_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcommentreport',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
