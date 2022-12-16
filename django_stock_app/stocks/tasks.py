from celery import shared_task
import datetime
from stocks.models.companies_model import StockCompanies
from api.serializers.stock_price_serializer import StockPricesSerializer
import requests


@shared_task
def price_db_update(*args, **kwargs):
    # Function explanation

    companies = StockCompanies.objects.values('company_abbreviation')
    start_day = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    db_columns = ['date', 'open_price', 'max_price', 'min_price', 'close_price', 'volume']

    for abbreviation in companies:
        company = abbreviation.get('company_abbreviation')
        url = f'https://stooq.pl/q/d/l/?s={company}&d1={start_day}&d2={start_day}&i=d'
        data = {'company_abbreviation': company}

        response = requests.get(url=url).content.decode('utf-8').strip().split('\r\n')

        data.update(dict(zip(db_columns, response[1].split(','))))

        serializer = StockPricesSerializer(data=data)
        serializer.is_valid()
        serializer.save()

