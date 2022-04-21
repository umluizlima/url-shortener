from django.contrib import admin

from .models import URL


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_filter = ["created_at"]
    search_fields = ["long_url"]

    def get_exclude(self, request, obj=None):
        return self.exclude if obj else ["hashed_url"]
