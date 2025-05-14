from django.urls import path

from apps.board.views.recruitment import RecruitmentListView, RecruitmentDetailView

urlpatterns = [
    path('recruitments', RecruitmentListView.as_view(), name='recruitment-list'),
    path('recruitments/<int:pk>/', RecruitmentDetailView.as_view(), name='recruitment-detail'),
]