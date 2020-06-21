from datascrape import views as data_code
from datetime import datetime

def daily_nse_pricing_scrape():
    print('ran daily_nse_pricing_scrape')
    timestart = str(datetime.now())
    print('start time - ' + timestart)
    data_code.NSEIndia.update_all_historic_ticker(date_check=True)
    data_code.IndexClass.update_all_historic_index(date_check=True)
    timeend = str(datetime.now())
    print('end time - ' + timeend)

def fresh_download_nse_pricing():
    print('ran fresh_download_nse_pricing')
    timestart = str(datetime.now())
    print('start time - ' + timestart)
    data_code.NSEIndia.update_all_historic_ticker(nse_tracker=True)
    timeend = str(datetime.now())
    print('end time - ' + timeend)