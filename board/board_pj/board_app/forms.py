from django import forms
from django.core.exceptions import ValidationError
from .models import *


class NoticeForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = [
            'title',
            'category',
            'content'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if title == content:
            raise ValidationError(
                "The text should not be identical to the title."
            )
        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "The title should start with a capital letter."
            )
        return title


class FeedbackForm(forms.ModelForm):
    text = forms.CharField(min_length=10)

    class Meta:
        model = Feedback
        fields = [
            'text',
            'notice_fb'
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text[0].islower():
            raise ValidationError(
                "The text should start with a capital letter."
            )
        return cleaned_data
