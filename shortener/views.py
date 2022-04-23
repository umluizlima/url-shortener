from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import URLCreateForm
from .models import URL


class URLRedirectView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(URL, hashed_url=kwargs["hash"])
        return url.long_url


class URLIndexView(generic.FormView):
    template_name = "shortener/index.html"
    form_class = URLCreateForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        url = URL.objects.create(long_url=form.cleaned_data["long_url"])
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class(),
                "url": url,
            },
        )


class URLDetailView(generic.DetailView):
    model = URL
    slug_field = "hashed_url"
    slug_url_kwarg = "hash"
    template_name = "shortener/detail.html"
