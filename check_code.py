from strategyout.views import *
from importlib import reload
from strategytest.models import *

StrategyDetails.objects.all().delete()
momentum_strategy(frequency = 1, return_months=12,num_stocks=30)