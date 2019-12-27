from django.contrib import admin

# Register your models here.
# Register your models here.
from app.models import *

admin.site.register(Game)
admin.site.register(League)
admin.site.register(Char)
admin.site.register(MatchType)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Result)
admin.site.register(Country)