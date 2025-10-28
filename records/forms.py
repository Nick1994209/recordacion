from django import forms
from .models import RecordEntry, RecordImage


class RecordEntryForm(forms.ModelForm):
    class Meta:
        model = RecordEntry
        fields = ['title', 'description', 'preview_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название рекорда'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание рекорда',
                'rows': 5
            }),
            'preview_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'preview_image': 'Картинка для preview'
        }


class RecordImageForm(forms.ModelForm):
    class Meta:
        model = RecordImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'image': 'Картинка для поста'
        }