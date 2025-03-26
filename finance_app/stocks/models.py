from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol


class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='data')
    timestamp = models.DateTimeField()  # <-- changed from DateField to DateTimeField
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('stock', 'timestamp')  # Only one record per symbol+timestamp

    def __str__(self):
        return f"{self.stock.symbol} at {self.timestamp}"


class StockSignal(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    trend = models.CharField(max_length=20)  # 'UP', 'DOWN', 'SIDEWAYS'
    action = models.CharField(max_length=10)  # 'BUY', 'SELL', 'HOLD'
    predicted_price = models.FloatField(null=True, blank=True)
    candle_chart_html = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('stock', 'timestamp')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.stock.symbol} - {self.trend} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
