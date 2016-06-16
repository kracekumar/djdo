from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages

from todo.models import Todo
from todo.forms import TodoForm, TodoDeleteForm


# Create your views here.

def index(request):
    return HttpResponse('Index')


@login_required
def todo_list(request):
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request, 'todo/todo_list.html', context)

@login_required
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    context = {'todo': todo}
    return render(request, 'todo/todo_detail.html', context)


@login_required
def todo_new(request):
    url = reverse('todo_new')
    if request.method == 'GET':
        form = TodoForm()
        context = {'form': form, 'url': url}
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
                    notes=data['notes'],
                    user=request.user)
            else:
                todo = Todo.objects.create(
                    name=data['name'],
                    is_completed=data['is_completed'],
                    notes=data['notes'],
                    user=request.user)
            context = {'todo': todo}
            return render(request,
                          'todo/todo_detail.html',
                          context)
        else:
            context = {'form': form, 'url': url}
            return render(request,
                          'todo/todo_new.html',
                          context)


@login_required
def todo_edit(request, pk):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, pk=pk)
        url = reverse('todo_edit', args=(todo.id,))
        initial_data = {'id': todo.id,
                        'name': todo.name,
                        'notes': todo.notes,
                        'is_completed': todo.is_completed,
                        'due_date': todo.due_date}
        form = TodoForm(initial=initial_data)
        context = {'form': form, 'submit_url': url}
        return render(request,
                      'todo/todo_new.html',
                      context)
    elif request.method == 'POST':
        form = TodoForm(request.POST)
        todo = get_object_or_404(Todo, pk=pk)
        url = reverse('todo_edit', args=(todo.id,))
        if form.is_valid():
            data = form.cleaned_data
            todo.name = data['name']
            todo.is_completed = data['is_completed']
            todo.notes = data['notes']
            todo.due_date = data['due_date']
            todo.save()
            messages.add_message(request, messages.INFO,
                                 'Successfully updated todo')
            context = {'todo': todo}
            return redirect('todo_detail', todo.id)
        else:
            context = {'form': form,
                       'submit_url': url}
            return render(request,
                          'todo/todo_new.html',
                          context)


@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'GET':
        form = TodoDeleteForm()
        context = {'form': form, 'todo': todo}
        return render(request, 'todo/todo_delete.html',
                      context)
    elif request.method == 'POST':
        form = TodoDeleteForm(request.POST)
        if form.is_valid():
            todo.delete()
            messages.add_message(request, messages.INFO,
                                 'Successfully deleted')
            return redirect('todo_list')
        print(form.errors)
        context = {'form': form, 'todo': todo}
        return render(request, 'todo/todo_delete.html',
                      context)
