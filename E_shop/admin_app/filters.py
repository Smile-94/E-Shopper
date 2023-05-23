import django_filters
from django import forms


from app.models import Order



class OrderFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='ordered_at', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='From')
    to_date = django_filters.DateFilter(field_name='ordered_at', lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), label='To')

    class Meta:
        model = Order
        fields = ['ordered_at']