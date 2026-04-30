from django.urls import path
from .views import FranchiseDashboardAPIView,FranchiseTeamPerformanceAPIView

urlpatterns = [
    path('franchise/dashboard/', FranchiseDashboardAPIView.as_view()),
    path('franchise/team-performance/', FranchiseTeamPerformanceAPIView.as_view()),
]