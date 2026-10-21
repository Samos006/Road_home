from django.urls import path

from events.views import (
    EventListView,
    EventDetailView,
    CreateEventView,
    EditEventView,
    CreateApplicationView,
    ApplicationSuccessView,
    MyApplicationsView,
    DeleteApplicationView
)

app_name = "events"

urlpatterns = [
    path("list/", EventListView.as_view(), name="event_list"),
    path("<int:event_id>/", EventDetailView.as_view(), name="details_event"),
    path("create-event/", CreateEventView.as_view(), name="create_event"),
    path("<int:event_id>/edit/", EditEventView.as_view(), name="edit_event"),
    path("create/", CreateApplicationView.as_view(), name="create_application"),
    path("success/", ApplicationSuccessView.as_view(), name="success"),
    path("my-applications/", MyApplicationsView.as_view(), name="my_applications"),
    path("applications/<int:application_id>/delete/", DeleteApplicationView.as_view(), name="delete_application"),
]
