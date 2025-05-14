from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.board.filtersets.application import ApplicationFilter
from apps.board.models import Application
from apps.board.serializers.application import ApplicationDetailSerializer, ApplicationSerializer
from apps.core.common.pagination import BasePagination

class ApplicationListView(APIView):
    filterset_class = ApplicationFilter
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        'title', 'content'
    ]
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = Application.objects.prefetch_related('application_field_set').select_related('created_by', 'updated_by').all()
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
        serializer = ApplicationDetailSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(ApplicationDetailSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Application, pk=pk)

    def get(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationDetailSerializer(application)
        return Response(serializer.data)

    def patch(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application, data=request.data, partial=True)

        if serializer.is_valid():
            instance = serializer.save(updated_by=request.user)
            return Response(ApplicationDetailSerializer(instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        application = self.get_object(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)