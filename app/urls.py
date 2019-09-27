from django.conf.urls import url
from app.views import index
from app.views import matches
from app.views import ranking
from app.views import new_match
from app.views import player
urlpatterns = [

	url(r'^$',
		index,
		name='index'
	),

	url(r'^matches$',
		matches,
		name='matches'
	),

	url(r'^ranking$',
		ranking,
		name='ranking'
	),

	url(r'^player/(?P<player_id>[a-zA-Z0-9-]+)$',
		player,
		name='player'
	),

	url(r'^new-match$',
		new_match,
		name='new_match'
	)
]
