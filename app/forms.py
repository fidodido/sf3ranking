from django import forms
from django.forms import ModelForm
from app.models import *
from django.utils.text import slugify


class AuthForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'login-input form-control'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'login-input form-control'}))


class LeagueForm(ModelForm):
    class Meta:
        model = League
        labels = {
            'title': 'Título',
            'game': 'Juego'
        }
        fields = ['title', 'game']
        widgets = {
            'league': forms.HiddenInput(),
            'game': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self):
        instance = super(LeagueForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        instance.save()

        return instance
        


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        labels = {
            'nickname': 'Nick',
            'main': 'Main',
            'ranking': 'Ranking inicial'
        }
        fields = ['nickname', 'ranking', 'main', 'league']
        widgets = {
            'league': forms.HiddenInput(),
            'main': forms.ModelChoiceField(queryset=Char.objects.all()),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'ranking': forms.NumberInput(attrs={'id': 'id_ranking', 'class': 'form-control', 'min': 0}),
        }

class ResultForm(ModelForm):

    class Meta:
        model = Result
        labels = {
            'mtype': 'Tipo de pelea',
            'challenging': 'Retador',
            'rival': 'Rival',
            'challenging_score': 'Marcador retador',
            'rival_score': 'Marcador rival',
            'tournament': 'Seleccionar torneo',
            'replay_url': 'URL Replay'
        }        
        fields = ['league', 'mtype', 'challenging', 'rival', 'challenging_score', 'rival_score', 'tournament', 'replay_url']
        widgets = {
            'league': forms.HiddenInput(),
            'mtype': forms.Select(attrs={'class': 'form-control'}),
            'challenging': forms.Select(attrs={'class': 'form-control'}),
            'rival': forms.Select(attrs={'class': 'form-control'}),
            'challenging_score': forms.NumberInput(attrs={'id': 'id_title', 'class': 'form-control', 'min': 0}),
            'rival_score': forms.NumberInput(attrs={'id': 'id_title', 'class': 'form-control', 'min': 0}),
            'tournament': forms.Select(attrs={'class': 'form-control'}),
            'replay_url': forms.TextInput(attrs={'class': 'form-control'}),
        }