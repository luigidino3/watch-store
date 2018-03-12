# Generated by Django 2.0.2 on 2018-03-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='itemtype',
            field=models.CharField(choices=[('Analog', 'Analog'), ('Smart', 'Smart'), ('Digital', 'Digital')], default='Analog', max_length=25),
        ),
        migrations.AddField(
            model_name='items',
            name='quantity',
            field=models.IntegerField(default=20),
        ),
    ]
