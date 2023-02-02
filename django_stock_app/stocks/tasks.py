from celery import shared_task
import datetime
from .models.companies_model import StockCompanies
from api.serializers.stock_price_serializer import StockPricesSerializer
import requests

DB_COLUMNS = ['date', 'open_price', 'max_price', 'min_price', 'close_price', 'volume']


def get_stock_data(company: str, start_day) -> dict[str, str | int]:
    """
    Function with web scrapping code to get the stock price data.
    :param company: Company abbreviation passed from celery task
    :param start_day: Date from which we want to get data
    :return: dict
    """
    url = f'https://stooq.pl/q/d/l/?s={company}&d1={start_day}&d2={start_day}&i=d'
    data = {'company_abbreviation': company}

    response = requests.get(url=url).content.decode('utf-8').strip().split('\r\n')
    data.update(dict(zip(DB_COLUMNS, response[1].split(','))))
    return data


def save_data(company: str, start_day) -> None:
    """
    Function to save web scrapped data to the stock_price database.
    :param company: company abbreviation passed from celery task
    :param start_day: date from which we want to get data
    :return: None
    """
    data = get_stock_data(company, start_day)
    serializer = StockPricesSerializer(data=data)
    serializer.is_valid()
    serializer.save()


@shared_task
def price_db_update(*args: tuple[any, ...], **kwargs: any) -> None:
    """
    Celery task to web scrapping stock prices for each company in a stock database.
    Task starts automatically at 24 o'clock and get data form the previous day.
    """

    companies = StockCompanies.objects.values('company_abbreviation')
    start_day = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')

    for abbreviation in companies:
        company = abbreviation.get('company_abbreviation')
        save_data(company, start_day)


