from django.forms import BaseModelForm
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.conf import settings

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm


UserModel = get_user_model()


class RegisterPageView(CreateView):
    template_name = "registration.html"
    form_class = UserRegisterForm
    model = UserModel
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)


def login_view(request):
    template_name = "login.html"
    context = {}

    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('users:account')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            print("Form is not valid")

    else:
        form = UserLoginForm()

    context['form'] = form
    return render(request, template_name, context)


def logout_view(request):
    logout(request=request)
    return redirect(settings.LOGOUT_REDIRECT_URL or reverse("users:login"))


# @login_required()
# def account_view(request):
    template_name = "account.html"
    instance = request.user
    
    if request.method == 'POST':

        form = UserRegisterForm(request.POST, instance=instance)

        if form.is_valid():

            form.save()
            messages.success(request, "Your details have been updated.")
            return redirect('some_success_page')
        
        else:
            messages.error(request, "There was an error updating your details.")
    else:
        form = UserRegisterForm(instance=instance)

    return render(request, template_name, {'form': form})


# @method_decorator(login_required, "dispatch")
# class AccountPageView(UpdateView):
#     template_name = "account.html"
#     model = UserModel
#     form_class = UserUpdateForm
#     pk_url_kwarg


@method_decorator(login_required, name='dispatch')
class AccountUpdateView(UpdateView):
    template_name = "account.html"
    success_url = reverse_lazy("users:account")
    model = UserModel
    form_class = UserUpdateForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        data = form.cleaned_data
        user = form.save(commit=False)
        
        if data.get("password"):
            user.set_password(data["password"])

        if user != self.request.user:
            return super().form_invalid(form)

        user.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AccountPageView(TemplateView):
    template_name = 'account.html'
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated.")
            return redirect('account')
        else:
            messages.error(request, "There was an error updating your details.")

        print(form.is_valid())
        
        return self.get(request, *args, **kwargs)
    