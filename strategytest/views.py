from django.shortcuts import render
from strategytest.models import *
from dataprep.models import *
from overall.views import *
import pandas as pd
import datetime as dt
from datetime import date, timedelta
# Create your views here.

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


    def calculate_strategy_returns(strategy):
        error = False
        success = False
        error_message_list = []
        output = StrategyReturns.objects.none()
        message = "Request Recieved"
        StrategyReturns.objects.all().delete()
        portfolio_list = StrategyPortfolio.objects.filter(strategy=strategy).order_by('date')
        for port in portfolio_list:        
            
            pass


        # return_stock    = models.FloatField()
        # high_water_mark = models.FloatField()
        # drawdown        = models.FloatField()

        return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}
