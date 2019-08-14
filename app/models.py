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
    ranking = models.IntegerField(default=0)
    main = models.ForeignKey(Char, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nickname

class Tournament(models.Model):
    name = models.CharField(max_length=255, unique=True)
    online = models.BooleanField(default=1)

    def __str__(self):
        return self.name

class Results(models.Model):
    mtype = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    online = models.BooleanField(default=0)
    challenging = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="challenging")
    rival = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="rival")
    victory_player = models.ForeignKey(Player, on_delete=models.CASCADE)
    challenging_score = models.IntegerField(default=0)
    rival_score = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(default=0)
    created = models.DateTimeField()

    def is_online(self):
        if self.online == True:
            return 'Si'
        else:
            return 'No'

    def __str__(self):
        return self.challenging.nickname + ' ' + ' v/s ' + self.rival.nickname

