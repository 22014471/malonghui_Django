from django.contrib import admin

# Register your models here.
from headlines.models import HeadlinesCategory, HeadlinesNews, NewsComment

admin.site.register(HeadlinesCategory)
admin.site.register(HeadlinesNews)
admin.site.register(NewsComment)
