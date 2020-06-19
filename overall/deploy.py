from datascrape.views import *
from datascrape.models import *
from dataprep.models import *
from dataprep.views import *
from strategytest.views import *

TickerHistoricDay.objects.all().delete()
Company.objects.all().delete()
Exchange.objects.all().delete()
DailyReturn.objects.all().delete()
MonthlyReturn.objects.all().delete()

# <<<< ------ Creating NSE Exchange ------>>>>

ExchangeClass.create_exchange(            
            exchange_name = 'National Stock Exchange of India'
            ,exchange_code = 'NSE'
            ,exchange_country = 'India'
            ,exchange_timezone = 'Asia/Kolkata'
            ,exchange_timezone_short = 'IST'
            ,timezone_gmt_off_milliseconds = 19800000
            ,exchange_currency = "INR"
)

# <<<< ------ Creating BSE Exchange ------>>>>
ExchangeClass.create_exchange(            
            exchange_name = 'Bombay Stock Exchange'
            ,exchange_code = 'BSE'
            ,exchange_country = 'India'
            ,exchange_timezone = 'Asia/Kolkata'
            ,exchange_timezone_short = 'IST'
            ,timezone_gmt_off_milliseconds = 19800000
            ,exchange_currency = "INR"
)


# <<<< ------ Download all NSE tickers ------>>>>
# NSEIndia.update_all_equity()


# <<<< ------ Download all historic data ------>>>>
# NSEIndia.update_all_historic_ticker()

# <<<< ------ Creating Indexes ------>>>>
# IndexClass.create_index(
#     name="Nifty 50",ticker="NSEI",exchange_code="NSE"
# )

# IndexClass.create_index(
#     name="Sensex",ticker="BSESN",exchange_code="BSE"
# )

# <<<< ------ Download all historic index data ------>>>>
# IndexClass.update_all_historic_index()

# <<<< ------ Compute equity returns ------>>>>
# ReturnCalculate.calculate_all_returns()

# <<<< ------ Compute index returns ------>>>>
# ReturnCalculate.calculate_all_index_returns()








