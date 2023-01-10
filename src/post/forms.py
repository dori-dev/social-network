from os.path import basename
from urllib import request
from urllib.parse import urlparse
from django import forms
from django.core.files.base import ContentFile
from . import models


def check_exists(url):
    try:
        response = request.urlopen(url)
        if response.code in range(200, 209):
            return True, response
    except Exception:
        pass
    return False, None


def check_image(response, valid_extensions):
    info = response.info()
    if info.get_content_maintype().lower() == 'image':
        return info.get_content_subtype().lower() in valid_extensions
    return False


def is_image_url(image_url, valid_extensions):
    exists, response = check_exists(image_url)
    if exists and check_image(response, valid_extensions):
        return True, response
    return False, None


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            'title',
            'description',
            'url',
        ]
        labels = {
            'title': 'عنوان',
            'description': 'توضیحات',
        }
        widgets = {
            'url': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
                'invalid': 'این فیلد رو به درستی وارد کن!',
            }
        # title
        title = self.fields['title']
        title.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2 rtl post-title-input'
        title.widget.attrs['dir'] = 'auto'
        title.widget.attrs[
            'placeholder'
        ] = 'عنوان پست ات رو اینجا بنویس...'
        title.error_messages = {
            'required': 'پست ات حتما باید عنوان داشته باشه!',
            'max_length': 'عنوان پست ات باید کمتر از ۱۰۰ کاراکتر باشه!',
        }
        # description
        description = self.fields['description']
        description.widget.attrs['class'] = 'form-control mt-2 mb-2 rtl'
        description.widget.attrs['dir'] = 'auto'
        description.widget.attrs[
            'placeholder'
        ] = 'توضیحاتی درباره پست ات بنویس...'

    def clean(self):
        cleaned_data = super().clean()
        url: str = cleaned_data['url']
        valid_extensions = [
            'jpg',
            'jpeg',
            'png',
            'gif',
            'webp',
        ]
        is_image, response = is_image_url(url, valid_extensions)
        if not is_image:
            raise forms.ValidationError('این لینک یک تصویر نیست!')
        self.response = response
        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError(
                'عنوان پست ات باید کمتر از ۱۰۰ کاراکتر باشه!'
            )
        return title

    def save(self, commit=True):
        image: models.Post = super().save(commit=False)
        image_url = self.cleaned_data['url']
        path = urlparse(image_url).path
        image_name = basename(path)
        # download image
        image.image.save(
            image_name,
            ContentFile(self.response.read()),
            save=False,
        )
        if commit:
            image.save()
        return image
