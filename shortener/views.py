from django.shortcuts import get_object_or_404
from django.views import generic

from .models import URL


class URLRedirectView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(URL, hashed_url=kwargs["hash"])
        return url.long_url
