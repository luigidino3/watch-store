# Generated by Django 2.0.2 on 2018-03-13 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_auto_20180313_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='creditinfo',
            name='user',
        ),
        migrations.AlterField(
            model_name='items',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='CreditInfo',
        ),
        migrations.AddField(
            model_name='review',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Items'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
    ]
