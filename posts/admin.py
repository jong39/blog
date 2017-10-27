from django.contrib import admin

# Register your models here.

from .models import Post

class PostModelAdmin(admin.ModelAdmin): #ModelAdmin is referring to Post model in models.py
    list_display = ["__unicode__", "title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated"]
    list_editable = ["title"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
