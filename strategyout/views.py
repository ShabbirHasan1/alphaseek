from django.shortcuts import render
from strategytest.views import * 
# Create your views here.
import random


# Test Strategies for the code
def random_1_asset():
    strategy = CheckStrategy.create_strategy(
        name="Random 1 Asset",
        description="Selecting any 1 random asset for the portfolio every month"
    )
    strategy = strategy['output'][0]
    all_monthly_returns = MonthlyReturn.objects.all().order_by('date')
    # logic
    months = list(map(lambda x : x.date,all_monthly_returns))
    months = list(dict.fromkeys(months))
    total_months = len(months)
    for i in range(0,total_months):
        portfolio_options = MonthlyReturn.objects.filter(date = months[i])
        asset_option = random.choice(portfolio_options)
        CheckStrategy.create_portfolio(strategy=strategy,company = asset_option.company, exchange = asset_option.exchange,date=months[i],weight=1)


    CheckStrategy.calculate_strategy_returns(strategy=strategy)
    CheckStrategy.alpha_check(strategy=strategy)

def random_2_asset():
    strategy = CheckStrategy.create_strategy(
        name="Random 2 Asset",
        description="Selecting any 2 random asset for the portfolio every month equi weighted or less depending on number of asset options" 
    )
    strategy = strategy['output'][0]
    all_monthly_returns = MonthlyReturn.objects.all().order_by('date')
    # logice
    months = list(map(lambda x : x.date,all_monthly_returns))
    months = list(dict.fromkeys(months))
    total_months = len(months)
    for i in range(0,total_months):
        portfolio_options = MonthlyReturn.objects.filter(date = months[i])
        if len(portfolio_options) == 1:
            asset_option = portfolio_options[0]
            CheckStrategy.create_portfolio(strategy=strategy,company = asset_option.company, exchange = asset_option.exchange,date=months[i],weight=1)            
        else:
            num_to_select = 2                           # set the number to select here.
            list_of_random_assets = random.sample(list(portfolio_options), num_to_select)
            first_random_asset = list_of_random_assets[0]
            second_random_asset = list_of_random_assets[1] 
            # asset_option = random.choice(portfolio_options)
            CheckStrategy.create_portfolio(strategy=strategy,company = first_random_asset.company, exchange = first_random_asset.exchange,date=months[i],weight=0.5)
            CheckStrategy.create_portfolio(strategy=strategy,company = second_random_asset.company, exchange = second_random_asset.exchange,date=months[i],weight=0.5)


    CheckStrategy.calculate_strategy_returns(strategy=strategy)
    CheckStrategy.alpha_check(strategy=strategy)


