from django.urls import path

from . import views

app_name = "shortener"
urlpatterns = [
    path("<str:hash>/", views.URLRedirectView.as_view(), name="redirect"),
    path("", views.URLIndexView.as_view(), name="index"),
    path("<str:hash>/detail", views.URLDetailView.as_view(), name="detail"),
]
