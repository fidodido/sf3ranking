from django.shortcuts import render
from django.shortcuts import render, redirect
from app.models import Result, Player, News
from app.forms import ResultForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.util import elo_native, elo_adapted
import math    
from django.db.models import Q

MESSAGE_SUCCESS = "La acción ha sido exitosa."
PAGINATE_DEFAULT = 25;

SORT_DEFAULT = '-created'
SORT_MORE_NEW = 'recientes'
SORT_MORE_VOTED = 'votadas'

SORT_VALUES = {'recientes': '-created', 'votadas': '-votes_agree'}

def new_match(request):
    
    form = ResultForm(initial={
            'victory_player': 1,
            'loser_player': 2
        })

    template = 'app/index/new_match.html'

    if request.method == 'POST':

        form = ResultForm(request.POST)

        if form.is_valid():

            victory_player = None
            loser_player = None

            new_result = form.save()

            is_tournament = False
            
            if new_result.mtype.id == 2:
                is_tournament = True

            delta = elo_adapted(new_result.challenging.ranking, new_result.rival.ranking, new_result.challenging_score, new_result.rival_score, is_tournament)

            if new_result.challenging_score > new_result.rival_score:
                victory_player = new_result.challenging
                loser_player = new_result.rival
            else:
                victory_player = new_result.rival
                loser_player = new_result.challenging

            victory_player.ranking = victory_player.ranking + delta
            victory_player.save()

            loser_player.ranking = loser_player.ranking - delta
            loser_player.save()

            new_result.victory_player = victory_player
            new_result.loser_player = loser_player
            new_result.ranking_del = delta
            new_result.save()

            messages.add_message(request, messages.SUCCESS, MESSAGE_SUCCESS)
            return redirect('new_match')


    return render(request, template, {
        'form': form
    })

def index(request):
    return redirect('matches')

def player(request, player_id):

    page = request.GET.get('page', 1)

    player = Player.objects.get(pk=player_id)
    results = Result.objects.filter(Q(challenging=player) | Q(rival=player)).order_by('-created')
    paginator = Paginator(results, PAGINATE_DEFAULT)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    template = 'app/index/player.html'

    return render(request, template, {
        'player': player,
        'results': results,
        'paginator': paginator,
    })

def matches(request):

    page = request.GET.get('page', 1)

    results = Result.objects.all().order_by('-created')
    paginator = Paginator(results, PAGINATE_DEFAULT)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    template = 'app/index/matches.html'

    return render(request, template, {
        'results': results,
        'paginator': paginator,
    })


def ranking(request):

    players = Player.objects.all().order_by('-ranking')

    template = 'app/index/ranking.html'

    return render(request, template, {
        'players': players
    })