from django.urls import path

from . import views

app_name = "shortener"
urlpatterns = [
    path("<str:hash>/", views.URLRedirectView.as_view(), name="redirect"),
]
