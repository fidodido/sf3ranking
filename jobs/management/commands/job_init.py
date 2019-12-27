from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    #create an sh file and schedule in CRONTAB or supervisor
    help = 'Python Job Manager - Backend'

#arguments needs to be defined here
    def add_arguments(self, parser):

        parser.add_argument(
            #job name can be passed along with either of the parameters
            '-a',
            '--appName',
            default=False,
            dest='app_name',
            #LIST OF CHOICES - job name
            choices=['app']
        )

        #Add any additional parameters as an argument
        parser.add_argument(
            #user preferences
            '-n',
            '--days',
            default='7',
            dest='num_days',
            choices=['7', '2']
        )

    #Any valid command will call handler
    def handle(self, *args, **options):

        #Init Jobs
        app_name = options['app_name']

        #sample 
        if app_name == 'app':

            from app.models import Player, Result
            from django.db.models import Q
            from django.db.models.functions import Extract

            import datetime

            cur_date = datetime.date.today()
            cur_year_month = cur_date.strftime("%Y-%m")
            players = Player.objects.all()
            
            for player in players:

                count = 0

                # contar los resultados jugadores durante el mes actual.
                results = Result.objects.filter(Q(challenging=player)| Q(rival=player))

                for result in results:
                    if cur_year_month == result.created.strftime("%Y-%m"):
                        count = count + 1

                # si no tiene peleas, se deshabilita el player
                if count == 0:
                    player.disabled = True
                    player.save()