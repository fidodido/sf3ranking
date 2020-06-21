from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')


class Country(models.Model):
    name = models.CharField(max_length=255)
    url_image = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    url_image = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Char(models.Model):
    name = models.CharField(max_length=255)
    url_image = models.CharField(max_length=255, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class League(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_by',)
    title = models.CharField(max_length=255, unique=True, validators=[alphanumeric])
    slug = models.SlugField(unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=1)

    def results(self):
        return Result.objects.filter(league=self).count()

    def __str__(self):
        return self.title


class MatchType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def is_tournament(self):

        if self.id is 1:
            return True
        else:
            return False

    def __str__(self):
        return self.name


class Player(models.Model):
    nickname = models.CharField(max_length=255)
    ranking = models.FloatField(default=0)
    main = models.ForeignKey(Char, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE, default=1)
    disabled = models.BooleanField(default=False)
    country = models.ForeignKey(Country, default=1, on_delete=models.CASCADE)

    def victories(self):
        return Result.objects.filter(victory_player=self).count()

    def loses(self):
        return Result.objects.filter(loser_player=self).count()

    def played(self):
        return self.loses() + self.victories()

    def champions(self):
        return Tournament.objects.filter(champion=self).count()        

    def __str__(self):
        return self.nickname

    class Meta:
        unique_together = ('nickname', 'league',)

class Tournament(models.Model):
    name = models.CharField(max_length=255, unique=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, default=1)
    champion = models.ForeignKey(Player, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class MedalType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Medal(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default=1)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mtype = models.ForeignKey(MedalType, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('tournament', 'player', 'mtype', )

class Result(models.Model):

    mtype = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    challenging = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="challenging")
    rival = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="rival")
    victory_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="victory_player", null=True,
                                       blank=True)
    loser_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="loser_player", null=True,
                                     blank=True)
    challenging_score = models.IntegerField(default=0)
    rival_score = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    replay_url = models.CharField(max_length=2000, null=True, blank=True)
    ranking_del_challenging = models.FloatField(default=0)
    ranking_del_rival = models.FloatField(default=0)
    league = models.ForeignKey(League, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.challenging.nickname + ' ' + ' v/s ' + self.rival.nickname
