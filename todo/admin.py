from django.contrib import admin

from .models import Todo
# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_completed', 'due_date',)
    list_filter = ('is_completed',)


admin.site.register(Todo, TodoAdmin)
