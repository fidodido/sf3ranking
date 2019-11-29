from django.conf.urls import url
from app.views.index import index
from app.views.league import index as league_index
from app.views.league import create_new_result
from app.views.league import create_new_player
from app.views.league import delete_result
from app.views.league import player
from app.views.league import ranking
from app.views.league import results

urlpatterns = [

    url(r'^$',
        index,
        name='index'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/$',
        league_index,
        name='league_index'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/create-new-result$',
        create_new_result,
        name='league_create_new_result'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/create-new-player$',
        create_new_player,
        name='league_create_new_player'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/delete-result/(?P<result_id>[a-zA-Z0-9-]+)$',
        delete_result,
        name='league_delete_result'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/results$',
        results,
        name='league_results'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/ranking$',
        ranking,
        name='league_ranking'
        ),

    url(r'^league/(?P<league_slug>[a-zA-Z0-9-]+)/player/(?P<player_id>[a-zA-Z0-9-]+)$',
        player,
        name='league_player'
        )
]
