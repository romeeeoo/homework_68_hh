from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, DetailView

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


def logout_view(request):
    logout(request)
    return redirect('index')


class ProfileView(DetailView):
    model = get_user_model()
    template_name = "user_detail.html"
    context_object_name = "user_obj"

    # def get_context_data(self, **kwargs):
    #     posts = self.object.posts.all()
    #     print(request.user)
    #     kwargs["posts"] = posts
    #     return super().get_context_data(**kwargs)

    # def post(self, request, *args, **kwargs):
    #     account_id = request.POST.get("cust_id")
    #     account = Account.objects.get(pk=account_id)
    #     user = request.user
    #     # здесь логика по отклику на вакансию/резюме
    #     return redirect('index')


