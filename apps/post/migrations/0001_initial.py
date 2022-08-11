# Generated by Django 3.0.5 on 2021-05-23 05:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=40)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('mood', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('weblink', models.URLField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=50, null=True)),
                ('tel_no', models.CharField(blank=True, max_length=50, null=True)),
                ('visibility_type', models.CharField(blank=True, choices=[('Public', 'Public'), ('Private', 'Private')], max_length=255, null=True)),
                ('item_type', models.CharField(blank=True, choices=[('Campaign', 'Campaign'), ('Diary', 'Diary'), ('Hotline', 'Hotline'), ('Event', 'Event'), ('Service', 'Services'), ('Support', 'Support-Groups'), ('Initiative', 'Initiative'), ('Share', 'Share'), ('Mood', 'Mood'), ('None', 'None')], max_length=255, null=True)),
                ('censorship', models.BooleanField(default=False)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('sched_start', models.DateTimeField(blank=True, null=True)),
                ('sched_end', models.DateTimeField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('state', models.CharField(db_index=True, default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to='account.Profile')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to='account.Profile')),
                ('shared_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='post.PostItem')),
            ],
        ),
        migrations.CreateModel(
            name='PostReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('state', models.CharField(db_index=True, default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.PostItem')),
                ('reported_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('state', models.CharField(db_index=True, default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.PostItem')),
            ],
        ),
        migrations.CreateModel(
            name='PostAuditTrail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=40)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('from_attrs', models.TextField(blank=True, null=True)),
                ('to_attrs', models.TextField(blank=True, null=True)),
                ('state', models.CharField(db_index=True, default='active', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.PostItem')),
            ],
        ),
    ]
