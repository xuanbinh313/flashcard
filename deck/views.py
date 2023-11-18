from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Deck, Card


def index(request):
    num_card = Card.objects.count()
    num_deck = Deck.objects.count()
    context = {
        'num_card': num_card,
        'num_deck': num_deck
    }
    return render(request, 'index.html', context)


class DeckListView(ListView):
    model = Deck
    context_object_name = 'decks'
    template_name = 'deck_list.html'

    def get_queryset(self):
        return Deck.objects.all()


def deckDetail(request, id):
    deck = get_object_or_404(Deck, id=id)
    card_list = Card.objects.filter(deck=deck)
    context = {
        'deck': deck,
        'cards': card_list
    }
    return render(request, 'deck_detail.html', context)


def play_audio(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    audio_file = card.audio.path
    return FileResponse(open(audio_file, 'rb'), content_type='audio/mpeg')
