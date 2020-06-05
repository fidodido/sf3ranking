
from django.contrib.auth.models import User
from app.models import League, Game, User, Result, MatchType, Player, Char, Country, Tournament
from rest_framework import routers, serializers, viewsets
from django.db.models.fields import DecimalField



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
	ranking = serializers.DecimalField(decimal_places=2, max_digits=15, default=0)

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
	ranking_del_challenging = serializers.DecimalField(decimal_places=2, max_digits=15, default=0)
	ranking_del_rival = serializers.DecimalField(decimal_places=2, max_digits=15, default=0)

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

	serializer_class = MatchSerializer

	def get_queryset(self):

		league_id = self.request.query_params.get('id')
		queryset = Result.objects.all()

		if league_id:
			queryset = queryset.filter(league_id=league_id).order_by('-created')

		return queryset

	


# ViewSets define the view behavior.
class PlayerViewSet(viewsets.ModelViewSet):

	serializer_class = PlayerSerializer

	def get_queryset(self):

		league_id = self.request.query_params.get('id')
		queryset = Player.objects.all()

		if league_id:
			queryset = queryset.filter(league=league_id, disabled=False).order_by('-ranking')

		return queryset


# ViewSets define the view behavior.
class TournamentViewSet(viewsets.ModelViewSet):

	serializer_class = TournamentSerializer

	def get_queryset(self):

		league_id = self.request.query_params.get('id')
		queryset = Tournament.objects.all()

		if league_id:
			queryset = queryset.filter(league_id=league_id)

		return queryset


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'leagues', LeagueViewSet)
router.register(r'matches', MatchViewSet, basename='Result')
router.register(r'players', PlayerViewSet, basename='Player')
router.register(r'tournaments', TournamentViewSet, basename='Tournament')
# Wire up our API using automatic URL routing.