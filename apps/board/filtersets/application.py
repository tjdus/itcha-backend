import django_filters

from apps.board.models import   Application


class ApplicationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(
        lookup_expr='icontains',
    )

    class Meta:
        model = Application
        fields = ['status']