from django.contrib import admin

# Register your models here.
from talks.models import Talks, TalkComment

admin.site.register(Talks)
admin.site.register(TalkComment)