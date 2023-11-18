from django.urls import path
from .views import index, DeckListView, deckDetail,play_audio

urlpatterns = [
    path('', index, name='index'),
    path('decks/', DeckListView.as_view(), name='deck_list'),
    path('decks/<int:id>/', deckDetail, name='deck_detail'),
    path('play_audio/<int:card_id>/', play_audio, name='play_audio')
]
