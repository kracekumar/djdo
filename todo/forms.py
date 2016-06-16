# -*- coding: utf-8 -*-

from django import forms


class TodoForm(forms.Form):
    name = forms.CharField(label='Todo Name', min_length=4,
                           max_length=255)
    is_completed = forms.BooleanField(required=False)
    due_date = forms.DateTimeField(required=False, input_formats=['%Y-%m-%d %H:%M:%S'])
    notes = forms.CharField(widget=forms.Textarea, required=False)


class TodoDeleteForm(forms.Form):
    pass
