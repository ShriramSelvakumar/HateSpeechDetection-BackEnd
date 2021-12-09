from .views import user_mentions_2, export_tweets, block_users_json, new_user, mute_users_json, search_tweets
from django.urls import path, include

urlpatterns = [
    path('mentions_2/', user_mentions_2),
    path('search_tweets/', search_tweets),
    path('export_tweets/', export_tweets),
    path('block_users_json/', block_users_json),
    path('mute_users_json/', mute_users_json),
    path('new_user/', new_user),
]
