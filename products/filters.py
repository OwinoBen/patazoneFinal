from .models import Product
import django_filters
from django_filters.filters import RangeFilter


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price = RangeFilter()

    class Meta:
        model = Product
        fields = ['title', 'price']
