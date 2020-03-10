from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account

def registration(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)



def home(request):
    context = {}
    accounts = Account.objects.all()
    context['accounts'] = accounts

    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'accounts/login.html', context)

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "username:": request.POST['username'],
                "sources": request.POST.get('sources', False),
                "categories": request.POST.get('categories', True),
            }
            form.save()
            context['success_message']= "Updated"
    else:
        form = AccountUpdateForm(initial = {
                                            'username':request.user.username,
                                            'sources': request.user.sources,
                                            'categories': request.user.categories
                                            })
    context['account_form'] = form
    return render(request, 'accounts/account.html', context)

# Create your views here.
