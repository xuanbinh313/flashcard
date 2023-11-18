# Generated by Django 4.2.7 on 2023-11-17 07:05

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deck', '0002_remove_progress_card_progress_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='progress',
            name='deck',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deck.deck'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='status',
            field=models.CharField(blank=True, choices=[('e', 'Easy'), ('m', 'Medium'), ('h', 'Hard')], help_text='Progress availability', max_length=1),
        ),
    ]