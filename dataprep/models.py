from django.db import models
from datascrape.models import BaseModel, Company, Exchange
import json
# Create your models here.

class DailyReturn(BaseModel):
    company      = models.ForeignKey(Company,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    exchange     = models.ForeignKey(Exchange,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    date         = models.DateField(db_index=True)
    return_1d    = models.FloatField(null=True)
    return_2d    = models.FloatField(null=True)
    return_3d    = models.FloatField(null=True)
    return_4d    = models.FloatField(null=True)
    return_5d    = models.FloatField(null=True)
    return_6d    = models.FloatField(null=True)
    return_7d    = models.FloatField(null=True)    
    return_14d   = models.FloatField(null=True)
    return_21d   = models.FloatField(null=True)
    return_25d   = models.FloatField(null=True)    
    def __str__(self):
        return json.dumps({'id':self.id,'ticker_name':self.company.name})

class MonthlyReturn(BaseModel):
    company     = models.ForeignKey(Company,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    exchange    = models.ForeignKey(Exchange,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    date        = models.DateField(db_index=True)
    return_1m    = models.FloatField(null=True)
    return_2m    = models.FloatField(null=True)
    return_3m    = models.FloatField(null=True)
    return_4m    = models.FloatField(null=True)
    return_5m    = models.FloatField(null=True)
    return_6m    = models.FloatField(null=True)
    return_7m    = models.FloatField(null=True)    
    return_8m    = models.FloatField(null=True)
    return_9m    = models.FloatField(null=True)
    return_10m   = models.FloatField(null=True)
    return_11m   = models.FloatField(null=True)
    return_12m   = models.FloatField(null=True)
    return_13m   = models.FloatField(null=True)
    return_14m   = models.FloatField(null=True)
    return_15m   = models.FloatField(null=True)    
    return_16m   = models.FloatField(null=True)    
    return_17m   = models.FloatField(null=True)    
    return_18m   = models.FloatField(null=True)    
