from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from .models import Product
from .serializers import ProductSerializer

class ProductFilter(FilterSet):
    min_price   = NumberFilter(field_name="price",   lookup_expr="gte")
    max_price   = NumberFilter(field_name="price",   lookup_expr="lte")
    min_rating  = NumberFilter(field_name="rating",  lookup_expr="gte")
    min_reviews = NumberFilter(field_name="reviews", lookup_expr="gte")

    class Meta:
        model = Product
        fields = ()

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields  = ("price", "rating", "reviews", "name")