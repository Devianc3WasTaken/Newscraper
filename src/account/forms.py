from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

class RegistrationForm(UserCreationForm):

    sources = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder": "Separate your URL's with comma: <url> , <url>",
                                                                                    "class": "new=class-bane two",
                                                                                     "rows": 10,
                                                                                    "cols": 60,
                                                                                    "id": "my-id-for-textarea",
                                                                                  }))
    categories = forms.CharField(max_length=300, required=False, widget=forms.Textarea(attrs={"placeholder": "Separate categories with comma: <keyword> , <keyword>"}))

    class Meta:
        model = Account
        fields = ("username", "password1", "password2", "sources", "categories")


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

    sources = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"placeholder": "Separate your URL's with comma: <url> , <url>",
               "class": "new=class-bane two",
               "rows": 10,
               "cols": 60,
               "id": "my-id-for-textarea",
               }))
    categories = forms.CharField(max_length=300, required=False, widget=forms.Textarea(
        attrs={"placeholder": "Separate categories with comma: <keyword> , <keyword>"}))

    class Meta:
        model = Account
        fields = ('username', 'sources', 'categories')

    # Check if the username user tries to change to it is not already in use
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use!' % username )
