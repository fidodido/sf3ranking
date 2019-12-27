from django.conf.urls import url
from app.views.index import index
from app.views.league import index as league_index
from app.views.league import create_new_player
from app.views.league import create_new_result
from app.views.league import create_new_tournament
from app.views.league import delete_result
from app.views.league import player
from app.views.league import player_edit
from app.views.league import ranking
from app.views.league import results
from app.views.league import tournaments
from app.views.league import create as league_create
from app.views.auth import login
from app.views.auth import signout
from app.views.auth import signup

urlpatterns = [

    url(r'^$',
        index,
        name='index'
        ),

    url(r'^login/$',
        login,
        name='login'
    ),

    url(r'^signup/$',
        signup,
        name='signup'
    ),

    url(r'^logout$',
        signout,
        name='signout'
    ),

    url(r'^crear-nueva-liga$',
        league_create,
        name='league_create'
    ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/$',
        league_index,
        name='league_index'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/create-new-result$',
        create_new_result,
        name='league_create_new_result'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/create-new-tournament$',
        create_new_tournament,
        name='league_create_new_tournament'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/create-new-player$',
        create_new_player,
        name='league_create_new_player'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/delete-result/(?P<result_id>[a-zA-Z0-9-]+)$',
        delete_result,
        name='league_delete_result'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/results$',
        results,
        name='league_results'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/tournaments$',
        tournaments,
        name='league_tournaments'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/ranking$',
        ranking,
        name='league_ranking'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/player/(?P<player_id>[a-zA-Z0-9-]+)$',
        player,
        name='league_player'
        ),

    url(r'^l/(?P<league_slug>[a-zA-Z0-9-]+)/player/(?P<player_id>[a-zA-Z0-9-]+)/editar$',
        player_edit,
        name='league_player_edit'
        )
]
