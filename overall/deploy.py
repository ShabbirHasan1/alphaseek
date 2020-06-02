from pricingdata.views import *
from pricingdata.models import *


# <<<< ------ Creating NSE Exchange ------>>>>
Exchange.objects.all().delete()
ExchangeClass.create_exchange(            
            exchange_name = 'National Stock Exchange of India'
            ,exchange_code = 'NSE'
            ,exchange_country = 'India'
            ,exchange_timezone = 'Asia/Kolkata'
            ,exchange_timezone_short = 'IST'
            ,timezone_gmt_off_milliseconds = 19800000
)

# <<<< ------ Download all NSE tickers ------>>>>
Company.objects.all().delete()
NseIndia.update_all_equity()


# <<<< ------ Download all historic data ------>>>>
TickerHistoricDay.objects.all().delete()
NseIndia.update_all_historic_ticker()










