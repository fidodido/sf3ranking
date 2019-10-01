from django.shortcuts import render
from django.shortcuts import render, redirect
from app.models import Result, Player, News
from app.forms import ResultForm
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

@login_required
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

            changes = elo_adapted(new_result.challenging.ranking, new_result.rival.ranking, new_result.challenging_score, new_result.rival_score, is_tournament)
            print(changes)

            if new_result.challenging_score > new_result.rival_score:
                victory_player = new_result.challenging
                loser_player = new_result.rival
            else:
                victory_player = new_result.rival
                loser_player = new_result.challenging

            new_result.challenging.ranking = new_result.challenging.ranking + changes[0]
            new_result.challenging.save()

            new_result.rival.ranking =  new_result.rival.ranking +  changes[1]
            new_result.rival.save()

            new_result.victory_player = victory_player
            new_result.loser_player = loser_player
            new_result.ranking_del_challenging = changes[0]
            new_result.ranking_del_rival = changes[1]
            new_result.save()

            messages.add_message(request, messages.SUCCESS, MESSAGE_SUCCESS)
            return redirect('new_match')

    return render(request, template, {
        'form': form
    })


@login_required
def delete_match(request, match_id):

    match = Result.objects.get(pk=match_id)

    # actualizamos el ranking del retador.
    match.challenging.ranking = match.challenging.ranking - match.ranking_del_challenging
    match.challenging.save()

    # actualizamos el rankign del rival.
    match.rival.ranking = match.rival.ranking - match.ranking_del_rival
    match.rival.save()

    match.delete()

    return redirect('matches')


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