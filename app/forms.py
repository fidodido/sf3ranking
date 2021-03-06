from django import forms
from django.forms import ModelForm
from app.models import *
from django.utils.text import slugify


class AuthForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'login-input form-control'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'login-input form-control'}))

class VersusForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.league_id = kwargs.pop('league_id')
        print(self.league_id)
        super(VersusForm,self).__init__(*args,**kwargs)

        self.fields['player1'] = forms.ModelChoiceField(required=False, queryset=Player.objects.filter(league__id=self.league_id).order_by('nickname'), empty_label="Seleccione player", widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['player2'] = forms.ModelChoiceField(required=False, queryset=Player.objects.filter(league__id=self.league_id).order_by('nickname'), empty_label="Seleccione player", widget=forms.Select(attrs={'class': 'form-control'}))
        
class LeagueForm(ModelForm):
    class Meta:
        model = League
        labels = {
            'title': 'Nombre de la liga',
            'game': 'Selecciona el juego'
        }
        fields = ['title', 'game', 'user']
        widgets = {
            'user': forms.HiddenInput(),
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
            'country': 'Pais'
        }
        fields = ['nickname', 'main', 'league', 'country']
        widgets = {
            'league': forms.HiddenInput(),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'main': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'ranking': forms.NumberInput(attrs={'id': 'id_ranking', 'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super(PlayerForm, self).__init__(*args, **kwargs) 
        self.fields['main'].queryset = Char.objects.filter(game__id=game).order_by('name')
        self.fields['country'].queryset = Country.objects.all().order_by('name')


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

    def __init__(self, *args, **kwargs):

        league = kwargs.pop('league', None)
        super(ResultForm, self).__init__(*args, **kwargs) 
        self.fields['challenging'].queryset = Player.objects.filter(league__id=league).order_by('nickname')
        self.fields['rival'].queryset = Player.objects.filter(league__id=league).order_by('nickname')


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        labels = {
            'name': 'Nombre'
        }
        fields = ['name', 'league', 'champion']
        widgets = {
            'league': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'champion': forms.Select(attrs={'class': 'form-control'}),
        }