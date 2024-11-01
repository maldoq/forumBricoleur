from django.contrib import admin
from .models import Comment,Like,DisLike,Article,Tag

# Register your models here.
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(DisLike)
admin.site.register(Article)
admin.site.register(Tag)