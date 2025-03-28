# Generated by Django 5.1.7 on 2025-03-25 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockSignal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('trend', models.CharField(max_length=20)),
                ('action', models.CharField(max_length=10)),
                ('predicted_price', models.FloatField(blank=True, null=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('stock', 'timestamp')},
            },
        ),
    ]
