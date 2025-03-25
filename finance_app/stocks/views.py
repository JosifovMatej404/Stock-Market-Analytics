from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock, StockSignal,StockData

#Create your views here.


def landing_page(request):
    stocks = Stock.objects.all().order_by('symbol')

    # Calculate price change % from last two days
    top_gainers, top_losers = [], []

    for stock in stocks:
        data = StockData.objects.filter(stock=stock).order_by('-timestamp')[:2]
        if len(data) == 2:
            latest, previous = data[0], data[1]
            try:
                change_pct = ((latest.close - previous.close) / previous.close) * 100
                top_gainers.append((stock.symbol, change_pct))
                top_losers.append((stock.symbol, change_pct))
            except:
                continue

    top_gainers = sorted(top_gainers, key=lambda x: x[1], reverse=True)[:5]
    top_losers = sorted(top_losers, key=lambda x: x[1])[:5]

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

    context = {
        'stock': stock,
        'signal': signal,
    }

    return render(request, 'stocks/dashboard.html', context)
