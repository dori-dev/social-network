from . import forms


def search(request):
    form = forms.SearchForm()
    return {
        'search_form': form,
    }
