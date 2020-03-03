from django import forms

from forums.models import Forum

class ForumForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ('title', 'text',)