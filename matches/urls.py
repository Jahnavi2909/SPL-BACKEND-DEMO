
 
from django.urls import path, include
from rest_framework.routers import DefaultRouter
 
from .views import (
    MatchListView,
    MatchDetailView,
    MatchUpdateView,
    PlayingXIViewSet,
    PointsTableViewSet,
    PlayerStatsViewSet,
    TopPerformerCardAPIView
   
)
 
router = DefaultRouter()
router.register(r'playing-xi', PlayingXIViewSet, basename='playing-xi')
router.register(r'points-table', PointsTableViewSet, basename='points-table')
router.register(r'player-stats', PlayerStatsViewSet, basename='player-stats')
 
urlpatterns = [
    # GET all matches
    path('matches/', MatchListView.as_view(), name='match-list'),
 
    # GET single match by id
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
 
    # Admin edit specific match
    path('matches/update/<int:pk>/', MatchUpdateView.as_view(), name='match-update'),
 
    # APIView
    path(
        'top-performer-card/',
        TopPerformerCardAPIView.as_view(),
        name='top-performer-card'
    ),
 
    # ViewSets
    path('', include(router.urls)),
]
 
 
