from django.views.generic import TemplateView, RedirectView


class HomePageView(RedirectView):
    pattern_name = "products:products"