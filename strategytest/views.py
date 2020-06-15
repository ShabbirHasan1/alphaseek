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
                name = name.lower()
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
        if not update:
            StrategyReturns.objects.all().delete()
        try:
            portfolio_list = StrategyPortfolio.objects.filter(strategy = strategy).order_by('date')        
            date_list = list(map(lambda x : x.date,portfolio_list))
            date_list = list(dict.fromkeys(date_list))
            total_dates = len(date_list)
            df_final = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
            counter_d = 0 
            # print(total_dates)
            for i in range(0,total_dates):   
                # print(i)
                portfolio = StrategyPortfolio.objects.filter(strategy=strategy, date = date_list[i])
                df_overall = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
                if i != (total_dates - 1):
                    counter_p = 0 
                    for port in portfolio:
                        df_port  = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
                        daily_returns = DailyReturn.objects.filter(company=port.company, exchange = port.exchange, date__gte= date_list[i], date__lt = date_list[i+1])
                        df_list = list(map(lambda x : {'Date':str(x.date),'Return':x.return_1d},daily_returns))
                        df_port = df_port.append(df_list,ignore_index=True)
                        df_port['Return'] = df_port['Return'] * port.weight
                        if counter_p == 0 :
                            df_overall = df_overall.append(df_port,ignore_index=True)
                        else:
                            df_overall['Return'] = df_overall['Return'] + df_port['Return']
                        counter_p = counter_p + 1
                else:
                    counter_p=0
                    for port in portfolio:
                        df_port  = pd.DataFrame({'Date':[],'Return':[]}, columns = ['Date','Return'])
                        returns = DailyReturn.objects.filter(company=port.company, exchange = port.exchange, date__gte= date_list[i])
                        daily_returns = DailyReturn.objects.filter(company=port.company, exchange = port.exchange, date__gte= date_list[i])                    
                        df_list = list(map(lambda x : {'Date':str(x.date),'Return':x.return_1d},daily_returns))
                        df_port = df_port.append(df_list,ignore_index=True)
                        df_port['Return'] = df_port['Return'] * port.weight
                        if counter_p == 0 :
                            df_overall = df_overall.append(df_port,ignore_index=True)
                        else:
                            df_overall['Return'] = df_overall['Return'] + df_port['Return']
                # print(df_port)
                # print(df_overall)            
                df_final = df_final.append(df_overall,ignore_index=True)
                
            
            df_final['HWM'] = 1.0
            df_final['Drawdown'] = 0.0
            df_final['Cumulative Return'] = 0.0
            hwm = 1.0
            port_return = 1.0
            max_drawdown = 0.0
            total_len_df = len(df_final)
            # total_len_df = 30
            for k in range(total_len_df):
                port_return = port_return * ( 1 + df_final['Return'][k])
                # print(port_return)
                hwm = max(hwm, port_return)
                drawdown = hwm - port_return 
                max_drawdown = max(max_drawdown,drawdown)
                df_final['HWM'][k] = hwm
                df_final['Drawdown'][k] = drawdown
                df_final['Cumulative Return'][k] = port_return

                if update:
                    strategy_return = StrategyReturns.objects.filter(date = df_final['Date'][k],strategy=strategy)                    
                    if strategy_return.count() > 0:
                        strategy_return = strategy_return[0]
                        strategy_return.return_strategy = df_final['Return'][k]
                        strategy_return.high_water_mark = hwm
                        strategy_return.drawdown = drawdown
                        strategy_return.cumulative_return = port_return
                        strategy_return.save()
                    else:
                        StrategyReturns.objects.create(
                            strategy            = strategy
                            ,date                = df_final['Date'][k]
                            ,return_strategy     = df_final['Return'][k]
                            ,high_water_mark     = hwm
                            ,drawdown            = drawdown
                            ,cumulative_return   = port_return
                        )
                else:
                    StrategyReturns.objects.create(
                        strategy            = strategy
                        ,date                = df_final['Date'][k]
                        ,return_strategy     = df_final['Return'][k]
                        ,high_water_mark     = hwm
                        ,drawdown            = drawdown
                        ,cumulative_return   = port_return
                    )
        # print(df_final)
            volatility = df_final['Return'].std() * math.sqrt(245)
            average_return = df_final['Return'].mean() * 245
            sharpe_ratio = ((average_return - risk_free_rate)/volatility)
            strategy.volatility = volatility 
            strategy.return_strategy = average_return 
            strategy.max_drawdown = max_drawdown
            strategy.sharpe_ratio = sharpe_ratio
            strategy.historic_start_date = df_final['Date'][0]
            strategy.historic_end_date = df_final['Date'][total_len_df-1]
            strategy.save()
            message = "Portfolio Calculations Complete"
            success = True
            error = False
            output = []
        except:
            message = "Calculation Failure"        
            output = []
            success = False
            error = True

        # print("volatility:" +  str(volatility))
        # print("average_return:" +  str(average_return))
        # print("max_drawdown:" +  str(max_drawdown))
        # print("sharpe_ratio:" +  str(sharpe_ratio))
        # print("historic_start_date:" +  str(df_final['Date'][0]))
        # print("historic_end_date:" +  str(df_final['Date'][total_len_df-1])
        
        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}


    def alpha_check(strategy,index_ticker):
        error = False
        success = False
        error_message_list = []
        output = ""
        message = "Request Recieved"


        if strategy:
            strategy_returns = StrategyReturns.objects.filter(strategy=strategy).order_by('date')           
        else:
            error = True
            success = False
            message = "Strategy missing!" 
            error_message_list.append("Strategy missing!")

        if index_ticker:
            index_returns = IndexDailyReturn.objects.filter(index__ticker = index_ticker).order_by('date')             

        else:
            error = True
            success = False
            message = "Index Code missing!" 
            error_message_list.append("Index Code missing!" )

        if not error:
            date_list_strat = list(map(lambda x : x.date,strategy_returns))
            return_strat_list = list(map(lambda x : x.return_1m,strategy_returns))
            df_strategy = pd.DataFrame({'Date':date_list_strat,'Return Strategy':return_strat_list}, columns = ['Date','Return Strategy'])
            
            date_list_index = list(map(lambda x : x.date,index_returns))
            return_index_list = list(map(lambda x : x.return_1m,index_returns))
            df_index    = pd.DataFrame({'Date':date_list_index,'Return Index':return_index_list}, columns = ['Date','Return Index'])
            df_final = pd.merge(df_strategy,
                 df_index[['Date', 'Return Index']],
                 on='Date', 
                 how='left')
            


        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}




