# community/board/filters.py

from django_filters import rest_framework as filters
from .models import Facility

class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    region = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    sport = filters.CharFilter(lookup_expr='icontains')
    target = filters.CharFilter(lookup_expr='icontains')
    period = filters.CharFilter(lookup_expr='icontains')
    day = filters.CharFilter(lookup_expr='icontains')
    time = filters.CharFilter(lookup_expr='icontains')
    fee = filters.NumberFilter()
    capacity = filters.NumberFilter()

    class Meta:
        model = Facility
        fields = ['name', 'region', 'location', 'sport', 'target', 'period', 'day', 'time', 'fee', 'capacity']
