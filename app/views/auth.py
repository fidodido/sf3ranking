from django.shortcuts import render
from django.shortcuts import render, redirect
from app.models import Result, Player, League
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
