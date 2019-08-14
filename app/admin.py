from django.contrib import admin

# Register your models here.
# Register your models here.
from app.models import *

admin.site.register(Char)
admin.site.register(Branch)
admin.site.register(MatchType)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Results)
admin.site.register(News)