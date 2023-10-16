from django.contrib import admin
from .models import Profile, Post, LikePost

class Postsadmin(admin.ModelAdmin):

    class Meta:
        model = Post
        fields = ('id','user',)


admin.site.register(Profile)
admin.site.register(Post, Postsadmin)
admin.site.register(LikePost)
