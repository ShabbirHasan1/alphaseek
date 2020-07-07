from django.shortcuts import render
from strategytest.views import * 
# Create your views here.
import random


# Test Strategies for the code
def random_1_asset(update=False):
    strategy = CheckStrategy.create_strategy(
        name="Random 1 Asset",
        description="Selecting any 1 random asset for the portfolio every month"
    )
    strategy = strategy['output'][0]
    # logic
    all_monthly_returns = MonthlyReturn.objects.all().order_by('date')
    months = list(map(lambda x : x.date,all_monthly_returns))
    months = list(dict.fromkeys(months))
    total_months = len(months)
    if not update:
        StrategyPortfolio.objects.filter(strategy = strategy).delete()

    for i in range(0,total_months):
        portfolio_options = MonthlyReturn.objects.filter(date = months[i])
        asset_option = random.choice(portfolio_options)
        CheckStrategy.create_portfolio(strategy=strategy,company = asset_option.company, exchange = asset_option.exchange,date=months[i],weight=1)


    CheckStrategy.calculate_strategy_returns(strategy=strategy,update=update)
    CheckStrategy.alpha_check(strategy=strategy)
    return "Strategy Created and Calculated"

def random_2_asset(update = False):
    strategy = CheckStrategy.create_strategy(
        name="Random 2 Asset",
        description="Selecting any 2 random asset for the portfolio every month equi weighted or less depending on number of asset options" 
    )
    strategy = strategy['output'][0]
    # logic
    all_monthly_returns = MonthlyReturn.objects.all().order_by('date')
    months = list(map(lambda x : x.date,all_monthly_returns))
    months = list(dict.fromkeys(months))
    total_months = len(months)
    if not update:
        StrategyPortfolio.objects.filter(strategy = strategy).delete()

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


    CheckStrategy.calculate_strategy_returns(strategy=strategy,update=update)
    CheckStrategy.alpha_check(strategy=strategy)
    return "Strategy Created and Calculated"

def momentum_strategy(months = 6, pickup_percentile = 5, update = False):
    if ((months <= 18) and (months > 0)):
        strategy = CheckStrategy.create_strategy(
            name="Long only momentum strategy; Portfolio update frequency :" + str(months) + " months" + "; percentile pickup : "+ str(pickup_percentile)+ "%",
            description="Selecting top " + str(pickup_percentile) + " percent assets for the portfolio every " + str(months) + "months. Equi weighted distribution of assets. Long Only for the postions" 
        )
        strategy = strategy['output'][0]
        # logic
        all_monthly_returns = MonthlyReturn.objects.all().order_by('date')
        months_list = list(map(lambda x : x.date,all_monthly_returns))
        months_list = list(dict.fromkeys(months_list))
        total_months = len(months_list)
        if not update:
            StrategyPortfolio.objects.filter(strategy = strategy).delete()
        month_shift = 0 
        for i in range(0,total_months):
            if ((i-month_shift) % months == 0 ):
                portfolio_options = MonthlyReturn.objects.filter(date = months_list[i]).order_by("-return_" + str(months) + "m")
                total_options = portfolio_options.count()
                if total_options >= 50:
                    print(months_list[i])
                    print("Options:"  + str(total_options))
                    options_to_select = (round(total_options * pickup_percentile / 100 ,0) + 1)
                    print("Options to select:"  + str(options_to_select))
                    weight_per_asset = (1/options_to_select)
                    print("Weight per asset:"  + str(weight_per_asset))
                    portfolio_selected = portfolio_options[:options_to_select]
                    for port in portfolio_selected:
                        CheckStrategy.create_portfolio(strategy=strategy,company = port.company, exchange = port.exchange, date=months_list[i],weight=float(weight_per_asset))            
                else:
                    month_shift = month_shift + 1
        CheckStrategy.calculate_strategy_returns(strategy=strategy,update=update)
        CheckStrategy.alpha_check(strategy=strategy)
        return "Strategy Created and Calculated"

    else:
        return "Strategy not created, reduce the month range"




