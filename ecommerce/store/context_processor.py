from .models import Brand,Variation, Product
from django.db.models import Min, Max

def brand_links(request):
    brands = Brand.objects.all()
    return dict(brand_links = brands)

def get_filters(request):
    cats = Product.objects.distinct().values('category__category_name', 'category__id')
    brands = Product.objects.distinct().values('brand__brand_name', 'brand__id')
    # colors = Variation.objects.filter(variation_category='color').values_list('variation_value', flat=True).distinct()
    # sizes = Variation.objects.filter(variation_category='size').values_list('variation_value', flat=True).distinct()
    minMaxPrice = Product.objects.aggregate(Min('price'), Max('price'))


    context = {
        'cats':cats,
        'brands':brands,
        # 'colors': colors,
        # 'sizes': sizes,
        'minMaxPrice':minMaxPrice
    }

    return context