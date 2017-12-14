from django.contrib import admin

from iw_app.models import Article, Comment, Draft

# Register your models here.
# admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Draft)
