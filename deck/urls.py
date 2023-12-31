from django.urls import path
from .views import index, DeckListView, deckDetail, play_audio, next_reviewed

urlpatterns = [
    path('dashboard/', index, name='index'),
    path('', DeckListView.as_view(), name='deck_list'),
    path('/<int:id>/', deckDetail, name='deck_detail'),
    path('play_audio/<int:card_id>/', play_audio, name='play_audio'),
    path('next_reviewed/<str:deck_id>/<str:status>/', next_reviewed, name='next_reviewed')
]
