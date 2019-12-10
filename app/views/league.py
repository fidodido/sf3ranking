from django.shortcuts import render
from django.shortcuts import render, redirect
from app.models import Char, Result, Player, League, Tournament
from app.forms import ResultForm, PlayerForm, LeagueForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.util import elo_adapted
import math
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse

MESSAGE_SUCCESS = "La acción ha sido exitosa."
PAGINATE_DEFAULT = 25;

SORT_DEFAULT = '-created'
SORT_MORE_NEW = 'recientes'
SORT_MORE_VOTED = 'votadas'

SORT_VALUES = {'recientes': '-created', 'votadas': '-votes_agree'}


def index(request, league_slug):
    return redirect('league_results', league_slug)

def create(request):
    
    success = False

    if request.method == 'POST':

        form = LeagueForm(request.POST)

        if form.is_valid():
            form.save()
            success = True

    return JsonResponse({
        'success': success,
        'errors': dict(form.errors.items())
    })

def tournaments(request, league_slug):

    page = request.GET.get('page', 1)
    league = League.objects.get(slug=league_slug)

    form_new_result = ResultForm(initial={
        'league': league.id,
        'victory_player': 1,
        'loser_player': 2
    })

    tournaments = Tournament.objects.filter(league=league)
    paginator = Paginator(tournaments, PAGINATE_DEFAULT)

    try:
        tournaments = paginator.page(page)
    except PageNotAnInteger:
        tournaments = paginator.page(1)
    except EmptyPage:
        tournaments = paginator.page(paginator.num_pages)

    template = 'app/league/tournaments.html'

    return render(request, template, {
        'form_new_result': form_new_result,
        'league': league,
        'tournaments': tournaments,
        'paginator': paginator
    })

def results(request, league_slug):

    page = request.GET.get('page', 1)
    league = League.objects.get(slug=league_slug)

    form_new_result = ResultForm(initial={
        'league': league.id,
        'victory_player': 1,
        'loser_player': 2
    }, league=league.id)

    results = Result.objects.filter(league=league).order_by('-created')

    paginator = Paginator(results, PAGINATE_DEFAULT)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    template = 'app/league/results.html'

    return render(request, template, {
        'form_new_result': form_new_result,
        'league': league,
        'results': results,
        'paginator': paginator
    })


def ranking(request, league_slug):

    league = League.objects.get(slug=league_slug)
    players = Player.objects.filter(league=league).order_by('-ranking')
    template = 'app/league/ranking.html'

    form = PlayerForm(initial={
        'ranking': 1000,
        'league': league.id
    },game=league.game.id)

    return render(request, template, {
        'form': form,
        'league': league,
        'players': players
    })


def player(request, league_slug, player_id):
    
    league = League.objects.get(slug=league_slug)
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

    template = 'app/league/player.html'

    return render(request, template, {
        'league': league,
        'player': player,
        'results': results,
        'paginator': paginator,
    })


@login_required
def create_new_player(request, league_slug):

    league = League.objects.get(slug=league_slug)
    success = False

    if request.method == 'POST':


        form = PlayerForm(request.POST, game=league.game.id)
        #form.fields['main'].choices = [Char.objects.filter(game__id=league.game.id)]

        if form.is_valid():
            form.save()
            success = True

    return JsonResponse({
        'success': success,
        'errors': dict(form.errors.items())
    })

@login_required
def create_new_result(request, league_slug):

    league = League.objects.get(slug=league_slug)
    success = False

    if request.method == 'POST':

        form = ResultForm(request.POST, league=league.id)

        if form.is_valid():

            victory_player = None
            loser_player = None

            new_result = form.save()

            is_tournament = False

            if new_result.mtype.id == 2:
                is_tournament = True

            changes = elo_adapted(new_result.challenging.ranking, new_result.rival.ranking,
                                  new_result.challenging_score, new_result.rival_score, is_tournament)

            if new_result.challenging_score > new_result.rival_score:
                victory_player = new_result.challenging
                loser_player = new_result.rival
            else:
                victory_player = new_result.rival
                loser_player = new_result.challenging

            new_result.challenging.ranking = new_result.challenging.ranking + changes[0]
            new_result.challenging.save()

            new_result.rival.ranking = new_result.rival.ranking + changes[1]
            new_result.rival.save()

            new_result.victory_player = victory_player
            new_result.loser_player = loser_player
            new_result.ranking_del_challenging = changes[0]
            new_result.ranking_del_rival = changes[1]
            new_result.save()

            success = True

    return JsonResponse({
        'success': success,
        'errors': dict(form.errors.items())
    })

@login_required
def delete_result(request, league_slug, result_id):

    match = Result.objects.get(pk=result_id)

    # actualizamos el ranking del retador.
    match.challenging.ranking = match.challenging.ranking - match.ranking_del_challenging
    match.challenging.save()

    # actualizamos el rankign del rival.
    match.rival.ranking = match.rival.ranking - match.ranking_del_rival
    match.rival.save()

    match.delete()

    return redirect('league_index', league_slug=league_slug)
