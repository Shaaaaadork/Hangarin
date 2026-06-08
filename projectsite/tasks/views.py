from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Task, SubTask, Category, Priority, Note
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass these to the template so the sidebar can show the options
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        context['statuses'] = ['Pending', 'In Progress', 'Completed']
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        
        # 1. Search Logic
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        
        # 2. Filter Logic (Sidebar Selections)
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        category = self.request.GET.get('category')

        if status: queryset = queryset.filter(status=status)
        if priority: queryset = queryset.filter(priority__id=priority)
        if category: queryset = queryset.filter(category__id=category)
        
        return queryset

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

# Subtasks
class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'
    login_url = 'login'

    def get_queryset(self):
        queryset = SubTask.objects.select_related('parent_task').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            queryset = queryset.filter(title__icontains=q)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

# Categories and Priorities
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q: return Category.objects.filter(name__icontains=q)
        return Category.objects.all()

class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q: return Priority.objects.filter(name__icontains=q)
        return Priority.objects.all()

# Notes
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    login_url = 'login'

    def get_queryset(self):
        queryset = Note.objects.all()
        q = self.request.GET.get('q')
        if q: queryset = queryset.filter(content__icontains=q)
        return queryset.order_by('-created_at')