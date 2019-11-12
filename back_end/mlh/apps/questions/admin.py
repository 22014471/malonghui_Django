from django.contrib import admin

# Register your models here.
from questions.models import *

class QuestionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['name']

admin.site.register(Question)
admin.site.register(QuestionCategory)
admin.site.register(Answer)
