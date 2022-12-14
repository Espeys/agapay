# Generated by Django 3.0.5 on 2021-06-24 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20210623_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_readed',
        ),
        migrations.AddField(
            model_name='message',
            name='seen_by',
            field=models.ManyToManyField(blank=True, related_name='seen_by', to='account.Profile'),
        ),
        migrations.AddField(
            model_name='notification',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifactor', to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_creator', to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notified_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifactee', to='account.Profile'),
        ),
    ]
