from http import HTTPStatus

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from portfolios import factories

from .forms.login_form import CustomLoginForm
from .forms.register_form import UserRegisterForm
from .models import Profile


class UsersTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        factories.UserFactory.reset_sequence(0, force=True)
        self.user = factories.UserFactory()

    def test_new_user_register_function(self):
        """Test if a new user has been created correctly."""
        response = self.client.post(
            reverse("register"),
            data={
                "username": "NewUser0",
                "email": "test@test.pl",
                "password1": "NewTest1234",
                "password2": "NewTest1234",
            },
        )
        new_user = User.objects.get(username="NewUser0")
        self.assertEqual(new_user.username, "NewUser0")

    def test_should_not_create_the_same_users(self):
        """Test if app does not allow to create two accounts with the same username and too common password"""
        form = UserRegisterForm(
            data={
                "username": "TestUser0",
                "email": "test@test.pl",
                "password1": "test1234",
                "password2": "test1234",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["username"], ["A user with that username already exists."]
        )
        self.assertEqual(form.errors["password2"], ["This password is too common."])

    def test_if_user_can_log_in(self):
        """Test if a user can log in to the app and is redirect to the home page"""
        response = self.client.post(
            reverse("login"),
            data={"username": "TestUser0", "password": "test1234"},
            follow=True,
        )
        self.assertTemplateUsed(response, "dashboard/index.html")
        self.assertRedirects(response, expected_url="/", status_code=HTTPStatus.FOUND)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_form_credentials_check(self):
        """Test if a user can not log in with wrong username and/or password."""
        form = CustomLoginForm(
            data={"username": "WrongUserName", "password": "WrongPassword"}
        )
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.errors, [])
