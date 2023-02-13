from decimal import Decimal

from django.conf import settings
from django.db import models

from ..models.companies import StockCompanies


class StockPrices(models.Model):
    company_abbreviation = models.ForeignKey(
        StockCompanies,
        to_field="company_abbreviation",
        on_delete=models.CASCADE,
        help_text="Company Abbreviation",
    )
    date = models.DateField(help_text="Stock Price Date")
    open_price = models.DecimalField(
        help_text="Day Open Price", max_digits=15, decimal_places=2
    )
    max_price = models.DecimalField(
        help_text="Day Max Price", max_digits=15, decimal_places=2
    )
    min_price = models.DecimalField(
        help_text="Day Min Price", max_digits=15, decimal_places=2
    )
    close_price = models.DecimalField(
        help_text="Day Close Price", max_digits=15, decimal_places=2
    )
    volume = models.BigIntegerField(help_text="Day Volume")

    def __str__(self):
        return f"{self.company_abbreviation.company_abbreviation}_{self.date.strftime('%Y-%m-%d')}"

    def get_weekly_price(self, field_name) -> Decimal or None:
        """Function to fetch the last week price."""
        last_week_price = StockPrices.objects.filter(
            models.Q(date=settings.LAST_WEEK_END)
            & models.Q(
                company_abbreviation__company_abbreviation=self.company_abbreviation
            )
        ).first()
        if not last_week_price:
            return None

        current_value = getattr(self, field_name)
        last_week_value = getattr(last_week_price, field_name)
        weekly_change = (current_value - last_week_value) / current_value
        return (Decimal(weekly_change) * 100).quantize(Decimal("0.01"))

    @property
    def close_weekly_change(self) -> Decimal or None:
        """Property calculates the weekly percentage change for close_price."""
        return self.get_weekly_price("close_price")

    @property
    def open_weekly_change(self):
        """Property calculates the weekly percentage change for open_price."""
        return self.get_weekly_price("open_price")

    @property
    def max_weekly_change(self):
        """Property calculates the weekly percentage change for max_price."""
        return self.get_weekly_price("max_price")

    @property
    def min_weekly_change(self):
        """Property calculates the weekly percentage change for min_price."""
        return self.get_weekly_price("min_price")

    @property
    def volume_weekly_change(self):
        """Property calculates the weekly percentage change for volume."""
        return self.get_weekly_price("volume")
