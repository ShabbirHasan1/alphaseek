
from django.shortcuts import render
from overall.views import cleanstring
import csv
import os
import requests
import re
# from lxml.html import document_fromstring
from datetime import date, timedelta
from pathlib import Path
from nsetools import Nse
import yfinance as yf
from datascrape.models import *

path = os.path.dirname(os.path.realpath(__file__))
test_mode = False
no_run = 3

index_list = [
    'BSESN',
    'NSEI'
]

class ExchangeClass():
    # Creates exchange in the database
    def create_exchange(exchange_name,exchange_code,exchange_country,exchange_timezone,exchange_timezone_short,timezone_gmt_off_milliseconds,exchange_currency):
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
                ,exchange_currency = exchange_currency
            )
            output = [exchange_new]
            success = True
            message = "Exchange Created!"
            error = False

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}


# NSE Data Update from NSE website

class IndexClass():
    def create_index(name,ticker,exchange_code):
        error = False
        success = False
        error_message_list = []
        output = Index.objects.none()
        message = "Request Recieved"
        if exchange_code:
            exchange = Exchange.objects.filter(exchange_code=exchange_code)
            if exchange:
                exchange = exchange[0]
            else:
                error = True
                success = False
                message = "Incorrect exchange code "

        else:
            error = True
            success = False
            message = "No exchange code mentioned"

        if not error:
            index = Index.objects.filter(name=name.lower())
            if index.count() > 0 :
                message = "Index Already Exists!"        
                output = index
                success = False
                error = False
            else:
                index_new = Index.objects.create(
                    name = name
                    ,ticker = ticker
                    ,exchange = exchange
                )
                output = [index_new]
                success = True
                message = "Exchange Created!"
                error = False

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def download_historic_index(index_code,date_check):
        error = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        
        indexasset = Index.objects.filter(ticker=index_code.upper())
        # exchange = Exchange.objects.filter(exchange_code=exchange_code)[0]
        yesterday = date.today() -  timedelta(days=1)
        period_run = True
    
        if indexasset.count() > 0:
            indexasset = indexasset[0]
            indexTotalData = yf.Ticker(("^" + index_code.upper()))
            period = "max"
            
            if indexasset.price_update_date:
                day_diff = (date.today() - indexasset.price_update_date).days + 4
                start_date = str(date.today() -  timedelta(days=day_diff))
                end_date = str(date.today())
                period_run = False                    
            try:
                print(("^" + index_code.upper()))
                if period_run:
                    indexPriceData = yf.download(("^" + index_code.upper()),period=period)
                else:
                    indexPriceData = yf.download(("^" + index_code.upper()),start=start_date,end=end_date)
                print('here')
                index = indexPriceData.reset_index()['Date']
                total_len = len(index)
                for i in range(total_len):
                    if date_check:
                        if IndexHistoricDay.objects.filter(index = indexasset, date = index[i]).count() > 0 or index[i] > yesterday:
                            print(index_code + " passed " + str(index[i]))    
                        else:
                            tick = IndexHistoricDay.objects.create(
                                index      = indexasset
                                ,exchange    = indexasset.exchange
                                ,date        = index[i]
                                ,price_high  = indexPriceData['High'][i]
                                ,price_low   = indexPriceData['Low'][i]
                                ,price_close = indexPriceData['Close'][i]
                                ,price_open  = indexPriceData['Open'][i]
                                ,price_close_adjusted = indexPriceData['Adj Close'][i]
                                ,volume      = indexPriceData['Volume'][i]
                            )
                            # output = output.append(tick)
                    else:
                        tick = IndexHistoricDay.objects.create(
                                index      = indexasset
                                ,exchange    = indexasset.exchange
                                ,date        = index[i]
                                ,price_high  = indexPriceData['High'][i]
                                ,price_low   = indexPriceData['Low'][i]
                                ,price_close = indexPriceData['Close'][i]
                                ,price_open  = indexPriceData['Open'][i]
                                ,price_close_adjusted = indexPriceData['Adj Close'][i]
                                ,volume      = indexPriceData['Volume'][i]          
                                )
                        # print(tick)
                        # output = output.append(tick)
                
                error = False
                success = True
                message = "Historical Data Scraped! " + index_code.upper() 
                indexasset.price_update_date = date.today()
                indexasset.save()

            except:
                output = []
                error = True
                success = False
                message = "Data Download error " + index_code.upper() 
                error_message_list.append('Download failure '+ index_code.upper() )
        else:
            error = True
            success = False
            message = "Company not found for the asset " + index_code.upper() 
            error_message_list.append("Company not found for the asset " + index_code.upper())
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def update_all_historic_index(date_check=False):
        error   = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        indexes = Index.objects.all().order_by('name')
        total_index = len(indexes)
        index_scraped = 0 
        if test_mode:
            indexes = [indexes[0],indexes[1]]
            # companies = [companies[0]]
        for ind in indexes:
            out = IndexClass.download_historic_index(index_code = ind.ticker,date_check=date_check)
            if out['error']:
                output.extend(out['output'])
                error_message_list.extend(out['error_message_list'])
                print(out['message'])
            else:
                output.extend(out['output'])
                error_message_list.extend(out['error_message_list'])
                index_scraped = index_scraped + 1
                print(out['message'] + " | "+ str(index_scraped) + "/" + str(total_index))
        if len(error_message_list) == 0:
            success = True
            error = False
            message = "Historical data scraped!"
        else:
            success = False
            error = True
            message = "Found errors! Check the error list!"
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}


class NSEIndia:
    # getting all equities from NSE
    def update_all_equity():
        error = False
        success = False
        error_message_list = []
        output = {}
        message = "Request Recieved"
        stocks_csv_url = 'http://www1.NSEIndia.com/content/equities/EQUITY_L.csv'

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

    def update_historic_data(asset,date_check):
        error = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        
        company = Company.objects.filter(nse_ticker=asset.upper())
        exchange = Exchange.objects.filter(exchange_code="NSE")[0]
        yesterday = date.today() -  timedelta(days=1)
        period_run = True
        if company.count() > 0:
            company = company[0]
            companyTotalData = yf.Ticker((asset.upper() + ".NS"))
            period = "max"
            
            if company.nse_price_update_db_date:
                day_diff = (date.today() - company.nse_price_update_db_date).days + 4
                start_date = str(date.today() -  timedelta(days=day_diff))
                end_date = str(date.today())
                period_run = False                    
            try:
                if period_run:
                    companyPriceData = yf.download((asset.upper() + ".NS"),period=period)
                else:
                    companyPriceData = yf.download((asset.upper() + ".NS"),start=start_date,end=end_date)
                companyDividendData = companyTotalData.get_dividends()
                companyStockSplitData = companyTotalData.get_splits()
                index = companyPriceData.reset_index()['Date']
                total_len = len(index)
                for i in range(total_len):
                    if date_check:
                        if TickerHistoricDay.objects.filter(company = company,exchange=exchange,date = index[i]).count() > 0 or index[i] > yesterday:
                            print(asset + " passed " + str(index[i]))    
                            pass
                        else:
                            tick = TickerHistoricDay.objects.create(
                                company      = company
                                ,exchange    = exchange
                                ,date        = index[i]
                                ,price_high  = companyPriceData['High'][i]
                                ,price_low   = companyPriceData['Low'][i]
                                ,price_close = companyPriceData['Close'][i]
                                ,price_open  = companyPriceData['Open'][i]
                                ,price_close_adjusted = companyPriceData['Adj Close'][i]
                                ,volume      = companyPriceData['Volume'][i]
                            )
                            # output = output.append(tick)
                    else:
                        tick = TickerHistoricDay.objects.create(
                                company      = company
                                ,exchange    = exchange
                                ,date        = index[i]
                                ,price_high  = companyPriceData['High'][i]
                                ,price_low   = companyPriceData['Low'][i]
                                ,price_close = companyPriceData['Close'][i]
                                ,price_open  = companyPriceData['Open'][i]
                                ,price_close_adjusted = companyPriceData['Adj Close'][i]
                                ,volume      = companyPriceData['Volume'][i]
                            )
                        # print(tick)
                        # output = output.append(tick)
                
                index1 = companyDividendData.reset_index()['Date']
                total_div = len(index1)
                
                for j in range(total_div):
                    if company.nse_price_update_db_date:
                        if (company.nse_price_update_db_date -  timedelta(days=2)) > index1[j]:
                            pass
                        else:
                            # print('1d')
                            # print(companyDividendData[j])

                            d_price_update = TickerHistoricDay.objects.filter(company=company,exchange=exchange,date=index1[j])[0]
                            d_price_update.dividends = companyDividendData[j]
                            d_price_update.save()
                    else:
                        # print('2d')
                        # print(companyDividendData[j])
                        d_price_update = TickerHistoricDay.objects.filter(company=company,exchange=exchange,date=index1[j])[0]
                        d_price_update.dividends = companyDividendData[j]
                        d_price_update.save()

                    
                index2 = companyStockSplitData.reset_index()['Date']
                total_split = len(index2)
                
                for k in range(total_split):
                    if company.nse_price_update_db_date:
                        if (company.nse_price_update_db_date -  timedelta(days=2)) > index2[k]:
                            pass
                        else:
                            # print('1')
                            # print(companyStockSplitData[k])
                            s_price_update = TickerHistoricDay.objects.filter(company=company,exchange=exchange,date=index2[k])[0]
                            s_price_update.stock_split = companyStockSplitData[k]
                            s_price_update.save()
                    else:
                        # print('2')
                        # print(companyStockSplitData[k])
                        s_price_update = TickerHistoricDay.objects.filter(company=company,exchange=exchange,date=index2[k])[0]
                        s_price_update.stock_split = companyStockSplitData[k]
                        s_price_update.save()
                    
                error = False
                success = True
                message = "Historical Data Scraped! " + asset 
                company.nse_tracker = True
                company.nse_price_update_db_date = date.today()
                company.save()
            except:
                output = []
                error = True
                success = False
                message = "Data Download error " + asset
                error_message_list.append('Download failure '+ asset)
        else:
            error = True
            success = False
            message = "Company not found for the asset " + asset.upper()
            error_message_list.append("Company not found for the asset " + asset.upper())
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    # updating all ticker price data

    def update_all_historic_ticker(date_check=False,nse_tracker=False):
        error   = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        if nse_tracker:
            companies = Company.objects.filter(is_listed_nse=True,nse_tracker=False).order_by('name')
        else:
            companies = Company.objects.filter(is_listed_nse=True).order_by('name')
        total_companies = len(companies)
        company_scraped = 0 
        if test_mode:
            companies = [companies[0],companies[1],companies[2]]
            # companies = [companies[0]]
        for com in companies:
            out = NSEIndia.update_historic_data(asset = com.nse_ticker,date_check=date_check)
            if out['error']:
                output.extend(out['output'])
                error_message_list.extend(out['error_message_list'])
                print(out['message'])
            else:
                output.extend(out['output'])
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

        
