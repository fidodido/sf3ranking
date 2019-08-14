from django.shortcuts import render
from django.shortcuts import render, redirect
from app.models import Results, Player, News
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

MESSAGE_SUCCESS = "La acción ha sido exitosa."
PAGINATE_DEFAULT = 10;

SORT_DEFAULT = '-created'
SORT_MORE_NEW = 'recientes'
SORT_MORE_VOTED = 'votadas'

SORT_VALUES = {'recientes': '-created', 'votadas': '-votes_agree'}


def index(request):

    results = Results.objects.all().order_by('-id')[:10]
    news = News.objects.all().order_by('-id')[:10]
    players = Player.objects.all()

    template = 'app/index/index.html'

    return render(request, template, {
        'results': results,
        'players': players,
        'news': news,
        'sort': sort,
        'paginator': paginator
    })


def matches(request):

    page = request.GET.get('page', 1)

    results = Results.objects.all()
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

    players = Player.objects.all()

    template = 'app/index/ranking.html'

    return render(request, template, {
        'players': players
    })