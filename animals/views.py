from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from animals.forms import AnimalForm, AnimalEditForm
from animals.models import Animal, AnimalPhoto


class AnimalListView(ListView):
    model = Animal
    template_name = "animals/animal_list.html"
    context_object_name = "animals"
    paginate_by = 8

    def get_queryset(self):
        queryset = Animal.objects.all()

        sex = self.request.GET.get("sex")
        animal_type = self.request.GET.get("animal_type")
        color = self.request.GET.get("color")
        vaccine = self.request.GET.get("vaccine")
        castration = self.request.GET.get("castration")

        age_min = self.request.GET.get("age_min")
        age_max = self.request.GET.get("age_max")

        character = self.request.GET.get("character")

        if sex:
            queryset = queryset.filter(sex=sex)

        if animal_type:
            queryset = queryset.filter(animal_type=animal_type)

        if color:
            queryset = queryset.filter(color=color)

        if vaccine in ["1", "true", "True"]:
            queryset = queryset.filter(vaccine=True)

        if castration in ["1", "true", "True"]:
            queryset = queryset.filter(castration=True)

        if age_min:
            queryset = queryset.filter(age__gte=age_min)

        if age_max:
            queryset = queryset.filter(age__lte=age_max)

        if character:
            queryset = [
                animal for animal in queryset
                if animal.character and character in animal.character
            ]
        queryset = queryset.order_by("?")
        
        return queryset


class FavoriteAnimalsView(ListView):
    model = Animal
    template_name = "animals/favorite_animals.html"
    context_object_name = "animals"
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.favorites.all()
        return Animal.objects.none()


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, animal_id):
        animal = get_object_or_404(Animal, id=animal_id)

        was_favorite = request.user.favorites.filter(pk=animal.pk).exists()

        if was_favorite:
            request.user.favorites.remove(animal)
        else:
            request.user.favorites.add(animal)

        return JsonResponse({
            "status": "ok",
            "is_favorite": not was_favorite,
            "animal_id": animal_id
        })


class AnimalDetailView(DetailView):
    model = Animal
    template_name = "animals/animal-details.html"
    context_object_name = "animal"
    pk_url_kwarg = "animal_id"


class CreateAnimalView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = "animals/create-animal.html"
    login_url = "users:login"

    def form_valid(self, form):
        animal = form.save(commit=False)
        animal.owner = self.request.user
        animal.save()

        for file in form.cleaned_data["photos"]:
            AnimalPhoto.objects.create(animal=animal, image=file)

        return redirect("animals:details", animal_id=animal.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context


class EditAnimalView(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalEditForm
    template_name = "animals/create-animal.html"
    pk_url_kwarg = "animal_id"

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        animal = form.save(commit=False)
        animal.owner = self.request.user
        animal.save()

        for file in form.cleaned_data["photos"]:
            AnimalPhoto.objects.create(animal=animal, image=file)

        return redirect("animals:details", animal_id=animal.id)

    def get_success_url(self):
        return reverse("animals:details", args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

class AnimalDeleteView(LoginRequiredMixin, DeleteView):
    model = Animal
    template_name = "animals/animal_confirm_delete.html"
    pk_url_kwarg = "animal_id"
    success_url = reverse_lazy("animals:animal_list")

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)
