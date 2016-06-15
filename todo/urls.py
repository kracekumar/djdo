from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'index/$', views.index, name='index'),
    url(r'todo/$', views.todo_list, name='todo_list'),
    url(r'todo/(?P<pk>[0-9]+)/$', views.todo_detail, name='todo_detail'),
    url(r'todo/new', views.todo_new, name='todo_new')
]
