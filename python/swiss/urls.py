from django.urls import path

from . import views

urlpatterns = [
    path('api/leagues', views.v_leagues, name='leagues'),
    path('api/league', views.v_league, name='league'),
    path('api/league/<int:league_id>', views.v_a_league, name='a_league'),
    path('api/league/<int:league_id>/players', views.v_players, name='players'),
    path('api/league/<int:league_id>/player', views.v_player, name='player'),
    path('api/league/<int:league_id>/player/<int:player_id>', views.v_a_player, name='a_player'),
    path('api/league/<int:league_id>/rounds', views.v_rounds, name='rounds'),
    path('api/league/<int:league_id>/round', views.v_round, name='round'),
    path('api/league/<int:league_id>/round/<int:round_id>', views.v_a_round, name='a_round'),
    path('api/league/<int:league_id>/round/<int:round_id>/matches', views.v_matches, name='matches'),
    path('api/league/<int:league_id>/round/<int:round_id>/match/<int:match_id>', views.v_a_match, name='a_match'),
]