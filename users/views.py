from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View

from emu.forms import SignUpForm, SignInForm
from emu.utils import get_next


class Register(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            sign_up_form = SignUpForm()
            context = {'sign_up_form': sign_up_form}
            return render(self.request, 'users/register.html', context)
        else:
            logout(self.request)
            sign_up_form = SignUpForm()
            context = {'sign_up_form': sign_up_form}
            return render(self.request, 'users/register.html', context)

    def post(self, *args, **kwargs):
        sign_up_form = SignUpForm(data=self.request.POST)
        if sign_up_form.is_valid():
            new_user = sign_up_form.save()
            login(self.request, new_user)
            return redirect('emu:item-list')
        else:
            context = {'sign_up_form': sign_up_form}
            return render(self.request, 'users/register.html', context)


class Login(View):
    def get(self, *args, **kwargs):
        print(self.request.user)
        get_next.next = self.request.GET.get('next')
        if not self.request.user.is_authenticated:
            sign_in_form = SignInForm()
            context = {'sign_in_form': sign_in_form}
            return render(self.request, 'users/login.html', context)
        else:
            logout(self.request)
            sign_in_form = SignInForm()
            context = {'sign_in_form': sign_in_form}
            messages.success(self.request, "Successfully signed out. Sign In again")
            return render(self.request, 'users/login.html', context)

    def post(self, *args, **kwargs):
        sign_in_form = SignInForm(data=self.request.POST)
        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data.get('username')
            password = sign_in_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(f"Next: {get_next.next}")
            login(self.request, user)
            if get_next.next:
                return redirect(get_next.next)
            else:
                return redirect('emu:item-list')
        else:
            context = {'sign_in_form': sign_in_form}
            return render(self.request, 'users/login.html', context)


class LogoutUser(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('users:login')

