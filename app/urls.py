from django.conf.urls import url
from app.views import index
from app.views import matches
from app.views import ranking

urlpatterns = [

	url(r'^$',
		matches,
		name='index'
	),

	url(r'^matches$',
		matches,
		name='matches'
	),

	url(r'^ranking$',
		ranking,
		name='ranking'
	)
]
