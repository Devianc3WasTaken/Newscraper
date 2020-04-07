from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):

    guardianSource = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id':'guardianSource'}),required=False)
    bbcSource = forms.BooleanField(required=False)
    independentSource = forms.BooleanField(required=False)

    categoryCoronaVirus = forms.BooleanField(required=False)
    categoryPolitics = forms.BooleanField(required=False)
    categorySport = forms.BooleanField(required=False)

    #Telling the registration form what kind of data we are going to be modelling/ what the form needs to look like
    class Meta:
        model = Account
        fields = ("username", "password1", "password2", "guardianSource", "bbcSource", "independentSource", "categoryCoronaVirus", "categoryPolitics", "categorySport")


#


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ( 'username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid Login!")





class AccountUpdateForm(forms.ModelForm):


    class Meta:
        model = Account
        fields = ('username', "guardianSource", "bbcSource", "independentSource", "categoryCoronaVirus", "categoryPolitics", "categorySport")

    # Check if the username user tries to change to it is not already in use
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use!' % account.username )
