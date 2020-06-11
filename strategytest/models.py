from django.db import models
from datascrape.models import BaseModel, Company, Exchange
import json
# Create your models here.

class StrategyDetails(BaseModel):
    name = models.CharField(max_length=300,db_index=True)
    description  = models.CharField(max_length=500,null=True)
    alpha = models.FloatField(null=True)
    sharpe_ratio = models.FloatField(null=True) 
    # total_return_strategy = models.FloatField(null=True) 
    average_return = models.FloatField(null=True) 
    max_drawdown    = models.FloatField(null=True)
    volatility = models.FloatField(null=True) 
    historic_start_date = models.DateField(null=True)
    historic_end_date = models.DateField(null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'ticker_name':self.strategy.name})

class StrategyPortfolio(BaseModel):
    strategy   = models.ForeignKey(StrategyDetails,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    company      = models.ForeignKey(Company,
                                    on_delete=models.CASCADE,
                                    null = True)
    exchange     = models.ForeignKey(Exchange,
                                    on_delete=models.CASCADE,
                                    null = True)
    date         = models.DateField()
    weight       = models.FloatField(null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'ticker_name':self.strategy.name})

class StrategyReturns(BaseModel):
    strategy        = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                null = True,db_index=True)
    date            = models.DateField()
    return_stock    = models.FloatField()
    high_water_mark = models.FloatField()
    drawdown        = models.FloatField()
    def __str__(self):
        return json.dumps({'id':self.id,'ticker_name':self.strategy.name})

