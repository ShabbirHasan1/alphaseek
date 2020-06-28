from django.db import models
import json
from django.contrib.postgres.fields import JSONField


return_details = {
    'return_1d':None,
    'return_1m':None,
    'return_1y':None,
    'annualized_avg_return':None,
    'annualized_avg_volatility':None
}

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# New Models

class Exchange(BaseModel):
    exchange_name = models.CharField(max_length=100,db_index=True)
    exchange_code = models.CharField(max_length=50,db_index=True)
    exchange_country = models.CharField(max_length=50)
    exchange_timezone = models.CharField(max_length=50)
    exchange_timezone_short = models.CharField(max_length=50)
    exchange_currency       = models.CharField(max_length=20)
    timezone_gmt_off_milliseconds = models.IntegerField(default=0)
    def __str__(self):
        return json.dumps({'id':self.id,'exchange_code':self.exchange_code})

class IndustrySector(BaseModel):
    industry = models.CharField(max_length=300,db_index=True)
    sector = models.CharField(max_length=300)
    details = models.CharField(max_length=500,null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'industry_name':self.industry,'sector_name':self.sector})

class Company(BaseModel):
    name            = models.CharField(max_length=300,db_index=True)
    isin_no         = models.CharField(max_length=50)
    is_listed_nse   = models.BooleanField(default=False)
    nse_ticker      = models.CharField(max_length=50,null=True)
    industry_sector = models.ForeignKey(IndustrySector,
                                        on_delete=models.SET_NULL,
                                        null = True)
    nse_tracker    = models.BooleanField(default=False)
    nse_price_update_db_date = models.DateField(null=True)
    nse_return_update_date = models.DateField(null=True)
    nse_return_date          = models.DateField(default=None,null=True)
    nse_return_1d            = models.FloatField(default=0,null=True)
    nse_return_1m            = models.FloatField(default=0,null=True)
    nse_return_1y            = models.FloatField(default=0,null=True)
    nse_annualized_return    = models.FloatField(default=0,null=True)
    nse_annualized_vol       = models.FloatField(default=0,null=True)
    nse_trade_date           = models.DateField(default=None,null=True)
    nse_price_high           = models.FloatField(default=0,null=True)
    nse_price_low            = models.FloatField(default=0,null=True)
    nse_price_close          = models.FloatField(default=0,null=True)
    nse_price_open           = models.FloatField(default=0,null=True)
    nse_price_close_adjusted = models.FloatField(default=0,null=True)
    nse_volume               = models.FloatField(default=0,null=True)
    finance_update_date      = models.DateField(default=None,null=True)
    sentiment_update_date    = models.DateField(default=None,null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'company_name':self.name})


class Index(BaseModel):
    name               = models.CharField(max_length=300,db_index=True)
    ticker             = models.CharField(max_length=50,null=True)
    exchange           = models.ForeignKey(Exchange,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    return_date = models.DateField(null=True)                     
    return_1d         = models.FloatField(default=0,null=True)
    return_1m         = models.FloatField(default=0,null=True)
    return_1y         = models.FloatField(default=0,null=True)
    annualized_return = models.FloatField(default=0,null=True)
    annualized_vol    = models.FloatField(default=0,null=True)
    trade_date   = models.DateField(default=None,null=True)
    price_high        = models.FloatField(default=0,null=True)
    price_low         = models.FloatField(default=0,null=True)
    price_close       = models.FloatField(default=0,null=True)
    price_open        = models.FloatField(default=0,null=True)
    price_close_adjusted = models.FloatField(default=0,null=True)
    volume            = models.FloatField(default=0,null=True)
    price_update_date = models.DateField(null=True)
    return_update_date = models.DateField(null=True)
    

class IndexHistoricDay(BaseModel):
    index     = models.ForeignKey(Index,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    exchange    = models.ForeignKey(Exchange,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    date        = models.DateField(db_index=True)
    price_high  = models.FloatField(null=True)
    price_low   = models.FloatField(null=True)
    price_close = models.FloatField(null=True)
    price_open  = models.FloatField(null=True)
    price_close_adjusted = models.FloatField(null=True)
    volume      = models.FloatField(null=True)



class TickerHistoricDay(BaseModel):
    company     = models.ForeignKey(Company,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    exchange    = models.ForeignKey(Exchange,
                                    on_delete=models.CASCADE,
                                    null = True,db_index=True)
    date        = models.DateField(db_index=True)
    price_high  = models.FloatField(null=True)
    price_low   = models.FloatField(null=True)
    price_close = models.FloatField(null=True)
    price_open  = models.FloatField(null=True)
    price_close_adjusted = models.FloatField(null=True)
    volume      = models.FloatField(null=True)
    dividends   = models.FloatField(null=True,default=0)
    stock_split = models.FloatField(null=True,default=0)
    def __str__(self):
        return json.dumps({'id':self.id,'ticker_name':self.company.name,'date':str(self.date)})