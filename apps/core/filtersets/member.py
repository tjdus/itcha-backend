import django_filters

from apps.core.models import User


class MemberFilter(django_filters.FilterSet):
    member = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ["member", 'name', 'email']