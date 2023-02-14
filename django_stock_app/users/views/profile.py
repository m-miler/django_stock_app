from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, UpdateView
from portfolios.models.portfolio_model import Portfolio
from users.forms.profile_update_form import ProfileUpdateForm, UserUpdateForm


class Profile(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = "users/profile.html"

    def get_object(self, queryset=None, *args, **kwargs):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = {}
        context["portfolios"] = self.object
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    model = Portfolio
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None, *args, **kwargs):
        return self.model.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        profile_form = ProfileUpdateForm(
            self.request.POST, self.request.FILES, instance=self.request.user.profile
        )

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, "Your profile's been updated!")
            return redirect("profile")
        return redirect("profile")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserUpdateForm(instance=self.request.user)
        profile_form = ProfileUpdateForm(instance=self.request.user.profile)
        return render(
            self.request,
            "users/edit_profile.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "portfolios": self.object,
            },
        )
