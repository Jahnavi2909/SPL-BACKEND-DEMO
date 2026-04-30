from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    #path('login/', TokenObtainPairView.as_view()),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    path('create-franchise/', CreateFranchiseView.as_view()),
     # PUBLIC
    path('franchises/', FranchiseListView.as_view()),
    path('franchises/<int:pk>/', FranchiseDetailView.as_view()),
    # ADMIN ONLY
    path('franchise/update/<int:pk>/', FranchiseUpdateView.as_view()),
    path('franchise/delete/<int:pk>/', FranchiseDeleteView.as_view()), 
    path('franchises/<int:pk>/teams/', FranchiseTeamsView.as_view()),

]

