from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


class Portfolio(models.Model):
    portfolio_id = models.CharField(
        max_length=150,
        help_text="Portfolio primary key user_portfolio_name",
        unique=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Portfolio owner"
    )
    name = models.CharField(max_length=20, help_text="User portfolio name")
    create_date = models.DateField(
        auto_now_add=True, help_text="Date of portfolio creation"
    )
    balance = models.DecimalField(
        default=10000.00,
        max_digits=15,
        decimal_places=2,
        help_text="Start balance 10k PLN",
    )

    def get_absolute_url(self):
        return reverse("portfolio-detail", kwargs={"portfolio": self.name})

    @property
    def portfolio_days(self) -> int:
        """Property calculates number of days since portfolio has been created."""
        portfolio_days = datetime.today().date() - self.create_date
        return portfolio_days.days
