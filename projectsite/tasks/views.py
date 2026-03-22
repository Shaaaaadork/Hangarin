from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Task.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return Task.objects.all()
    login_url = 'login'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'category', 'deadline']
    template_name = 'task_form.html' # Django looks for this by default
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'category', 'deadline']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')