from django import forms
from account.forms import ImageField
from . import models


class CreateUpdatePostFrom(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            'image',
            'description',
        ]
        field_classes = {
            'image': ImageField,
        }
        labels = {
            'image': 'تصویر',
            'description': 'توضیحات',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
                'invalid': 'این فیلد رو به درستی وارد کن!',
            }
        # image
        image = self.fields['image']
        image.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2'
        image.widget.attrs[
            'autofocus'
        ] = 'true'
        image.widget.attrs[
            'onchange'
        ] = 'loadImage(event)'
        image.error_messages = {
            'required': 'پست ات باید یک تصویر داشته باشه.',
        }
        # description
        description = self.fields['description']
        description.widget.attrs['class'] = 'form-control mt-2 mb-2 rtl'
        description.widget.attrs['dir'] = 'auto'
        description.widget.attrs[
            'placeholder'
        ] = 'توضیحاتی درباره پست ات بنویس...'
        description.error_messages = {
            'required': 'پست ات حتما باید عنوان داشته باشه!',
            'max_length': 'توضیحات پست ات خیلی زیاد شد!',
        }
