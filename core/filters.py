import django_filters
from .models import *

class PostFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(
        field_name='description', lookup_expr='icontains')

    class Meta:
        model = Posts
        fields = ['description']
