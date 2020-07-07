from strategyout.views import *
from importlib import reload
from strategytest.models import *

StrategyDetails.objects.all().delete()
momentum_strategy(months=6,pickup_percentile=10)