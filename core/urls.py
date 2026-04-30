from django.urls import path
from .views import *

urlpatterns = [
    path('team/create/', CreateTeamView.as_view()),
    path('team/approve/<int:pk>/', ApproveTeamView.as_view()),
    path('teams-get/',teamListView.as_view()),
    path('player/create/', CreatePlayerView.as_view()),

     # PUBLIC GET
    path('teams/', TeamListView.as_view()),
    path('teams/<int:pk>/', TeamDetailView.as_view()),
    path('players/', PlayerListView.as_view()),
    path('players/<int:pk>/', PlayerDetailView.as_view()),
   

    # UPDATE / DELETE
    path('team/update/<int:pk>/', TeamUpdateView.as_view()),
    path('team/delete/<int:pk>/', TeamDeleteView.as_view()),
    path('player/update/<int:pk>/', PlayerUpdateView.as_view()),
    path('player/delete/<int:pk>/', PlayerDeleteView.as_view()),

    #search by name
   path('teams/<int:pk>/players/', TeamPlayersView.as_view()),
   path(
        'franchises/<int:franchise_id>/teams/<int:team_id>/',
        FranchiseTeamDetailAPIView.as_view(),
        name='franchise-team-detail'
    ),
    path(
    'franchises/<int:franchise_id>/teams/<int:team_id>/players/<int:player_id>/',
    FranchiseTeamPlayerFullAPIView.as_view(),
    ),
    path("player/<int:pk>/", PlayerFullDetailAPIView.as_view()),

]