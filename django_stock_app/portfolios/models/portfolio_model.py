from django.db import models
from datetime import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Portfolio(models.Model):
    portfolio_id = models.CharField(max_length=150, help_text='Portfolio primary key user_portfolio_name', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Portfolio owner')
    name = models.CharField(max_length=20, help_text='User portfolio name', unique=True)
    create_date = models.DateField(auto_now_add=True, help_text='Date of portfolio creation')
    balance = models.FloatField(default=10000, help_text='Start balance 10k PLN')

    def get_absolute_url(self):
        return reverse('portfolio-detail', kwargs={'portfolio': self.name})

    @property
    def portfolio_days(self):
        portfolio_days = datetime.today().date() - self.create_date
        return portfolio_days.days
