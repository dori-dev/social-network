from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def transaction(request):
    context = {
        'segment': 'transactions'
    }
    return render(request, 'pages/transactions.html', context)


@login_required(login_url="/accounts/login/")
def settings(request):
    context = {
        'segment': 'settings'
    }
    return render(request, 'pages/settings.html', context)


@login_required(login_url="/accounts/login/")
def bs_tables(request):
    context = {
        'parent': 'tables',
        'segment': 'bs_tables',
    }
    return render(request, 'pages/tables/bootstrap-tables.html', context)


@login_required(login_url="/accounts/login/")
def buttons(request):
    context = {
        'parent': 'components',
        'segment': 'buttons',
    }
    return render(request, 'pages/components/buttons.html', context)


@login_required(login_url="/accounts/login/")
def notifications(request):
    context = {
        'parent': 'components',
        'segment': 'notifications',
    }
    return render(request, 'pages/components/notifications.html', context)


@login_required(login_url="/accounts/login/")
def forms(request):
    context = {
        'parent': 'components',
        'segment': 'forms',
    }
    return render(request, 'pages/components/forms.html', context)


@login_required(login_url="/accounts/login/")
def modals(request):
    context = {
        'parent': 'components',
        'segment': 'modals',
    }
    return render(request, 'pages/components/modals.html', context)


@login_required(login_url="/accounts/login/")
def typography(request):
    context = {
        'parent': 'components',
        'segment': 'typography',
    }
    return render(request, 'pages/components/typography.html', context)
