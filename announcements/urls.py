from django.urls import path
from .views import *
 
urlpatterns = [
    path('announcements/', AnnouncementListCreateView.as_view()),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view()),
 
    path('news/', NewsListCreateView.as_view()),
    path('news/<int:pk>/', NewsDetailView.as_view()),
]