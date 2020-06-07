from dataclean import views as clean_data
from datetime import datetime

def nse_return_calculate():
    print('ran nse_return_calculate')
    timestart = str(datetime.now())
    print('start time - ' + timestart)
    clean_data.ReturnCalculate.calculate_all_returns()
    timeend = str(datetime.now())
    print('end time - ' + timeend)

