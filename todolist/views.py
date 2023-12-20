from django.http import JsonResponse
from django.shortcuts import render
from .models import Task

def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        due_time = request.POST.get('due_time')
        task = Task.objects.create(title=title, due_date=due_date, due_time=due_time, description=description)
        return JsonResponse({'status': 'ok'})

def update(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'status': 'ok'})

def delete(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.delete()
        return JsonResponse({'status': 'ok'})
