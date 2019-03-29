from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, City, Country, Hotel,  Tour
from .models import Point
from django.views import generic
from cart.forms import CartAddProductForm

def MainPage(request):
    return render(request, 'catalog/base.html', )

# Страница с товарами
def ProductListCat(request, category_slug=None):
    print(category_slug)
    category = None
    tours = Tour.objects.all()
    points = Point.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        tours = Tour.objects.filter(TourCategory=category)
    return render(request, 'catalog/vitrina.html', {
        'points': points,
        'tours': tours,
        'category': category,

    })


# Страница отдельного товара
def ProductDetail(request, id, slug):
    tour = get_object_or_404(Tour, id=id, slug=slug)
    point = get_object_or_404(Point, PointTour=tour)

    cart_product_form = CartAddProductForm()
    return render(request, 'catalog/detail.html', {'tour': tour, 'point': point,
                                                   'cart_product_form': cart_product_form })

