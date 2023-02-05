from django import forms
from . import models


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = [
            'body',
        ]

        labels = {
            'body': 'نظر',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
            }
        # body
        body = self.fields['body']
        body.widget.attrs['class'] = 'form-control mt-2 mb-2 rtl'
        body.widget.attrs['dir'] = 'auto'
        body.widget.attrs['rows'] = '5'
        body.widget.attrs[
            'placeholder'
        ] = 'نظرت درباره پست رو بنویس...'
        body.error_messages = {
            'required': 'پست ات حتما باید عنوان داشته باشه!',
            'max_length': 'توضیحات پست ات خیلی زیاد شد!',
        }
