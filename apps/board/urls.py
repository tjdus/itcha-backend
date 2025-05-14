from django.urls import path

from apps.board.views.application import ApplicationListView, ApplicationDetailView
from apps.board.views.recruitment import RecruitmentListView, RecruitmentDetailView

urlpatterns = [
    path('recruitments', RecruitmentListView.as_view(), name='recruitment-list'),
    path('recruitments/<int:pk>', RecruitmentDetailView.as_view(), name='recruitment-detail'),
    path('applications', ApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>', ApplicationDetailView.as_view(), name='application-detail'),
]