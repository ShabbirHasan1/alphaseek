from django.shortcuts import render
from strategytest.views import * 
# Create your views here.




def test_strategy():
    strategy = CheckStrategy.create_strategy(
        name="Test Strategy",
        description="To test if strategy testing codes are working"
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



