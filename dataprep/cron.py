from dataprep import views as clean_data
from datetime import datetime

def nse_return_calculate():
    print('ran nse_return_calculate')
    timestart = str(datetime.now())
    print('start time - ' + timestart)
    clean_data.ReturnCalculate.calculate_all_returns()
    clean_data.ReturnCalculate.calculate_all_index_returns()
    clean_data.UpdateTicker.update_all_company()
    clean_data.UpdateTicker.update_all_index()
    timeend = str(datetime.now())
    print('end time - ' + timeend)

# def update_company_details():
#     print('ran update_company_details')
#     timestart = str(datetime.now())
#     print('start time - ' + timestart)
    
#     print('end time - ' + timeend)