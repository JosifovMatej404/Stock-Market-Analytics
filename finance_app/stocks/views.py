from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock, StockSignal,StockData
from stocks.services.metrics import get_top_movers
from stocks.services.visualization import plot_candlestick_chart
from django.views.decorators.csrf import csrf_exempt
from stocks.tasks import analyze_stock_task





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
    candle_chart = plot_candlestick_chart(symbol)

    return render(request, 'stocks/dashboard.html', {
        "stock": stock,
        "signal": signal,
        "candle_chart": candle_chart,
    })


@csrf_exempt
def regenerate_prediction(request, symbol):
    if request.method == 'POST':
        stock = get_object_or_404(Stock, symbol=symbol)
        analyze_stock_task.delay(symbol)  # 🚀 Async call to regenerate prediction
        return redirect('company_dashboard', symbol=symbol)