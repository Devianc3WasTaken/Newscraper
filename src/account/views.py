from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm,  AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from account.scraper import Scraper

def registration(request):
    context = {}

    if request.user.is_authenticated: # If user is logged in, redirect to home screen, they cannot register again!
        return redirect('home')
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
    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)

### HOME VIEW ###
def home(request):
    context = {}
    accounts = Account.objects.all()
    context['accounts'] = accounts

    scraper = Scraper("https://www.theguardian.com/politics", "Coronavirus")

    # To do : Scrape the bloody articles!

    # checkRecent can take a "force-yes" parameter to enforce the scraper to always scrape
    # if scraper.checkRecent("force-yes"):
    if scraper.checkRecent():
        print("Scrape has been recent")
    else:
        #scraper.search()
        print("Scrape has not been recent")

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
            form.save()
            context['success_message'] = "Updated"
    else: # Display the saved user details from database
        form = AccountUpdateForm(
                                initial = {
                                'username':request.user.username,
                                "guardianSource": request.user.guardianSource,
                                "bbcSource": request.user.bbcSource,
                                "independentSource": request.user.independentSource,

                                "categoryCoronaVirus": request.user.categoryCoronaVirus,
                                "categoryPolitics": request.user.categoryPolitics,
                                "categorySport": request.user.categorySport,
                                            })
    context['account_form'] = form
    return render(request, 'accounts/account.html', context)

# Create your views here.
