import datetime
from django.utils import timezone
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Deck, Card, Progress


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming today is the current date
        today = timezone.now().date()
        # Get the decks with Progress.next_reviewed equal to today
        decks_with_today_review = Deck.objects.filter(
            progress__next_reviewed__date__lte=today)
        decks_with_future_review = Deck.objects.filter(
            progress__next_reviewed__date__gt=today)
        context = {
            'today': decks_with_today_review,
            'nextday': decks_with_future_review
        }
        return context


def deckDetail(request, id):
    deck = get_object_or_404(Deck, id=id)
    card_list = Card.objects.filter(deck=deck)
    context = {
        'deck': deck,
        'cards': card_list
    }
    return render(request, 'deck_detail.html', context)


def play_audio(_, card_id):
    card = get_object_or_404(Card, pk=card_id)
    audio_file = card.audio.path
    return FileResponse(open(audio_file, 'rb'), content_type='audio/mpeg')


def next_reviewed(request, deck_id, status):
    deck = get_object_or_404(Deck, pk=deck_id)
    progress = get_object_or_404(Progress, deck=deck)
    progress.status = status
    progress.save()
    return JsonResponse({'message': 'update successful'})
