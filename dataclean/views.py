from django.shortcuts import render
from pricingdata.models import *
import pandas as pd
from dataclean.models import *
import datetime as dt
from datetime import date, timedelta
# Create your views here

test_mode = True
no_run = 3

class ReturnCalculate:
    def calculate_return(company,exchange,date_check=True):
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
                price_list = list(map(lambda x : float(x.price_close),assetdata))

                exchange = assetdata[0].exchange
                company = assetdata[0].company
                date_price = {
                            'Price': price_list
                            }
                asset_df = pd.DataFrame(date_price, columns = ['Price'], index=pd.to_datetime(date_list))
            
                try:                    
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
                            output['daily_return'].append(assetdreturn)
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
                
                asset_df_new = asset_df.resample('M').ffill()

                try:
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
                            output['monthly_return'].append(assetmreturn)
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

    def calculate_all_returns(exchange='NSE',date_check=True):
            error   = False
            success = False
            error_message_list = []
            output = []
            # output['monthly'] = []
            # output['daily'] = []
            message = "Request Recieved"
            if exchange =="NSE":
                if test_mode:
                    companies = Company.objects.filter(is_listed_nse=True,nse_ticker="20MICRONS")
                else:
                    companies = Company.objects.filter(is_listed_nse=True)
                
                total_companies = len(companies)
                company_calculated = 0 
                

                for com in companies:
                    # out1 = ReturnCalculate.daily_return(asset = com.nse_ticker,exchange="NSE")
                    # if out1['error']:
                    #     output['daily'].append(out1['output'])
                    #     error_message_list.append(out1['error_message_list'])
                    #     print(out1['message'])
                    # else:
                    #     output['daily'].append(out1['output'])
                    #     error_message_list.append(out1['error_message_list'])
                    #     company_calculated_d = company_calculated_d + 1
                    #     com.nse_daily_return_update_date = date.today()
                    #     com.save()
                    #     print(out1['message'] + " | "+ str(company_calculated_d) + "/" + str(total_companies))

                    # out2 = ReturnCalculate.monthly_return(asset = com.nse_ticker,exchange="NSE")
                    # if out2['error']:
                    #     output['monthly'].append(out2['output'])
                    #     error_message_list.append(out2['error_message_list'])
                    #     print(out2['message'])
                    # else:
                    #     output['monthly'].append(out2['output'])
                    #     error_message_list.append(out2['error_message_list'])
                    #     company_calculated_m = company_calculated_m + 1
                    #     com.nse_monthly_return_update_date = date.today()
                    #     com.save()
                    out = ReturnCalculate.calculate_return(company = com,exchange = exchange,date_check=date_check) 
                    output.append(out['output'])
                    error_message_list.append(out['error_message_list']) 
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

            



    # def daily_return(asset,exchange):
    #     error = False
    #     success = False
    #     error_message_list = []
    #     output = []
    #     message = "Request Recieved"
    #     date_today = date.today()
    #     if exchange == "NSE":
    #         # company = Company.objects.filter(company__nse_ticker=asset)
    #         # if company:
    #         #     company = company[0]
                
    #         #     last_db_update_date = company.nse_daily_return_update_date
    #         #     fromdate = last_db_update_date - timedelta(days=600)
    #         # else:

    #         assetdata = TickerHistoricDay.objects.filter(company__nse_ticker=asset).order_by('date')
    #         # print('1')
    #         if assetdata.count() > 0:
    #             try:
    #                 date_list  = list(map(lambda x : str(x.date),assetdata))
    #                 price_list = list(map(lambda x : float(x.price_close),assetdata))
    #                 # print('2')
    #                 exchange = assetdata[0].exchange
    #                 company = assetdata[0].company
    #                 date_price = {
    #                             'Price': price_list
    #                             }
    #                 asset_df = pd.DataFrame(date_price, columns = ['Price'], index=pd.to_datetime(date_list))
    #                 # return asset_df
    #                 # print('3')
    #                 asset_daily_return_1d  =  asset_df['Price'].pct_change(1)
    #                 asset_daily_return_2d  =  asset_df['Price'].pct_change(2)
    #                 asset_daily_return_3d  =  asset_df['Price'].pct_change(3)
    #                 asset_daily_return_4d  =  asset_df['Price'].pct_change(4)
    #                 asset_daily_return_5d  =  asset_df['Price'].pct_change(5)
    #                 asset_daily_return_6d  =  asset_df['Price'].pct_change(6)
    #                 asset_daily_return_7d  =  asset_df['Price'].pct_change(7)
    #                 asset_daily_return_14d =  asset_df['Price'].pct_change(14)
    #                 asset_daily_return_21d =  asset_df['Price'].pct_change(21)
    #                 asset_daily_return_25d =  asset_df['Price'].pct_change(25)
    #                 # print('4')
    #                 total_len = len(price_list)
    #                 for i in range(total_len):
    #                     # print('5')
    #                     # print(i)
    #                     # print(company.name)
    #                     # print(date_list[i])
    #                     # print(asset_daily_return_1d[i])
    #                     assetreturn = DailyReturn.objects.create(
    #                         company       = company
    #                         ,exchange     = exchange
    #                         ,date         = date_list[i]
    #                         ,return_1d    = asset_daily_return_1d[i] if str(asset_daily_return_1d[i]) != 'nan'  else None   
    #                         ,return_2d    = asset_daily_return_2d[i] if str(asset_daily_return_2d[i]) != 'nan'  else None   
    #                         ,return_3d    = asset_daily_return_3d[i] if str(asset_daily_return_3d[i]) != 'nan'  else None   
    #                         ,return_4d    = asset_daily_return_4d[i] if str(asset_daily_return_4d[i]) != 'nan'  else None   
    #                         ,return_5d    = asset_daily_return_5d[i] if str(asset_daily_return_5d[i]) != 'nan'  else None   
    #                         ,return_6d    = asset_daily_return_6d[i] if str(asset_daily_return_6d[i]) != 'nan'  else None   
    #                         ,return_7d    = asset_daily_return_7d[i] if str(asset_daily_return_7d[i]) != 'nan'  else None   
    #                         ,return_14d   = asset_daily_return_14d[i] if str(asset_daily_return_14d[i]) != 'nan'  else None   
    #                         ,return_21d   = asset_daily_return_21d[i] if str(asset_daily_return_21d[i]) != 'nan'  else None   
    #                         ,return_25d   = asset_daily_return_25d[i] if str(asset_daily_return_25d[i]) != 'nan'  else None   
    #                         )  
    #                 output = DailyReturn.objects.filter(company = company)
    #                 error = False
    #                 success = True
    #                 message = "Daily Returns calculated for " + asset 
    #                 # print("Daily Returns calculated for " + asset )
    #             except:
    #                 output = []
    #                 error = True
    #                 success = False
    #                 message = "Daily Return calculation error " + asset
    #                 error_message_list.append('Daily return calculation failure '+ asset)
    #                 # print("Daily Return calculation error " + asset)
    #         else:
    #             error = True
    #             success = False
    #             message = "Data not found for the " + asset
    #             error_message_list.append("Invalid asset code")
    #             # print("No data found for " + asset )
        
    #     return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    # def monthly_return(asset,exchange):
    #     error = False
    #     success = False
    #     error_message_list = []
    #     output = []
    #     message = "Request Recieved"
    #     if exchange == "NSE":
    #         assetdata = TickerHistoricDay.objects.filter(company__nse_ticker=asset).order_by('date')
    #         # print('1')
    #         if assetdata.count() > 0:
    #             try:
    #                 date_list  = list(map(lambda x : str(x.date),assetdata))
    #                 price_list = list(map(lambda x : float(x.price_close),assetdata))
    #                 # print('2')
    #                 exchange = assetdata[0].exchange
    #                 company = assetdata[0].company
    #                 date_price = {
    #                             'Price': price_list,
    #                             'Dates':date_list
    #                             }
    #                 asset_df = pd.DataFrame(date_price, columns = ['Dates','Price'], index=pd.to_datetime(date_list))
    #                 asset_df_new = asset_df.resample('M').ffill()

    #                 # return asset_df
    #                 # prinmonthly)
    #                 asset_monthly_return_1m   =  asset_df_new['Price'].pct_change(1)
    #                 asset_monthly_return_2m   =  asset_df_new['Price'].pct_change(2)
    #                 asset_monthly_return_3m   =  asset_df_new['Price'].pct_change(3)
    #                 asset_monthly_return_4m   =  asset_df_new['Price'].pct_change(4)
    #                 asset_monthly_return_5m   =  asset_df_new['Price'].pct_change(5)
    #                 asset_monthly_return_6m   =  asset_df_new['Price'].pct_change(6)
    #                 asset_monthly_return_7m   =  asset_df_new['Price'].pct_change(7)
    #                 asset_monthly_return_8m   =  asset_df_new['Price'].pct_change(8)
    #                 asset_monthly_return_9m   =  asset_df_new['Price'].pct_change(9)
    #                 asset_monthly_return_10m  =  asset_df_new['Price'].pct_change(10)
    #                 asset_monthly_return_11m  =  asset_df_new['Price'].pct_change(11)
    #                 asset_monthly_return_12m  =  asset_df_new['Price'].pct_change(12)
    #                 asset_monthly_return_13m  =  asset_df_new['Price'].pct_change(13)
    #                 asset_monthly_return_14m  =  asset_df_new['Price'].pct_change(14)
    #                 asset_monthly_return_15m  =  asset_df_new['Price'].pct_change(15)
    #                 asset_monthly_return_16m  =  asset_df_new['Price'].pct_change(16)
    #                 asset_monthly_return_17m  =  asset_df_new['Price'].pct_change(17)
    #                 asset_monthly_return_18m  =  asset_df_new['Price'].pct_change(18)
                    

    #                 # print('4')
    #                 total_len = len(asset_df_new)
    #                 # print(asset_df_new)
    #                 for i in range(total_len):
    #                     # print('5')
    #                     # print(i)
    #                     # print(company.name)
    #                     # print(date_list[i])
    #                     # print(asset_daily_return_1d[i])
    #                     # print(date_list[i])
    #                     # print(asset_monthly_return_1m[i])
    #                     assetreturn = MonthlyReturn.objects.create(
    #                         company       = company
    #                         ,exchange     = exchange
    #                         ,date         = dt.datetime.utcfromtimestamp(asset_df_new.index[i].value//1000000000).strftime("%Y-%m-%d")
    #                         ,return_1m    = asset_monthly_return_1m[i] if str(asset_monthly_return_1m[i]) != 'nan'  else None   
    #                         ,return_2m    = asset_monthly_return_2m[i] if str(asset_monthly_return_2m[i]) != 'nan'  else None   
    #                         ,return_3m    = asset_monthly_return_3m[i] if str(asset_monthly_return_3m[i]) != 'nan'  else None   
    #                         ,return_4m    = asset_monthly_return_4m[i] if str(asset_monthly_return_4m[i]) != 'nan'  else None   
    #                         ,return_5m    = asset_monthly_return_5m[i] if str(asset_monthly_return_5m[i]) != 'nan'  else None   
    #                         ,return_6m    = asset_monthly_return_6m[i] if str(asset_monthly_return_6m[i]) != 'nan'  else None   
    #                         ,return_7m    = asset_monthly_return_7m[i] if str(asset_monthly_return_7m[i]) != 'nan'  else None   
    #                         ,return_8m    = asset_monthly_return_8m[i] if str(asset_monthly_return_8m[i]) != 'nan'  else None   
    #                         ,return_9m    = asset_monthly_return_9m[i] if str(asset_monthly_return_9m[i]) != 'nan'  else None   
    #                         ,return_10m   = asset_monthly_return_10m[i] if str(asset_monthly_return_10m[i]) != 'nan'  else None   
    #                         ,return_11m   = asset_monthly_return_11m[i] if str(asset_monthly_return_11m[i]) != 'nan'  else None   
    #                         ,return_12m   = asset_monthly_return_12m[i] if str(asset_monthly_return_12m[i]) != 'nan'  else None   
    #                         ,return_13m   = asset_monthly_return_13m[i] if str(asset_monthly_return_13m[i]) != 'nan'  else None   
    #                         ,return_14m   = asset_monthly_return_14m[i] if str(asset_monthly_return_14m[i]) != 'nan'  else None   
    #                         ,return_15m   = asset_monthly_return_15m[i] if str(asset_monthly_return_15m[i]) != 'nan'  else None   
    #                         ,return_16m   = asset_monthly_return_16m[i] if str(asset_monthly_return_16m[i]) != 'nan'  else None   
    #                         ,return_17m   = asset_monthly_return_17m[i] if str(asset_monthly_return_17m[i]) != 'nan'  else None   
    #                         ,return_18m   = asset_monthly_return_18m[i] if str(asset_monthly_return_18m[i]) != 'nan'  else None   
    #                         )  
    #                 output = MonthlyReturn.objects.filter(company = company)
    #                 error = False
    #                 success = True
    #                 message = "Monthly Returns calculated for " + asset 
    #                 # print("Monthly Returns calculated for " + asset )
    #             except:
    #                 output = []
    #                 error = True
    #                 success = False
    #                 message = "Monthly Return calculation error " + asset
    #                 error_message_list.append('Monthly Return Calculation failure '+ asset)
    #                 # print("Monthly Return calculation error " + asset)
    #         else:
    #             error = True
    #             success = False
    #             message = "Data not found for the " + asset
    #             # print("Data not found for the " + asset)
    #             error_message_list.append("Invalid asset code")
        
    #     return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}


