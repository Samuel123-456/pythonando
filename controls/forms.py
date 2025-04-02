from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class FormSignup(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'username': 'username',
                'class': 'block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'passoword',
                'class': 'block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6'
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'confirm_password',
                'class': 'block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6'
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    

    def clean(self):
        data = super().clean()

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()

        if not username:
            messages.error(self.request, 'username not informed!')
            raise forms.ValidationError('username not informed!')
        if User.objects.filter(username=username).exists():
            messages.error(self.request, 'This user name already exists')
            raise forms.ValidationError('This user name already exists')
        if not password:
            raise forms.ValidationError('password not informed!')
        if len(password) < 5:
            messages.error(self.request, 'password less then 5 digits')
            raise forms.ValidationError('password less then 5 digits')
        if not confirm_password:
            messages.error(self.request, 'password confirmationo not informed')
            raise forms.ValidationError('password confirmationo not informed')
        if confirm_password != password:
            messages.error(self.request, 'different password confirmation!')
            raise forms.ValidationError('different password confirmation!')
        
        

        return data
    
    def save(self, *args, **kwargs):
        data = self.clean()

        User.objects.create_user(
            username=data.get('username'),
            password=data.get('password')
        )
        
        messages.success(self.request, 'User creation was success!')



class FormSignin(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'name': 'username',
                'class': 'block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'class': 'block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6'
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


