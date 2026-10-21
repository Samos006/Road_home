from django.urls import path

from animals.views import(
    AnimalListView,
    FavoriteAnimalsView,
    ToggleFavoriteView,
    AnimalDetailView,
    CreateAnimalView,
    EditAnimalView,
    AnimalDeleteView
)

app_name = "animals"

urlpatterns = [
    path("list/", AnimalListView.as_view(), name = "animal_list"),
    path("favorites/", FavoriteAnimalsView.as_view(), name = "favorite_animals"),
    path("<int:animal_id>/toggle-favorite/", ToggleFavoriteView.as_view(), name = "toggle-favorite"),
    path("<int:animal_id>/", AnimalDetailView.as_view(), name = "details"),
    path("create-animal/", CreateAnimalView.as_view(), name = "create"),
    path("<int:animal_id>/edit/", EditAnimalView.as_view(), name = "edit"),
    path("<int:animal_id>/delete/", AnimalDeleteView.as_view(), name="delete"),
]
