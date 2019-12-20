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

            import datetime

            date = datetime.date.today()
            print(date)

            players = Player.objects.all()

            year = 2019
            month = 1

            for player in players:
            	count = Result.objects.annotate(year=2019, month=1).values('year', 'month').annotate(count=Count('pk'))
            	print(count)