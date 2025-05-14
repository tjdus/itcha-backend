import django_filters

from apps.board.models import Recruitment


class RecruitmentFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(
        lookup_expr='icontains',
    )
    deadline_before = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='lte',
                                                    label='Deadline before')
    deadline_after = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='gte',
                                                   label='Deadline after')

    is_completed = django_filters.BooleanFilter(label='Is completed')

    class Meta:
        model = Recruitment
        fields = ['type', 'deadline_before', 'deadline_after', 'is_completed']