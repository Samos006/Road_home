from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from events.forms import EventForm, EventEditForm, ApplicationForm
from events.models import Event, Application
from animals.models import Animal


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    paginate_by = 6

    def get_queryset(self):
        queryset = Event.objects.select_related('owner')
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(owner__role=role)
        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event-details.html"
    context_object_name = "event"
    pk_url_kwarg = "event_id"


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/create-event.html"
    login_url = 'users:login'

    def form_valid(self, form):
        event = form.save(commit=False)
        event.owner = self.request.user
        event.save()
        return redirect("events:details_event", event.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context


class EditEventView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventEditForm
    template_name = "events/create-event.html"
    pk_url_kwarg = "event_id"

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse("events:details_event", args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "applications/applications_list.html"
    context_object_name = "applications"
    login_url = "users:login"
 
    def get_queryset(self):
        return (
            Application.objects
            .filter(animal__owner=self.request.user)
            .select_related("animal", "owner")
            .order_by("-created_at")
        )
 
 
class DeleteApplicationView(LoginRequiredMixin, View):
    login_url = "users:login"
 
    def post(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
 
        if application.animal.owner != request.user:
            messages.error(request, "У вас нет прав удалить эту заявку.")
            return redirect("users:user_detail", user_id=request.user.id)
 
        application.delete()
        messages.success(request, "Заявка удалена.")
        return redirect("events:my_applications")
 
class CreateApplicationView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "applications/create-application.html"
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.request.GET.get("animal_id") or self.request.POST.get("animal_id")
        if animal_id:
            context["animal"] = get_object_or_404(Animal, id=animal_id)
        return context

    def form_valid(self, form):
        application = form.save(commit=False)
        application.owner = self.request.user

        animal_id = self.request.POST.get("animal_id") or self.request.GET.get("animal_id")
        if animal_id:
            application.animal_id = animal_id

        app_type = self.request.POST.get("title") or self.request.GET.get("app_type", "take_home")
        application.title = app_type

        application.save()
        return redirect("events:success")


class ApplicationSuccessView(TemplateView):
    template_name = "applications/application-success.html"
