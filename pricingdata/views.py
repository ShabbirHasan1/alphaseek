
from django.shortcuts import render
from overall.views import cleanstring
import csv
import os
import requests
import re
# from lxml.html import document_fromstring
from datetime import date, timedelta
from pathlib import Path

path = os.path.dirname(os.path.realpath(__file__))


from nsetools import Nse
import yfinance as yf
from pricingdata.models import *

test_mode = False
no_run = 3


class ExchangeClass():
    # Creates exchange in the database
    def create_exchange(exchange_name,exchange_code,exchange_country,exchange_timezone,exchange_timezone_short,
    timezone_gmt_off_milliseconds
    ):
        error = False
        success = False
        error_message_list = []
        output = Exchange.objects.none()
        message = "Request Recieved"

        exchange = Exchange.objects.filter(exchange_code=exchange_code)
        if exchange.count() > 0 :
            message = "Exchange Already Exists!"        
            output = exchange
            success = False
            error = False
        else:
            exchange_new = Exchange.objects.create(
                exchange_name = exchange_name
                ,exchange_code = exchange_code
                ,exchange_country = exchange_country
                ,exchange_timezone = exchange_timezone
                ,exchange_timezone_short = exchange_timezone_short
                ,timezone_gmt_off_milliseconds = timezone_gmt_off_milliseconds
            )
            output = [exchange_new]
            success = True
            message = "Exchange Created!"
            error = False

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}


# NSE Data Update from NSE website

class NseIndia:
    # getting all equities from NSE
    def update_all_equity():
        error = False
        success = False
        error_message_list = []
        output = {}
        message = "Request Recieved"
        stocks_csv_url = 'http://www1.nseindia.com/content/equities/EQUITY_L.csv'

        with requests.Session() as s:
            try:
                download = s.get(stocks_csv_url)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                my_list = list(cr)
            except:
                error_message_list.append('Download Failure CSV!')
                error = True
                message = "Error Found! Please refer list"
                success = False

            if not error:
                count = 0 
                if (my_list[0][6] == " ISIN NUMBER" and my_list[0][0] == "SYMBOL" and my_list[0][1] == "NAME OF COMPANY"):
                    for row in my_list:
                        if count > 0:
                            company = Company.objects.filter(isin_no=row[6])
                            if company.count() > 0 :
                                company = company[0]
                                company.name = row[1],
                                company.nse_ticker = row[0]
                                company.is_listed_nse = True
                            else:
                                company = Company.objects.create(
                                    name = cleanstring(row[1].lower())
                                    ,isin_no = row[6]
                                    ,nse_ticker = row[0]
                                    ,is_listed_nse=True
                                )
                        count = count + 1
                    output = Company.objects.all()
                    success = True
                    error = False
                    message = "Companies Updated"
                else:
                    success = False
                    error = True
                    message = "Error Found! Please refer list"
                    error_message_list = "check incoming data format!"

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    # Updating one NSE ticker price data

    def update_historic_data(asset,date_check,period="max",force_period=False):
        error = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        
        company = Company.objects.filter(nse_ticker=asset.upper())
        exchange = Exchange.objects.filter(exchange_code="NSE")[0]
        yesterday = date.today() -  timedelta(days=1)
        if company.count() > 0:
            company = company[0]
            companyTotalData = yf.Ticker((asset.upper() + ".NS"))
            period = period
            if not force_period:
                if company.nse_price_update_db_date:
                    day_diff = (company.nse_price_update_db_date - date.today()).days
                    if day_diff >= 300:
                        period = "max"
                    elif day_diff >= 140 and day_diff < 300:
                        period = "1y"
                    elif day_diff >= 80 and day_diff < 140:
                        period = "6mo"
                    elif day_diff >= 28 and day_diff < 80:
                        period = "3mo"
                    elif day_diff >= 5 and day_diff < 28:
                        period = "1mo"                            
                    else:
                        period = "5d"                            
                else:
                    period = period
            try:
                companyPriceData = companyTotalData.history(period=period)
                index = companyPriceData.reset_index()['Date']
                total_len = len(index)
                for i in range(total_len):
                    if date_check:
                        if TickerHistoricDay.objects.filter(company = company,exchange=exchange,date = index[i]).count() > 0 or index[i] > yesterday:
                            pass
                            print(asset + " passed " + str(index[i]))    

                        # new_path_2 = os.path.join(path, 'filesdownloaded', exchange.exchange_code + "_" +asset.upper() + "_" + str(index[i])[:10] + ".tickerdata")
                        # if Path(new_path_2).is_file():
                            # pass
                        else:
                            tick = TickerHistoricDay.objects.create(
                                company      = company
                                ,exchange    = exchange
                                ,date        = index[i]
                                ,price_high  = companyPriceData['High'][i]
                                ,price_low   = companyPriceData['Low'][i]
                                ,price_close = companyPriceData['Close'][i]
                                ,price_open  = companyPriceData['Open'][i]
                                ,volume      = companyPriceData['Volume'][i]
                                ,dividends   = companyPriceData['Dividends'][i]
                                ,stock_split = companyPriceData['Stock Splits'][i]
                            )
                            output = output.append(tick)
                    else:
                        tick = TickerHistoricDay.objects.create(
                                company      = company
                                ,exchange    = exchange
                                ,date        = index[i]
                                ,price_high  = companyPriceData['High'][i]
                                ,price_low   = companyPriceData['Low'][i]
                                ,price_close = companyPriceData['Close'][i]
                                ,price_open  = companyPriceData['Open'][i]
                                ,volume      = companyPriceData['Volume'][i]
                                ,dividends   = companyPriceData['Dividends'][i]
                                ,stock_split = companyPriceData['Stock Splits'][i]
                            )
                        # new_path = os.path.join(path, 'filesdownloaded', exchange.exchange_code + "_" +asset.upper() + "_" + str(index[i])[:10] + ".tickerdata")
                        # with open(new_path , 'w') as fp: 
                        #     pass                        
                        output = output.append(tick)
                error = False
                success = True
                message = "Historical Data Scraped! " + asset 
                
            except:
                output = []
                error = True
                success = False
                message = "Data Download error " + asset
                error_message_list.append('Download failure '+ asset)
        else:
            error = True
            success = False
            message = "Please check asset code"
            error_message_list.append("Invalid asset code")
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    # updating all ticker price data

    def update_all_historic_ticker(partial=False,date_check=False):
        error   = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        if partial:
            companies = Company.objects.filter(is_listed_nse=True,nse_tracker=True)
        else:
            companies = Company.objects.filter(is_listed_nse=True)
        total_companies = len(companies)
        company_scraped = 0 
        if test_mode:
            companies = [companies[0]]


        for com in companies:
            out = NseIndia.update_historic_data(asset = com.nse_ticker,date_check=date_check)
            if out['error']:
                output.append(out['output'])
                error_message_list.extend(out['error_message_list'])
                print(out['message'])
            else:
                com.nse_tracker = True
                com.nse_price_update_db_date = date.today()
                com.save()
                output.append(out['output'])
                error_message_list.extend(out['error_message_list'])
                company_scraped = company_scraped + 1
                print(out['message'] + " | "+ str(company_scraped) + "/" + str(total_companies))
        if len(error_message_list) == 0:
            success = True
            error = False
            message = "Historical data scraped!"
        else:
            success = False
            error = True
            message = "Found errors! Check the error list!"
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

        
