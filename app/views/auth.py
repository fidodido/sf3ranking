from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from docx import Document
from app.forms import AuthForm
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
from elo import rate_1vs1

MESSAGE_SUCCESS = "La acción ha sido exitosa."
PAGINATE_DEFAULT = 25;

SORT_DEFAULT = '-created'
SORT_MORE_NEW = 'recientes'
SORT_MORE_VOTED = 'votadas'

SORT_VALUES = {'recientes': '-created', 'votadas': '-votes_agree'}


#this errors must be in global config
ERR_NOT_VALID = 'Sorry, Not valid account'
ERR_INACTIVE = 'Sorry, this account is inactive'
NO_PROJECTS = 'Sorry, this account dont have projects active'
SUCCESS_REDIRECT = '/'
LOGOUT_REDIRECT = '/'

def login(request):

    success_redirect = 'index'
    template = 'app/auth/login.html'

    if request.method == 'POST':

        form = AuthForm(request.POST)
        errors = []
        context = {
            'form': form,
            'errors': errors
        }

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            # si el usuario existe.
            if user is not None:

                # si el usuario esta activo.
                if user.is_active:

                    auth_login(request, user)
                    return redirect(SUCCESS_REDIRECT)
                    
                else:
                    errors.append(ERR_INACTIVE)
                    return render(request, template, context)
            else:
                errors.append(ERR_NOT_VALID)
                return render(request, template, context)
        else:
            return render(request, template, context)

    form = AuthForm()
    return render(request, template)

def signout(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT)