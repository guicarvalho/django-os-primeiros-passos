from django.contrib import admin
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at',)
    search_fields = ('title',)
    prepopulated_fields = {'post_slug': ('title',)}


admin.site.register(Post, PostAdmin)
