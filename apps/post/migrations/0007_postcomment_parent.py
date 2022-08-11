# Generated by Django 3.0.5 on 2021-06-21 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20210621_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='post.PostComment'),
        ),
    ]