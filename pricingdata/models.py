from django.db import models
import json

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
    name           = models.CharField(max_length=300,db_index=True)
    isin_no        = models.CharField(max_length=50)
    is_listed_nse  = models.BooleanField(default=False)
    nse_ticker     = models.CharField(max_length=50,null=True)
    industry_sector        = models.ForeignKey(IndustrySector,
                                        on_delete=models.SET_NULL,
                                        null = True)
    nse_tracker    = models.BooleanField(default=False)
    nse_price_update_db_date = models.DateField(null=True)
    nse_return_update_date = models.DateField(null=True)
    finance_update_date = models.DateField(null=True)
    sentiment_update_date = models.DateField(null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'company_name':self.name})

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
    dividends   = models.FloatField(null=True)
    stock_split = models.FloatField(null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'ticker_name':self.company.name})