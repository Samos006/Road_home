from django.views.generic import TemplateView
from animals.models import Animal
from users.models import User


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["dogs_count"] = Animal.objects.filter(animal_type="dog").count()
        context["cats_count"] = Animal.objects.filter(animal_type="cat").count()
        context["groups_count"] = User.objects.filter(role="shelter").count()

        return context
