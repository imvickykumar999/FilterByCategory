from django.contrib import admin
from .models import Post, Comment, LikeDislike, Profile, Category

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikeDislike)
admin.site.register(Profile)
admin.site.register(Category)
