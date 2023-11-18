import os
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from googletrans import Translator
from gtts import gTTS


class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=150, help_text='Name of deck')

    def get_absolute_url(self):
        return reverse('model-deck-view', args=[str(self.id)])

    def __str__(self):
        return self.name


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.RESTRICT)
    front_content = models.TextField(max_length=1000)
    back_content = models.TextField(max_length=1000, blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('model-card-view', args=[str(self.id)])

    def save(self, *args, **kwargs):
        should_have = not self.id
        if should_have:
            super().save(*args, **kwargs)
        # save audio
        tts = gTTS(self.front_content, lang='en')
        audio_path = f'audios/{self.id}.mp3'
        tts.save(os.path.join('media', audio_path))
        self.audio.name = audio_path
        # save text translate
        if not self.back_content:
            translator = Translator()
            result = translator.translate(
                self.front_content,
                src='en',
                dest='vi'
            )
            self.back_content = result.text
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.front_content} ({self.deck.name})"


class Progress(models.Model):
    deck = models.OneToOneField(Deck, on_delete=models.CASCADE)
    last_reviewed = models.DateTimeField(default=timezone.now)
    next_reviewed = models.DateTimeField(default=timezone.now)
    PROGRESS_STATUS = (
        ('e', 'Easy'),
        ('m', 'Medium'),
        ('h', 'Hard')
    )
    status = models.CharField(
        max_length=1,
        choices=PROGRESS_STATUS,
        blank=True,
        help_text='Progress availability'
    )

    class Meta:
        ordering = ['next_reviewed']

    def save(self,*args, **kwargs):
        if self.id:
            if self.status == 'e':
                self.next_reviewed = self.next_reviewed + timedelta(7)
            elif self.status == 'm':
                self.next_reviewed = self.next_reviewed + timedelta(3)
            else:
                self.next_reviewed = self.next_reviewed + timedelta(1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.deck.name}"

    def get_absolute_url(self):
        return reverse('model-progress-view', args=[str(self.id)])
