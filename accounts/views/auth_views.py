from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView

from accounts.forms import SignUpForm, LoginForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    success_url = "/admin"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            user.profile.is_corporate = form.cleaned_data.get("is_corporate")
            user.profile.avatar = form.cleaned_data.get("avatar")
            user.save()
            login(request, user)
            return redirect("index")
        context = {}
        context["form"] = form
        return self.render_to_response(context)


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        # next = request.GET.get('next')
        # form_data = {} if not next else {'next': next}
        form = self.form
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        # next = form.cleaned_data.get('next')
        user = authenticate(request, username=username, password=password)
        if not user:
            return redirect('login')
        login(request, user)
        # if next:
        #     return redirect(next)
        return redirect('index')



