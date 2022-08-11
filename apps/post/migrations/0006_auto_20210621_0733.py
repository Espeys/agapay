# Generated by Django 3.0.5 on 2021-06-21 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20210621_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postitem',
            name='item_type',
            field=models.CharField(blank=True, choices=[('promotion', 'promotion'), ('status', 'status'), ('diary', 'diary'), ('request', 'request'), ('offer', 'offer')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='postitem',
            name='mood_type',
            field=models.CharField(blank=True, choices=[('angry', 'angry'), ('sad', 'sad'), ('meh', 'meh'), ('satisfied', 'satisfied'), ('happy', 'happy')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='postitem',
            name='promotion_type',
            field=models.CharField(blank=True, choices=[('campaign', 'campaign'), ('event', 'event'), ('hotline', 'hotline'), ('service', 'service'), ('group', 'group'), ('initiative', 'initiative'), ('article', 'article'), ('ads', 'ads'), ('other', 'other')], max_length=255, null=True),
        ),
    ]