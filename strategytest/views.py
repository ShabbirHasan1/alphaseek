from django.shortcuts import render
from strategytest.models import *
from dataprep.models import *
from overall.views import *
import pandas as pd
import datetime as dt
from datetime import date, timedelta
import math
# Create your views here.

risk_free_rate = 0.044

class CheckStrategy:
    def create_strategy(name,description):
        error = False
        success = False
        error_message_list = []
        output = StrategyDetails.objects.none()
        message = "Request Recieved"

        strategy = StrategyDetails.objects.filter(name=name.lower())
        if strategy.count() > 0 :
            message = "Strategy Already Exists!"        
            output = strategy
            success = False
            error = False
        else:
            strategy_new = StrategyDetails.objects.create(
                name = name
                ,description = description
            )
            output = [strategy_new]
            success = True
            message = "Strategy Created!"
            error = False

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

    def create_portfolio(strategy,company,exchange,date,weight):
        error = False
        success = False
        error_message_list = []
        output = StrategyPortfolio.objects.none()
        message = "Request Recieved"

        portfolio = StrategyPortfolio.objects.filter(
            strategy=strategy,
            company=company,
            exchange=exchange,
            date=date
        )
        if portfolio.count() > 0 :
            message = "Portfolio entry already exists!"        
            output = portfolio
            success = False
            error = False
        else:
            portfolio_new = StrategyPortfolio.objects.create(
                strategy=strategy,
                company=company,
                exchange=exchange,
                date=date,
                weight=weight
            )
            output = [portfolio_new]
            success = True
            message = "Portfolio entry added Created!"
            error = False

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}


    def calculate_strategy_returns(strategy,update=False):
        error = False
        success = False
        error_message_list = []
        output = StrategyReturns.objects.none()
        message = "Request Recieved"
        if update:
            StrategyReturns.objects.all().delete()

        portfolio_list = StrategyPortfolio.objects.filter(strategy = strategy).order_by('date')        
        date_list = list(map(lambda x : x.date,portfolio_list))
        date_list = list(dict.fromkeys(date_list))
        total_dates = len(date_list)
        df_final = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
        counter_d = 0 
        for i in range(0,total_dates):        
            portfolio = StrategyPortfolio.objects.filter(strategy=strategy, date = date[i])
            df_overall = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
            if i != total_dates:
                counter_p = 0 
                for port in portfolio:
                    df_port  = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
                    daily_returns = DailyReturn.objects.filter(company=port.company, exchange = port.exchange, date__gte= date[i], date__lt = date[i+1])
                    df_list = list(map(lambda x : {'Date':str(x.date),'Return':x.asset_daily_return_1d},daily_returns))
                    df_port = df_port.append(df_list,ignore_index=True)
                    df_port['Return'] = df_port['Return'] * port.weight
                    if counter_p == 0 :
                        df_overall = df_overall.append(df_port,ignore_index=True)
                    else:
                        df_overall['Return'] = df_overall['Return'] + df_port['Return']
                    counter_p = counter_p + 1
            else:
                for port in portfolio:
                    df_port  = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
                    returns = DailyReturn.objects.filter(company=port.company, exchange = port.exchange, date__gte= date[i])
                    daily_returns = DailyReturn.objects.filter(company=port.company, exchange = port.exchange, date__gte= date[i])                    
                    df_list = list(map(lambda x : {'Date':str(x.date),'Return':x.asset_daily_return_1d},daily_returns))
                    df_port = df_port.append(df_list,ignore_index=True)
                    df_port['Return'] = df_port['Return'] * port.weight
                    if counter_p == 0 :
                        df_overall = df_overall.append(df_port,ignore_index=True)
                    else:
                        df_overall['Return'] = df_overall['Return'] + df_port['Return']
            
            df_final = df_final.append(df_overall,ignore_index=True)
        
        df_final['HWM'] = 1
        df_final['Drawdown'] = 0
        hwm = 1
        port_return = 1
        max_drawdown = 0 
        total_len_df = len(df_final)
        for k in range(total_len_df):
            port_return = port_return * ( 1+ df_final['Return'][k])
            hwm = max(hwm, port_return)
            drawdown = hwm - port_return 
            max_drawdown = max(max_drawdown,drawdown)
            df_final['HWM'][k] = hwm
            df_final['Drawdown'][k] = drawdown
        
        volatility = df_final['Return'].std() * math.sqrt(245)
        average_return = df_final['Return'].mean() * 245
        strategy.volatility = volatility 
        strategy.return_strategy = port_return 
        strategy.max_drawdown = max_drawdown
        strategy.sharpe_ratio = ((average_return - risk_free_rate)/volatility)
        strategy.historic_start_date = df_final['Date'][total_len_df-1]
        strategy.historic_end_date = df_final['Date'][0]
        strategy.save()

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}
