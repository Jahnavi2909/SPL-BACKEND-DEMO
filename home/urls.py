from django.urls import path
from .views import RecentActivitiesAPIView
from .views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),


    path('admin/recent-activities/', RecentActivitiesAPIView.as_view()),

]
