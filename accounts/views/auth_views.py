from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from accounts.forms import SignUpForm, LoginForm, UserChangeForm, ProfileChangeForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    success_url = "/admin"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        print(form.is_bound)
        if form.is_valid():
            user = form.save()
            # user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            user.profile.is_corporate = form.cleaned_data.get("is_corporate")
            user.profile.avatar = form.cleaned_data.get("avatar")
            user.profile.save()
            login(request, user)
            return redirect("index")
        context = dict()
        print(context)
        context["form"] = form
        print(form.fields)
        print(form)
        print(context)
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
            return redirect("login")
        login(request, user)
        # if next:
        #     return redirect(next)
        return redirect("account", pk=user.pk)


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


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'partial/partial_user_change.html'
    context_object_name = 'user_obj'
    data = dict()

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.data
        data['html_forms'] = render_to_string(self.template_name, self.get_context_data(), request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form, request)
        else:
            return self.form_invalid(form, profile_form, request)

    def form_valid(self, form, profile_form, request):
        self.object = form.save()
        profile_form.save()
        data = self.data
        data['forms_are_valid'] = True
        user_obj = self.object
        data['html_user_detail'] = render_to_string("user_detail.html", {"user_obj": user_obj})
        return JsonResponse(data)

    def form_invalid(self, form, profile_form, request):
        data = self.data
        data['forms_are_valid'] = False
        context = self.get_context_data(form=form, profile_form=profile_form)
        data['html_forms'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)
