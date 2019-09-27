from django import forms
from django.forms import ModelForm
from app.models import *
from django.utils.text import slugify


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
        fields = ['mtype', 'challenging', 'rival', 'challenging_score', 'rival_score', 'tournament', 'replay_url']
        widgets = {
            'mtype': forms.Select(attrs={'class': 'form-control'}),
            'challenging': forms.Select(attrs={'class': 'form-control'}),
            'rival': forms.Select(attrs={'class': 'form-control'}),
            'challenging_score': forms.NumberInput(attrs={'id': 'id_title', 'class': 'form-control'}),
            'rival_score': forms.NumberInput(attrs={'id': 'id_title', 'class': 'form-control'}),
            'tournament': forms.Select(attrs={'class': 'form-control'}),
            'replay_url': forms.TextInput(attrs={'class': 'form-control'}),
        }