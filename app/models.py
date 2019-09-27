from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.title


class Char(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url_image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class MatchType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    url_image = models.CharField(max_length=1000, null=True, blank=True)
    mail = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    fecha_nac = models.DateField()
    ranking = models.FloatField(default=0)
    main = models.ForeignKey(Char, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nickname

class Tournament(models.Model):
    name = models.CharField(max_length=255, unique=True)
    online = models.BooleanField(default=1)

    def __str__(self):
        return self.name

class Result(models.Model):
    mtype = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    challenging = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="challenging")
    rival = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="rival")
    victory_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="victory_player", null=True, blank=True)
    loser_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="loser_player", null=True, blank=True)
    challenging_score = models.IntegerField(default=0)
    rival_score = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    replay_url = models.CharField(max_length=2000, null=True, blank=True)
    ranking_del = models.FloatField(default=0)

    def __str__(self):
        return self.challenging.nickname + ' ' + ' v/s ' + self.rival.nickname

