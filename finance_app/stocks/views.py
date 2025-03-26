from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock, StockSignal,StockData
from stocks.services.metrics import get_top_movers
from stocks.services.visualization import plot_candlestick_chart
from django.views.decorators.csrf import csrf_exempt
from stocks.tasks import analyze_stock_task
from stocks.tasks import plot_candlestick_chart_task
from stocks.services.analysis import analyze_stock



def landing_page(request):
    stocks = Stock.objects.all().order_by('symbol')
    top_gainers, top_losers = get_top_movers()

    if request.method == 'POST':
        selected_symbol = request.POST.get('symbol')
        return redirect('company_dashboard', symbol=selected_symbol)

    return render(request, 'stocks/landing.html', {
        'stocks': stocks,
        'top_gainers': top_gainers,
        'top_losers': top_losers,
    })




def company_dashboard(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    signal = StockSignal.objects.filter(stock=stock).first()
    candle_chart = signal.candle_chart_html if signal else None


    trend_color = {
        "UP": "#27ae60",
        "DOWN": "#c0392b",
        "SIDEWAYS": "#7f8c8d"
    }.get(signal.trend if signal else "", "#bdc3c7")

    action_color = {
        "BUY": "#2ecc71",
        "SELL": "#e74c3c",
        "HOLD": "#95a5a6"
    }.get(signal.action if signal else "", "#bdc3c7")

    return render(request, 'stocks/dashboard.html', {
        "stock": stock,
        "signal": signal,
        "candle_chart": candle_chart,
        "trend_color": trend_color,
        "action_color": action_color,
    })



