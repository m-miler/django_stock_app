from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from users.forms.login_form import CustomLoginForm
from users.forms.reset_password_form import CustomPasswordResetForm
from users.forms.reset_password_confirmation_form import CustomPasswordConfirmationForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('register/', user_views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(authentication_form=CustomLoginForm,
                                      template_name='users/login.html'),
         name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm,
                                              template_name='users/password_reset_form.html'),
         name='password_reset'),

    path('accounts/password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('accounts/reset/done',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('accounts/password/reset/<str:uidb64>/<str:token>',
         auth_views.PasswordResetConfirmView.as_view(form_class=CustomPasswordConfirmationForm,
                                                     template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
