from django.shortcuts import render
from django.shortcuts import render, redirect
from app.models import Result, Player, League
from app.forms import ResultForm, LeagueForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.util import elo_adapted
import math    
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required

MESSAGE_SUCCESS = "La acción ha sido exitosa."
PAGINATE_DEFAULT = 25;

SORT_DEFAULT = '-created'
SORT_MORE_NEW = 'recientes'
SORT_MORE_VOTED = 'votadas'

SORT_VALUES = {'recientes': '-created', 'votadas': '-votes_agree'}

def index(request):

	results = Result.objects.all().order_by('-created')[:10]
	leagues = League.objects.all()
	form = LeagueForm(initial={'user': request.user})
	template = 'app/index/index.html'

	return render(request, template, {
		'results': results, 	
		'form': form,
	    'leagues': leagues
	})