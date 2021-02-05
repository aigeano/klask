from django.db import models
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class BaseModel(TimeStampedModel):
    """
    Base Model
    """

    class Meta:
        abstract = True
        app_label = 'tournament'


class Player(BaseModel):
    name = models.CharField(_('Name'), max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name


class Tournament(BaseModel):
    players = models.ManytoMany(Player, blank=True, null=True)
    bracket = models.CharField(max_length=1096, null=True, blank=True)
    winners = models.ManytoMany(Player, blank=True, null=True)


class Game(BaseModel):
    first_player = models.ForeignKey(Player)
    second_player = models.ForeignKey(Player)
    winner = models.models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_won')


class Match(BaseModel):
    first_game = models.OneToOneField(Game)
    second_game = models.OneToOneField(Game)
    third_game = models.OneToOneField(Game, null=True, blank=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_won')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
