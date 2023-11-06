from .models import Brand,Variation


def brand_links(request):
    brands = Brand.objects.all()
    return dict(brand_links = brands)