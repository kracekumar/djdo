from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from todo.models import Todo
from todo.forms import TodoForm


# Create your views here.

def index(request):
    return HttpResponse('Index')


def todo_list(request):
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request, 'todo/todo_list.html', context)


def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    context = {'todo': todo}
    return render(request, 'todo/todo_detail.html', context)


def todo_new(request):
    if request.method == 'GET':
        form = TodoForm()
        context = {'form': form}
        return render(request, 'todo/todo_new.html',
                      context)
    elif request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.INFO,
                                 'Successfully created todo')
            data = form.cleaned_data
            if data['due_date']:
                todo = Todo.objects.create(
                    name=data['name'],
                    is_completed=data['is_completed'],
                    due_date=data['due_date'],
                    notes=data['notes'])
            else:
                todo = Todo.objects.create(
                    name=data['name'],
                    is_completed=data['is_completed'],
                    notes=data['notes'])
            context = {'todo': todo}
            return render(request,
                          'todo/todo_detail.html',
                          context)
        else:
            context = {'form': form}
            return render(request,
                          'todo/todo_new.html',
                          context)
