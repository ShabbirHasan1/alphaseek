from django.shortcuts import render
from datascrape.models import *
import pandas as pd
from dataprep.models import *
import datetime as dt
from datetime import date, timedelta
import math
import numpy as np
# Create your views here

test_mode = True
no_run = 3

class ReturnCalculate:
    def calculate_return(company,exchange):
        error = False
        success = False
        error_message_list = []
        output = {}
        output['daily_return'] = []
        output['monthly_return'] = []
        # message = "Request Recieved"
        messagedaily = "Daily Request Recieved"
        messagemonthly = "Monthly Request Recieved"
        date_today = date.today()
        asset_df = None
        asset_df_new = None
        if exchange == "NSE":
            asset = company.nse_ticker
        


        if company:
            # company = company[0]
            last_db_update_date = company.nse_return_update_date
        
            
            if last_db_update_date != None:
                fromdate = last_db_update_date - timedelta(days=600)
                assetdata = TickerHistoricDay.objects.filter(company=company,date__range=[str(fromdate), str(date_today)]).order_by('date')
            else:
                assetdata = TickerHistoricDay.objects.filter(company=company).order_by('date')
            
            if assetdata.count() > 0:
                date_list  = list(map(lambda x : str(x.date),assetdata))
                price_list = list(map(lambda x : float(x.price_close_adjusted),assetdata))

                exchange = assetdata[0].exchange
                
                date_price = {
                            'Price': price_list
                            }
                
            
                try:                    
                    asset_df = pd.DataFrame(date_price, columns = ['Price'], index=pd.to_datetime(date_list))
                    asset_daily_return_1d  =  asset_df['Price'].pct_change(1)
                    asset_daily_return_2d  =  asset_df['Price'].pct_change(2)
                    asset_daily_return_3d  =  asset_df['Price'].pct_change(3)
                    asset_daily_return_4d  =  asset_df['Price'].pct_change(4)
                    asset_daily_return_5d  =  asset_df['Price'].pct_change(5)
                    asset_daily_return_6d  =  asset_df['Price'].pct_change(6)
                    asset_daily_return_7d  =  asset_df['Price'].pct_change(7)
                    asset_daily_return_14d =  asset_df['Price'].pct_change(14)
                    asset_daily_return_21d =  asset_df['Price'].pct_change(21)
                    asset_daily_return_25d =  asset_df['Price'].pct_change(25)

                    total_len = len(price_list)
                    for i in range(total_len):
                        daily_return_check = DailyReturn.objects.filter(company=company,exchange=exchange,date=date_list[i])
                        if daily_return_check.count() > 0:
                            pass
                        else:
                            assetdreturn = DailyReturn.objects.create(
                            company       = company
                            ,exchange     = exchange
                            ,date         = date_list[i]
                            ,return_1d    = asset_daily_return_1d[i] if str(asset_daily_return_1d[i]) != 'nan'  else None   
                            ,return_2d    = asset_daily_return_2d[i] if str(asset_daily_return_2d[i]) != 'nan'  else None   
                            ,return_3d    = asset_daily_return_3d[i] if str(asset_daily_return_3d[i]) != 'nan'  else None   
                            ,return_4d    = asset_daily_return_4d[i] if str(asset_daily_return_4d[i]) != 'nan'  else None   
                            ,return_5d    = asset_daily_return_5d[i] if str(asset_daily_return_5d[i]) != 'nan'  else None   
                            ,return_6d    = asset_daily_return_6d[i] if str(asset_daily_return_6d[i]) != 'nan'  else None   
                            ,return_7d    = asset_daily_return_7d[i] if str(asset_daily_return_7d[i]) != 'nan'  else None   
                            ,return_14d   = asset_daily_return_14d[i] if str(asset_daily_return_14d[i]) != 'nan'  else None   
                            ,return_21d   = asset_daily_return_21d[i] if str(asset_daily_return_21d[i]) != 'nan'  else None   
                            ,return_25d   = asset_daily_return_25d[i] if str(asset_daily_return_25d[i]) != 'nan'  else None   
                                )  
                            # output['daily_return'].append(assetdreturn)
                    # output['daily_return'] = DailyReturn.objects.filter(company = company)
                    error = False
                    success = True
                    messagedaily = "Daily Returns calculated for " + asset 
                    # print("Daily Returns calculated for " + asset )
                except:
                    error = True
                    success = False
                    messagedaily = "Daily Return calculation error " + asset
                    error_message_list.append('Daily return calculation failure '+ asset)    
                
                

                try:
                    asset_df_new = asset_df.resample('M').ffill()
                    asset_monthly_return_1m   =  asset_df_new['Price'].pct_change(1)
                    asset_monthly_return_2m   =  asset_df_new['Price'].pct_change(2)
                    asset_monthly_return_3m   =  asset_df_new['Price'].pct_change(3)
                    asset_monthly_return_4m   =  asset_df_new['Price'].pct_change(4)
                    asset_monthly_return_5m   =  asset_df_new['Price'].pct_change(5)
                    asset_monthly_return_6m   =  asset_df_new['Price'].pct_change(6)
                    asset_monthly_return_7m   =  asset_df_new['Price'].pct_change(7)
                    asset_monthly_return_8m   =  asset_df_new['Price'].pct_change(8)
                    asset_monthly_return_9m   =  asset_df_new['Price'].pct_change(9)
                    asset_monthly_return_10m  =  asset_df_new['Price'].pct_change(10)
                    asset_monthly_return_11m  =  asset_df_new['Price'].pct_change(11)
                    asset_monthly_return_12m  =  asset_df_new['Price'].pct_change(12)
                    asset_monthly_return_13m  =  asset_df_new['Price'].pct_change(13)
                    asset_monthly_return_14m  =  asset_df_new['Price'].pct_change(14)
                    asset_monthly_return_15m  =  asset_df_new['Price'].pct_change(15)
                    asset_monthly_return_16m  =  asset_df_new['Price'].pct_change(16)
                    asset_monthly_return_17m  =  asset_df_new['Price'].pct_change(17)
                    asset_monthly_return_18m  =  asset_df_new['Price'].pct_change(18)
                    
                    total_len = len(asset_df_new)
                    
                    for i in range(total_len):
                        date_check = dt.datetime.utcfromtimestamp(asset_df_new.index[i].value//1000000000).strftime("%Y-%m-%d")
                        monthly_return_check = MonthlyReturn.objects.filter(company=company,exchange=exchange,date=date_check)
                        if monthly_return_check.count() > 0:
                            pass
                        else:
                            assetmreturn = MonthlyReturn.objects.create(
                                company       = company
                                ,exchange     = exchange
                                ,date         = dt.datetime.utcfromtimestamp(asset_df_new.index[i].value//1000000000).strftime("%Y-%m-%d")
                                ,return_1m    = asset_monthly_return_1m[i] if str(asset_monthly_return_1m[i]) != 'nan'  else None   
                                ,return_2m    = asset_monthly_return_2m[i] if str(asset_monthly_return_2m[i]) != 'nan'  else None   
                                ,return_3m    = asset_monthly_return_3m[i] if str(asset_monthly_return_3m[i]) != 'nan'  else None   
                                ,return_4m    = asset_monthly_return_4m[i] if str(asset_monthly_return_4m[i]) != 'nan'  else None   
                                ,return_5m    = asset_monthly_return_5m[i] if str(asset_monthly_return_5m[i]) != 'nan'  else None   
                                ,return_6m    = asset_monthly_return_6m[i] if str(asset_monthly_return_6m[i]) != 'nan'  else None   
                                ,return_7m    = asset_monthly_return_7m[i] if str(asset_monthly_return_7m[i]) != 'nan'  else None   
                                ,return_8m    = asset_monthly_return_8m[i] if str(asset_monthly_return_8m[i]) != 'nan'  else None   
                                ,return_9m    = asset_monthly_return_9m[i] if str(asset_monthly_return_9m[i]) != 'nan'  else None   
                                ,return_10m   = asset_monthly_return_10m[i] if str(asset_monthly_return_10m[i]) != 'nan'  else None   
                                ,return_11m   = asset_monthly_return_11m[i] if str(asset_monthly_return_11m[i]) != 'nan'  else None   
                                ,return_12m   = asset_monthly_return_12m[i] if str(asset_monthly_return_12m[i]) != 'nan'  else None   
                                ,return_13m   = asset_monthly_return_13m[i] if str(asset_monthly_return_13m[i]) != 'nan'  else None   
                                ,return_14m   = asset_monthly_return_14m[i] if str(asset_monthly_return_14m[i]) != 'nan'  else None   
                                ,return_15m   = asset_monthly_return_15m[i] if str(asset_monthly_return_15m[i]) != 'nan'  else None   
                                ,return_16m   = asset_monthly_return_16m[i] if str(asset_monthly_return_16m[i]) != 'nan'  else None   
                                ,return_17m   = asset_monthly_return_17m[i] if str(asset_monthly_return_17m[i]) != 'nan'  else None   
                                ,return_18m   = asset_monthly_return_18m[i] if str(asset_monthly_return_18m[i]) != 'nan'  else None   
                                )  
                            # output['monthly_return'].append(assetmreturn)
                        # output['monthly_return'] = MonthlyReturn.objects.filter(company = company)
                        error = False
                        success = True
                        messagemonthly = "Monthly Returns calculated for " + asset 
                except:
                    error = True
                    success = False
                    messagemonthly = "Monthly Return calculation error " + asset
                    error_message_list.append('Monthly Return Calculation failure '+ asset)

                message = messagedaily + " | " + messagemonthly

            else:
                error = True
                success = False
                message = "Data not found for the " + asset
                error_message_list.append("Data not found for the " + asset)


        else:
            error = True
            success = False
            message = "Asset not found: " + asset
            error_message_list.append("Asset not found: " + asset)
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def calculate_all_returns(exchange='NSE'):
            error   = False
            success = False
            error_message_list = []
            output = []
            # output['monthly'] = []
            # output['daily'] = []
            message = "Request Recieved"
            if exchange =="NSE":
                if test_mode:
                    companies = Company.objects.filter(is_listed_nse=True,nse_tracker=True).order_by('name')
                else:
                    companies = Company.objects.filter(is_listed_nse=True)
                
                total_companies = len(companies)
                company_calculated = 0 
                

                for com in companies:
                    out = ReturnCalculate.calculate_return(company = com,exchange = exchange) 
                    output.append(out['output'])
                    error_message_list.extend(out['error_message_list']) 
                    com.nse_return_update_date = date.today()
                    com.save()
                    company_calculated = company_calculated + 1
                    # print(error_message_list)
                    print(out['message'] + " | "+ str(company_calculated) + "/" + str(total_companies))
                    
                if len(error_message_list) == 0:                
                    success = True
                    error = False
                    message = "Return Calculated!"
                else:
                    success = False
                    error = True
                    message = "Found errors! Check the error list!"
            return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def calculate_index_return(index):
        error = False
        success = False
        error_message_list = []
        output = {}
        output['daily_return'] = []
        output['monthly_return'] = []
        # message = "Request Recieved"
        messagedaily = "Daily Request Recieved"
        messagemonthly = "Monthly Request Recieved"
        date_today = date.today()
        asset_df = None
        asset_df_new = None
        # if exchange == "NSE":
        #     asset = company.nse_ticker
        


        if index:
            # company = company[0]
            last_db_update_date = index.return_update_date
        
            
            if last_db_update_date != None:
                fromdate = last_db_update_date - timedelta(days=600)
                assetdata = IndexHistoricDay.objects.filter(index=index,date__range=[str(fromdate), str(date_today)]).order_by('date')
            else:
                assetdata = IndexHistoricDay.objects.filter(index=index).order_by('date')
            
            if assetdata.count() > 0:
                date_list  = list(map(lambda x : str(x.date),assetdata))
                price_list = list(map(lambda x : float(x.price_close_adjusted),assetdata))

                exchange = assetdata[0].exchange
                
                date_price = {
                            'Price': price_list
                            }
                
            
                try:                    
                    asset_df = pd.DataFrame(date_price, columns = ['Price'], index=pd.to_datetime(date_list))
                    asset_daily_return_1d  =  asset_df['Price'].pct_change(1)
                    asset_daily_return_2d  =  asset_df['Price'].pct_change(2)
                    asset_daily_return_3d  =  asset_df['Price'].pct_change(3)
                    asset_daily_return_4d  =  asset_df['Price'].pct_change(4)
                    asset_daily_return_5d  =  asset_df['Price'].pct_change(5)
                    asset_daily_return_6d  =  asset_df['Price'].pct_change(6)
                    asset_daily_return_7d  =  asset_df['Price'].pct_change(7)
                    asset_daily_return_14d =  asset_df['Price'].pct_change(14)
                    asset_daily_return_21d =  asset_df['Price'].pct_change(21)
                    asset_daily_return_25d =  asset_df['Price'].pct_change(25)

                    total_len = len(price_list)
                    for i in range(total_len):
                        daily_return_check = IndexDailyReturn.objects.filter(index=index,exchange=exchange,date=date_list[i])
                        if daily_return_check.count() > 0:
                            pass
                        else:
                            assetdreturn = IndexDailyReturn.objects.create(
                            index       = index
                            ,exchange     = exchange
                            ,date         = date_list[i]
                            ,return_1d    = asset_daily_return_1d[i] if str(asset_daily_return_1d[i]) != 'nan'  else None   
                            ,return_2d    = asset_daily_return_2d[i] if str(asset_daily_return_2d[i]) != 'nan'  else None   
                            ,return_3d    = asset_daily_return_3d[i] if str(asset_daily_return_3d[i]) != 'nan'  else None   
                            ,return_4d    = asset_daily_return_4d[i] if str(asset_daily_return_4d[i]) != 'nan'  else None   
                            ,return_5d    = asset_daily_return_5d[i] if str(asset_daily_return_5d[i]) != 'nan'  else None   
                            ,return_6d    = asset_daily_return_6d[i] if str(asset_daily_return_6d[i]) != 'nan'  else None   
                            ,return_7d    = asset_daily_return_7d[i] if str(asset_daily_return_7d[i]) != 'nan'  else None   
                            ,return_14d   = asset_daily_return_14d[i] if str(asset_daily_return_14d[i]) != 'nan'  else None   
                            ,return_21d   = asset_daily_return_21d[i] if str(asset_daily_return_21d[i]) != 'nan'  else None   
                            ,return_25d   = asset_daily_return_25d[i] if str(asset_daily_return_25d[i]) != 'nan'  else None   
                                )  
                            # output['daily_return'].append(assetdreturn)
                    # output['daily_return'] = DailyReturn.objects.filter(company = company)
                    error = False
                    success = True
                    messagedaily = "Daily Returns calculated for " + index.ticker 
                    # print("Daily Returns calculated for " + asset )
                except:
                    error = True
                    success = False
                    messagedaily = "Daily Return calculation error " + index.ticker 
                    error_message_list.append('Daily return calculation failure '+ index.ticker )    
                
                

                try:
                    asset_df_new = asset_df.resample('M').ffill()
                    asset_monthly_return_1m   =  asset_df_new['Price'].pct_change(1)
                    asset_monthly_return_2m   =  asset_df_new['Price'].pct_change(2)
                    asset_monthly_return_3m   =  asset_df_new['Price'].pct_change(3)
                    asset_monthly_return_4m   =  asset_df_new['Price'].pct_change(4)
                    asset_monthly_return_5m   =  asset_df_new['Price'].pct_change(5)
                    asset_monthly_return_6m   =  asset_df_new['Price'].pct_change(6)
                    asset_monthly_return_7m   =  asset_df_new['Price'].pct_change(7)
                    asset_monthly_return_8m   =  asset_df_new['Price'].pct_change(8)
                    asset_monthly_return_9m   =  asset_df_new['Price'].pct_change(9)
                    asset_monthly_return_10m  =  asset_df_new['Price'].pct_change(10)
                    asset_monthly_return_11m  =  asset_df_new['Price'].pct_change(11)
                    asset_monthly_return_12m  =  asset_df_new['Price'].pct_change(12)
                    asset_monthly_return_13m  =  asset_df_new['Price'].pct_change(13)
                    asset_monthly_return_14m  =  asset_df_new['Price'].pct_change(14)
                    asset_monthly_return_15m  =  asset_df_new['Price'].pct_change(15)
                    asset_monthly_return_16m  =  asset_df_new['Price'].pct_change(16)
                    asset_monthly_return_17m  =  asset_df_new['Price'].pct_change(17)
                    asset_monthly_return_18m  =  asset_df_new['Price'].pct_change(18)
                    
                    total_len = len(asset_df_new)
                    
                    for i in range(total_len):
                        date_check = dt.datetime.utcfromtimestamp(asset_df_new.index[i].value//1000000000).strftime("%Y-%m-%d")
                        monthly_return_check = IndexMonthlyReturn.objects.filter(index=index,exchange=exchange,date=date_check)
                        if monthly_return_check.count() > 0:
                            pass
                        else:
                            assetmreturn = IndexMonthlyReturn.objects.create(
                                index       = index
                                ,exchange     = exchange
                                ,date         = dt.datetime.utcfromtimestamp(asset_df_new.index[i].value//1000000000).strftime("%Y-%m-%d")
                                ,return_1m    = asset_monthly_return_1m[i] if str(asset_monthly_return_1m[i]) != 'nan'  else None   
                                ,return_2m    = asset_monthly_return_2m[i] if str(asset_monthly_return_2m[i]) != 'nan'  else None   
                                ,return_3m    = asset_monthly_return_3m[i] if str(asset_monthly_return_3m[i]) != 'nan'  else None   
                                ,return_4m    = asset_monthly_return_4m[i] if str(asset_monthly_return_4m[i]) != 'nan'  else None   
                                ,return_5m    = asset_monthly_return_5m[i] if str(asset_monthly_return_5m[i]) != 'nan'  else None   
                                ,return_6m    = asset_monthly_return_6m[i] if str(asset_monthly_return_6m[i]) != 'nan'  else None   
                                ,return_7m    = asset_monthly_return_7m[i] if str(asset_monthly_return_7m[i]) != 'nan'  else None   
                                ,return_8m    = asset_monthly_return_8m[i] if str(asset_monthly_return_8m[i]) != 'nan'  else None   
                                ,return_9m    = asset_monthly_return_9m[i] if str(asset_monthly_return_9m[i]) != 'nan'  else None   
                                ,return_10m   = asset_monthly_return_10m[i] if str(asset_monthly_return_10m[i]) != 'nan'  else None   
                                ,return_11m   = asset_monthly_return_11m[i] if str(asset_monthly_return_11m[i]) != 'nan'  else None   
                                ,return_12m   = asset_monthly_return_12m[i] if str(asset_monthly_return_12m[i]) != 'nan'  else None   
                                ,return_13m   = asset_monthly_return_13m[i] if str(asset_monthly_return_13m[i]) != 'nan'  else None   
                                ,return_14m   = asset_monthly_return_14m[i] if str(asset_monthly_return_14m[i]) != 'nan'  else None   
                                ,return_15m   = asset_monthly_return_15m[i] if str(asset_monthly_return_15m[i]) != 'nan'  else None   
                                ,return_16m   = asset_monthly_return_16m[i] if str(asset_monthly_return_16m[i]) != 'nan'  else None   
                                ,return_17m   = asset_monthly_return_17m[i] if str(asset_monthly_return_17m[i]) != 'nan'  else None   
                                ,return_18m   = asset_monthly_return_18m[i] if str(asset_monthly_return_18m[i]) != 'nan'  else None   
                                )  
                            # output['monthly_return'].append(assetmreturn)
                        # output['monthly_return'] = MonthlyReturn.objects.filter(company = company)
                        error = False
                        success = True
                        messagemonthly = "Monthly Returns calculated for " + index.ticker 
                except:
                    error = True
                    success = False
                    messagemonthly = "Monthly Return calculation error " + index.ticker 
                    error_message_list.append('Monthly Return Calculation failure '+ index.ticker)

                message = messagedaily + " | " + messagemonthly

            else:
                error = True
                success = False
                message = "Data not found for the " + index.ticker 
                error_message_list.append("Data not found for the " + index.ticker )


        else:
            error = True
            success = False
            message = "Asset not found: " + index.ticker 
            error_message_list.append("Asset not found: " + index.ticker )
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def calculate_all_index_returns(date_check=True):
        error   = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        if test_mode:
            indexes = Index.objects.all().order_by('name')
            indexes = [indexes[0],indexes[1]]
        else:
            indexes = Index.objects.all()
        
        total_indexes = len(indexes)
        indexes_calculated = 0 
        

        for ind in indexes:
            out = ReturnCalculate.calculate_index_return(index = ind) 
            output.append(out['output'])
            error_message_list.extend(out['error_message_list']) 
            ind.return_update_date = date.today()
            ind.save()
            indexes_calculated = indexes_calculated + 1
            # print(error_message_list)
            print(out['message'] + " | "+ str(indexes_calculated) + "/" + str(total_indexes))
            
        if len(error_message_list) == 0:                
            success = True
            error = False
            message = "Return Calculated!"
        else:
            success = False
            error = True
            message = "Found errors! Check the error list!"
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

class UpdateTicker:
    def update_ticker(company, exchange):
        error = False
        success = False
        error_message_list = []
        output = {}
        message = "Request Recieved"
        price_data = TickerHistoricDay.objects.filter(exchange__exchange_code = exchange, company = company).order_by('-date')
        daily_return_data = DailyReturn.objects.filter(exchange__exchange_code = exchange, company = company).order_by('-date')
        monthly_return_data = MonthlyReturn.objects.filter(exchange__exchange_code = exchange, company = company).order_by('-date')
        date_list = list(map(lambda x : str(x.date)[:19],daily_return_data))
        return_list = list(map(lambda x : x.return_1d,daily_return_data))
        # date_list = list(dict.fromkeys(date_list))
        db_return = pd.DataFrame({'Date':date_list,'Return':return_list}, columns = ['Date','Return'])
        volatility = db_return['Return'].std() * math.sqrt(245)
        average_return = db_return['Return'].mean() * 245
        if exchange == "NSE":
            try:
                company.nse_trade_date           = price_data[0].date
                company.nse_price_high           = price_data[0].price_high
                company.nse_price_low            = price_data[0].price_low
                company.nse_price_close          = price_data[0].price_close
                company.nse_price_open           = price_data[0].price_open
                company.nse_price_close_adjusted = price_data[0].price_close_adjusted
                company.nse_volume               = price_data[0].volume
                company.nse_return_date          = daily_return_data[0].date
                company.nse_return_1d            = daily_return_data[0].return_1d
                company.nse_return_1m            = monthly_return_data[0].return_1m
                company.nse_return_1y            = monthly_return_data[0].return_12m
                company.nse_annualized_return    = average_return
                company.nse_annualized_vol       = volatility
                company.save()
                error = False
                success = True
                message = "Data updation complete for the  " + company.nse_ticker
            except:
                error = True
                success = False
                message = "Data updation error for the  " + company.nse_ticker
                error_message_list.append("Data updation error for the  " + company.nse_ticker)
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def update_all_company():
        error   = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        
        companies = Company.objects.filter(is_listed_nse = True).order_by('name')
        # total_indexes = len(indexes)
        companies_calculated = 0 
        total_companies = companies.count()
        for com in companies:
            out = UpdateTicker.update_ticker(company = com, exchange = "NSE") 
            output.append(out['output'])
            error_message_list.extend(out['error_message_list']) 
            companies_calculated = companies_calculated + 1
            print(out['message'] + " | "+ str(companies_calculated) + "/" + str(total_companies))
    
        if len(error_message_list) == 0:                
            success = True
            error = False
            message = "Company Updation Complete!"
        else:
            success = False
            error = True
            message = "Found errors! Check the error list!"
        return {'output':{},'message':message,'error':error,'error_message_list':error_message_list,'success':success}
            
    def update_index(index):
        error = False
        success = False
        error_message_list = []
        output = {}
        message = "Request Recieved"
        price_data = IndexHistoricDay.objects.filter(index = index).order_by('-date')
        daily_return_data = IndexDailyReturn.objects.filter(index = index).order_by('-date')
        monthly_return_data = IndexMonthlyReturn.objects.filter(index = index).order_by('-date')
        date_list = list(map(lambda x : str(x.date)[:19],daily_return_data))
        return_list = list(map(lambda x : x.return_1d,daily_return_data))
        # date_list = list(dict.fromkeys(date_list))
        db_return = pd.DataFrame({'Date':date_list,'Return':return_list}, columns = ['Date','Return'])
        volatility = db_return['Return'].std() * math.sqrt(245)
        average_return = db_return['Return'].mean() * 245
        # if exchange == "NSE":
        try:
            index.trade_date           = price_data[0].date
            index.price_high           = price_data[0].price_high
            index.price_low            = price_data[0].price_low
            index.price_close          = price_data[0].price_close
            index.price_open           = price_data[0].price_open
            index.price_close_adjusted = price_data[0].price_close_adjusted
            index.volume               = price_data[0].volume
            index.return_date          = daily_return_data[0].date
            index.return_1d            = daily_return_data[0].return_1d
            index.return_1m            = monthly_return_data[0].return_1m
            index.return_1y            = monthly_return_data[0].return_12m
            index.annualized_return    = average_return
            index.annualized_vol       = volatility
            index.save()
            error = False
            success = True
            message = "Data updation complete for the  " + index.ticker
        except:
            error = True
            success = False
            message = "Data updation error for the  " + index.ticker
            error_message_list.append("Data updation error for the  " + index.ticker)
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def update_all_index():
        error   = False
        success = False
        error_message_list = []
        output = []
        message = "Request Recieved"
        
        indexes = Index.objects.all().order_by('name')
        # total_indexes = len(indexes)
        indexes_calculated = 0 
        total_indexes = indexes.count()
        for ind in indexes:
            out = UpdateTicker.update_index(index = ind) 
            output.append(out['output'])
            error_message_list.extend(out['error_message_list']) 
            indexes_calculated = indexes_calculated + 1
            print(out['message'] + " | "+ str(indexes_calculated) + "/" + str(total_indexes))
    
        if len(error_message_list) == 0:                
            success = True
            error = False
            message = "Index Updation Complete!"

        else:
            success = False
            error = True
            message = "Found errors! Check the error list!"
        return {'output':{},'message':message,'error':error,'error_message_list':error_message_list,'success':success}







