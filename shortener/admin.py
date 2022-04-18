from django.contrib import admin

from .models import URL


class URLAdmin(admin.ModelAdmin):
    exclude = ["hashed_url"]
    list_filter = ["created_at"]
    search_fields = ["long_url"]


admin.site.register(URL, URLAdmin)
