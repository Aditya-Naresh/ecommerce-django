from .models import Brand


def brand_links(request):
    brands = Brand.objects.all()
    return dict(brand_links = brands)