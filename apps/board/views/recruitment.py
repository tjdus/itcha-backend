from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.board.filtersets.recruitment import RecruitmentFilter
from apps.board.models import Recruitment
from apps.board.serializers.recruitment import RecruitmentSerializer, RecruitmentCreateSerializer, \
    RecruitmentUpdateSerializer
from apps.core.common.pagination import BasePagination

class RecruitmentListView(APIView):
    filterset_class = RecruitmentFilter
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        'title', 'content'
    ]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = Recruitment.objects.prefetch_related('recruitment_field_set').select_related('created_by', 'updated_by').all()
        return queryset

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.
        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def paginate_queryset(self, queryset):
        paginator = self.pagination_class()
        return paginator.paginate_queryset(queryset, self.request), paginator

    def get(self, request):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        paginated_queryset, paginator = self.paginate_queryset(filtered_queryset)
        serializer = RecruitmentSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RecruitmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(created_by=request.user)
            return Response(RecruitmentSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecruitmentDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Recruitment, pk=pk)

    def get(self, request, pk):
        recruitment = self.get_object(pk)
        serializer = RecruitmentSerializer(recruitment)
        return Response(serializer.data)

    def patch(self, request, pk):
        recruitment = self.get_object(pk)
        serializer = RecruitmentUpdateSerializer(recruitment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recruitment = self.get_object(pk)
        recruitment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)