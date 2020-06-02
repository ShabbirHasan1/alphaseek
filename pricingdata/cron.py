from pricingdata import views as data_code

def daily_nse_pricing_scrape():
    print('ran daily_nse_pricing_scrape')
    # data_code.NseIndia.update_all_historic_ticker(partial=False,date_check=True)

def fresh_download_nse_pricing():
    print('ran fresh_download_nse_pricing')
    # data_code.NseIndia.update_all_historic_ticker()