
from django.contrib.auth.models import User
from app.models import League, Game, User, Result, MatchType, Player, Char, Country, Tournament
from rest_framework import routers, serializers, viewsets

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = ('title', 'url_image',)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'url_image', )

class CharSerializer(serializers.ModelSerializer):

	game = GameSerializer()

    class Meta:
        model = Char
        fields = ('name', 'url_image', 'game')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class PlayerSerializer(serializers.ModelSerializer):

	id = serializers.ReadOnlyField()
	main = CharSerializer()
	country = CountrySerializer()

	class Meta:
		model = Player
		fields = ('id', 'nickname', 'ranking', 'main', 'country', 'victories', 'loses', 'played', 'champions')

class MatchTypeSerializer(serializers.ModelSerializer):

	id = serializers.ReadOnlyField()

	class Meta:
		model = MatchType
		fields = ('id', 'name', )


# Serializers define the API representation.
class LeagueSerializer(serializers.ModelSerializer):

	id = serializers.ReadOnlyField()
	game = GameSerializer()
	user = UserSerializer()
	
	class Meta:

		model = League
		fields = ('id', 'title', 'game', 'user', 'results')

class MatchSerializer(serializers.ModelSerializer):

	mtype = MatchTypeSerializer()
	challenging = PlayerSerializer()
	rival = PlayerSerializer()
	victory_player = PlayerSerializer()
	league = LeagueSerializer()

	class Meta:
		model = Result
		fields = ('challenging_score', 'rival_score', 'ranking_del_challenging', 'ranking_del_rival', 'mtype', 'challenging', 'rival', 'victory_player', 'league')


class TournamentSerializer(serializers.ModelSerializer):

	champion = PlayerSerializer()

	class Meta:
		model = Tournament
		fields = ('name', 'champion', )


# ViewSets define the view behavior.
class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


# ViewSets define the view behavior.
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = MatchSerializer


# ViewSets define the view behavior.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

# ViewSets define the view behavior.
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'leagues', LeagueViewSet)
router.register(r'matchs', MatchViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'tournaments', TournamentViewSet)
# Wire up our API using automatic URL routing.