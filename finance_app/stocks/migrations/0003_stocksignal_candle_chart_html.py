# Generated by Django 5.1.7 on 2025-03-26 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stocksignal'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocksignal',
            name='candle_chart_html',
            field=models.TextField(blank=True, null=True),
        ),
    ]
