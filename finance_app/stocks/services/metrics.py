from stocks.models import Stock, StockData

def get_top_movers(limit=5):
    top_gainers = []
    top_losers = []

    stocks = Stock.objects.all()

    for stock in stocks:
        recent = StockData.objects.filter(stock=stock).order_by('-timestamp')[:2]
        if len(recent) < 2:
            continue

        today, yesterday = recent[0], recent[1]

        try:
            if yesterday.close == 0:
                continue
            change_pct = ((today.close - yesterday.close) / yesterday.close) * 100
            top_gainers.append((stock.symbol, change_pct))
            top_losers.append((stock.symbol, change_pct))
        except:
            continue

    # Sort and limit
    top_gainers = sorted(top_gainers, key=lambda x: x[1], reverse=True)[:limit]
    top_losers = sorted(top_losers, key=lambda x: x[1])[:limit]

    return top_gainers, top_losers
