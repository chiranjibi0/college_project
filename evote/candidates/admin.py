from django.contrib import admin
from .models import Candidate,Party,Voter,Election,Vote
# Register your models here.

admin.site.site_header="e-Vote_Campus"
admin.site.register(Party)
admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(Vote)
