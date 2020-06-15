from django.shortcuts import render
from strategytest.views import * 
# Create your views here.



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
        description="Selecting any 2 random asset for the portfolio every month equi weighted" 
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


