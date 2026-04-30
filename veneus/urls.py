from django.urls import path
from .views import VenueListCreateView, VenueDetailView,SponsorListCreateView, SponsorDetailView
 
urlpatterns = [
    path('venues/', VenueListCreateView.as_view()),
    path('venues/<int:pk>/', VenueDetailView.as_view()),
    path('sponsors/', SponsorListCreateView.as_view()),
    path('sponsors/<int:pk>/', SponsorDetailView.as_view()),
]