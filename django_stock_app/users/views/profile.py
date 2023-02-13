from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from portfolios.models.portfolio_model import Portfolio
from users.forms.profile_update_form import ProfileUpdateForm, UserUpdateForm


def profile(request):
    """Function to render portfolio template."""
    portfolios = Portfolio.objects.filter(user__username=request.user.username).all()
    return render(request, "users/profile.html", context={"portfolios": portfolios})


@login_required
def edit_profile(request):
    portfolios = Portfolio.objects.filter(user__username=request.user.username).all()
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile's been updated!")
            redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request,
        "users/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "portfolios": portfolios,
        },
    )
