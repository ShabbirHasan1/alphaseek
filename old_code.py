





        
    # def create_update_ticker(asset):
    #     nse = Nse()
    #     asset_ticker        = asset.lower()
    #     asset_nse_data      = nse.get_quote(asset) 
    #     isin_no             = asset_nse_data['isinCode']
    #     exchange            = Exchange.objects.get(exchange_code = 'NSE')        
    #     company             = Company.objects.get(isin_no = isin_no)
    #     findTicker          = Ticker.objects.filter(ticker = asset_ticker, exchange = exchange)
    #     # instrument      = cleanstring(company[3]).lower()
    #     if findTicker.count() > 0:
    #         findTicker                                = findTicker[0]
    #         findTicker.status                         = asset_nse_data['css_status_desc']  
    #         findTicker.price_high                     = asset_nse_data['dayHigh']
    #         findTicker.price_low                      = asset_nse_data['dayLow']
    #         findTicker.price_current                  = asset_nse_data['lastPrice']
    #         findTicker.price_open                     = asset_nse_data['open']
    #         findTicker.price_previous_close           = asset_nse_data['previousClose']
    #         findTicker.total_buy_quantity             = asset_nse_data['totalBuyQuantity']
    #         findTicker.total_sell_quantity            = asset_nse_data['totalSellQuantity']
    #         findTicker.total_traded_value             = asset_nse_data['totalTradedValue']
    #         findTicker.total_traded_volume            = asset_nse_data['totalTradedVolume']
    #         findTicker.instrument_type                = 'Equity' if asset_nse_data['series'] == 'EQ' else 'NA'
    #         findTicker.save()
    #         output = findTicker
    #     else:
    #         output = Ticker.objects.create(
    #             company                         = company
    #             ,exchange                       = exchange
    #             ,ticker                         = asset_ticker
    #             ,status                         = asset_nse_data['css_status_desc']  
    #             ,price_high                     = asset_nse_data['dayHigh']
    #             ,price_low                      = asset_nse_data['dayLow']
    #             ,price_current                  = asset_nse_data['lastPrice']
    #             ,price_open                     = asset_nse_data['open']
    #             ,price_previous_close           = asset_nse_data['previousClose']
    #             ,total_buy_quantity             = asset_nse_data['totalBuyQuantity']
    #             ,total_sell_quantity            = asset_nse_data['totalSellQuantity']
    #             ,total_traded_value             = asset_nse_data['totalTradedValue']
    #             ,total_traded_volume            = asset_nse_data['totalTradedVolume']
    #             ,instrument_type                = 'Equity' if asset_nse_data['series'] == 'EQ' else 'NA'
    #         )
    #     return output

    # def create_update_all_ticker():
    #     nse = Nse()
    #     all_asset_codes  = Company.objects.filter(is_listed_nse=True)
    #     i = 0
    #     for asset in all_asset_codes:
    #         if test_mode and i > no_run:
    #             break
    #         else:
    #             if i != 0:
    #                 print (asset.nse_ticker)
    #                 NseIndia.create_update_ticker(asset=asset.nse_ticker)
    #                 i = i + 1 
    #             else:
    #                 i = i + 1 
        




            




        














# <---------- Old Code ---------->


# quarters = {
#         1:'mar-19',
#         2:'mar-18',
#         4:'dec-18',
#         5:'dec-17',
#         7:'sep-18',
#         8:'sep-17',
#         10:'jun-18',
#         11:'jun-17',
# }

# years = {
#         2:'mar-19',
#         2:'mar-18',
#         4:'dec-18',
#         5:'dec-17',
#         7:'sep-18',
#         8:'sep-17',
#         10:'jun-18',
#         11:'jun-17',
# }



# def load_historical_prices():
#     companies = Company.objects.filter(scraped=False)    
#     j = 1
#     for company in companies:
#         if company.exchange == "NSE":
#             # print("3")
#             print(str(j) + ' | '+ company.exchange + ' | ' + company.security_code)
#             CompanyPrices.objects.filter(company=company).delete()
#             try:
#                 companyTotalData = yf.Ticker((company.security_code + ".NS"))
#                 companyPriceData = companyTotalData.history(period="max")
#                 index = companyPriceData.reset_index()['Date']
#                 total_len = len(index)
#                 for i in range(total_len):
#                     CompanyPrices.objects.create(
#                         company      = company
#                         ,date        = index[i]
#                         ,price_high  = companyPriceData['High'][i]
#                         ,price_low   = companyPriceData['Low'][i]
#                         ,price_close = companyPriceData['Close'][i]
#                         ,price_open  = companyPriceData['Open'][i]
#                         ,volume      = companyPriceData['Volume'][i]
#                         ,dividends   = companyPriceData['Dividends'][i]
#                         ,stock_split = companyPriceData['Stock Splits'][i]
#                     )
#                 company.status = "Active"
#                 company.scraped = True
#                 company.save()
#             except:
#                 company.status = "Delisted"
#                 company.save()
#             j = j + 1
                    






# def loadBSE(fileName):
#     with open(path+'/data/'+fileName, 'rU') as csvfile:
#         companyData = csv.reader(csvfile, delimiter='\t', quotechar='|')
#         i = 0
#         for company in companyData:
#             if i != 0:
#                 industry_name = cleanstring(company[7]).lower()
#                 if industry_name != "":
#                     industry = Industry.objects.filter(industry_name = industry_name)
#                     if industry.count() == 0:
#                         industry = Industry.objects.create(
#                             industry_name = industry_name
#                         )
#                     else:
#                         industry = None

#                 bse_security_code   = cleanstring(company[0]).lower()
#                 bse_security_id     = company[1]
#                 company_name        = cleanstring(company[2]).lower()
#                 bse_status          = cleanstring(company[3]).lower() 
#                 bse_group           = cleanstring(company[4]).lower()
#                 bse_face_value      = cleanstring(company[5]).lower()
#                 bse_isin_number     = cleanstring(company[6]).lower()
#                 bse_instrument      = cleanstring(company[8]).lower()

#                 findCompany = Company.objects.filter(bse_security_code=bse_security_code)
#                 if findCompany.count() > 0:
#                     findCompany = findCompany[0]
#                     findCompany.bse_security_code          = bse_security_code
#                     findCompany.bse_security_id            = bse_security_id
#                     findCompany.company_name               = company_name
#                     findCompany.bse_status                 = bse_status
#                     findCompany.bse_group                  = bse_group
#                     findCompany.bse_face_value             = bse_face_value
#                     findCompany.bse_isin_number            = bse_isin_number
#                     findCompany.industry                   = industry
#                     findCompany.bse_instrument             = bse_instrument
#                     findCompany.save()
#                 else:
#                     Company.objects.create(
#                         bse_security_code          = bse_security_code
#                         ,bse_security_id            = bse_security_id
#                         ,company_name               = company_name
#                         ,bse_status                 = bse_status
#                         ,bse_group                  = bse_group
#                         ,bse_face_value             = bse_face_value
#                         ,bse_isin_number            = bse_isin_number
#                         ,industry                   = industry
#                         ,bse_instrument             = bse_instrument
#                     )
#                 print(str(i) + '|' + company_name)
#             i = i + 1




# def loadNSE(fileName):
#     with open(path+'/data/'+fileName, 'rU') as csvfile:
#         companyData = csv.reader(csvfile, delimiter='\t', quotechar='|')
#         i = 0
#         for company in companyData:
#             if i != 0:
#                 industry_name = cleanstring(company[2]).lower()
#                 if industry_name != "":
#                     industry = Industry.objects.filter(industry_name = industry_name)
#                     if industry.count() == 0:
#                         industry = Industry.objects.create(
#                             industry_name = industry_name
#                         )
#                     else:
#                         industry = None

#                 security_code   = cleanstring(company[0])
#                 company_name    = cleanstring(company[1]).lower()
#                 instrument      = cleanstring(company[3]).lower()
#                 exchange        = cleanstring(company[4])

#                 findCompany = Company.objects.filter(security_code=security_code,exchange=exchange)
#                 if findCompany.count() > 0:
#                     findCompany = findCompany[0]
#                     findCompany.company_name               = company_name
#                     findCompany.industry                   = industry
#                     findCompany.instrument                 = instrument
#                     findCompany.save()
#                 else:
#                     Company.objects.create(
#                         security_code               = security_code
#                         ,company_name               = company_name
#                         ,industry                   = industry
#                         ,instrument                 = instrument
#                         ,exchange                   = exchange

#                     )
#                 print(str(i) + '|' + company_name)
#             i = i + 1
            





# def getFinancials(stockname):
#     response = requests.get('http://www.ratestar.in/company/bajfinance/500034/bajaj-finance-ltd-100034')
#     doc = document_fromstring(response.text)
#     # volume
#     volume = doc.xpath("//li[contains(@class, 'vol-pad')]/span")[0].text
#     # shareholding pattern
#     sharepattern = {}
#     sharediv = doc.xpath("//div[contains(@class, 'com-mid-share-tab1')]//li")
#     sharediv2 = doc.xpath("//div[contains(@class, 'com-mid-share-tab2')]//li")
#     sharenum = 0 
#     for share in sharediv:
#         sharepattern[cleanstring(share.text)] = cleanstring(sharediv2[sharenum].text)
#         # sharepattern[cleanstring(share.text)] = BeautifulSoup(sharediv2[sharenum].text).get_text()
#         sharenum = sharenum + 1

#     # ratestar
#     # quarterly resultss
#     quaterly_pnl_rows = doc.xpath("//section[contains(@id, 'Quarterly')]//table[contains(@id,'tblQtyStd')]//tbody/tr")
#     quarterly_standalone = {}
#     for pnlrow in quaterly_pnl_rows:
#         data_rows = pnlrow.xpath("./td//div[contains(@class,'in-tab-col-1')]")[0].xpath('./div')
#         i = 0 
#         dict = {}
#         for row in data_rows:            
#             if i == 0 :
#                 header = cleanstring(row.xpath("./span")[0].text)
#                 print(header)
#             else:
#                 print(i)
#                 if i not in [3,6,9,12,13]:                    
#                     dict[quarters[i]] = cleanstring(row.text)
#             print(dict)
#             i = i + 1
#         quarterly_standalone[header] = dict    
            
#     quaterly_pnl_rows = doc.xpath("//section[contains(@id, 'Quarterly')]//table[contains(@id,'tblQtyCons')]//tbody/tr")
 
#     quarterly_consolidated = {}
#     for pnlrow in quaterly_pnl_rows:
#         data_rows = pnlrow.xpath("./td//div[contains(@class,'in-tab-col-1')]")[0].xpath('./div')
#         i = 0 
#         dict = {}
#         for row in data_rows:            
#             if i == 0 :
#                 header = cleanstring(row.xpath("./span")[0].text)
#                 print(header)
#             else:
#                 print(i)
#                 if i not in [3,6,9,12,13]:                    
#                     dict[quarters[i]] = cleanstring(row.text)
#             print(dict)
#             i = i + 1
#         quarterly_consolidated[header] = dict    
    

#     response1 = requests.get('https://www.screener.in/company/BAJFINANCE/')
#     doc1 = document_fromstring(response.text)
