from django import forms

from .models import ConversationMessges


class ConversationMessgesForm(forms.ModelForm):
    class Meta:
        model = ConversationMessges
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }
