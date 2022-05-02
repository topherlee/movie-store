from .views import basket

def sections_processor(request):
    baskets = basket.Basket(request)
    total_item = len(baskets)
    total_price = basket.Basket.get_total_price(baskets)
    return {
        'total_item':total_item,
        'total_price':total_price,
    }