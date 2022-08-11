# Generated by Django 3.0.5 on 2021-05-28 15:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=40)),
                ('text', models.CharField(default='active', max_length=50)),
                ('state', models.CharField(db_index=True, default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='postitem',
            name='tags',
            field=models.ManyToManyField(blank=True, to='post.PostTag'),
        ),
    ]
