from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.core.paginator import Paginator
from django.core import serializers
from pricingdata.models import *
from django.db.models import Q
from overall.views import get_param,cleanstring,booleanvar_check, listvar_check, intvar_check, floatvar_check
import json
import operator
import math
from django.views.decorators.csrf import csrf_exempt
operations_allowed_default = ['create','read','update','delete']

# Create your views here.

def create_update_exchange(request):
    error = False
    success = False
    error_message_list = []
    output = Exchange.objects.none()
    message = "Request Recieved"
    operation               = get_param(request, 'operation', None)
    exchange_name           = get_param(request, 'exchange_name', None)      
    exchange_code           = get_param(request, 'exchange_code', None)      
    exchange_country        = get_param(request, 'exchange_country', None)  
    exchange_timezone        = get_param(request, 'exchange_timezone', None)  
    exchange_timezone_short = get_param(request, 'exchange_timezone_short', None) 
    timezone_gmt_off_milliseconds = get_param(request, 'timezone_gmt_off_milliseconds', None)  
    data_id                 = get_param(request, 'data_id', None)      
    # user fields check and correction
    if exchange_name:
        exchange_name = cleanstring(exchange_name)
    else:
        error = True
        error_message_list.append("Missing exchange_name")                               

    if exchange_code:
        exchange_code = cleanstring(exchange_code)
    else:
        if operation=="update":
            pass
        else:
            error = True
            error_message_list.append("Missing exchange_code")                               

    if exchange_timezone:
        exchange_timezone = cleanstring(exchange_timezone)
    else:
        error = True
        error_message_list.append("Missing exchange_timezone")                               


    if exchange_country:
        exchange_country = cleanstring(exchange_country)
    else:
        error = True
        error_message_list.append("Missing exchange_country")                               

    if exchange_timezone_short:
        pass
    else:
        error = True
        error_message_list.append("Missing exchange_timezone_short")                               

    check_time = intvar_check(variable_name="timezone_gmt_off_milliseconds",value=timezone_gmt_off_milliseconds)
    if not check_time['error']:
        timezone_gmt_off_milliseconds = check_time['output']
    else:
        error = check_time['error']
        error_message_list.append(check_time['errormessage'])    

    if operation == "update":
        if data_id:
            try:
                exchange = Exchange.objects.get(id=data_id)
            except:
                error = True
                error_message_list = ['invalid data_id']
        else:
            error = True
            error_message_list = ['missing data_id']
        
    if not error: 
        if operation == "create":
            exchange = Exchange.objects.filter(
                exchange_code=exchange_code
                )
            if exchange.count() > 0 :
                message = "Exchange Already Exists!"        
                output = exchange
                success = False
            else:
                exchange_new = Exchange.objects.create(
                exchange_name = exchange_name
                ,exchange_code = exchange_code
                ,exchange_country = exchange_country
                ,exchange_timezone = exchange_timezone
                ,exchange_timezone_short = exchange_timezone_short
                ,timezone_gmt_off_milliseconds = timezone_gmt_off_milliseconds
                )
                output = [exchange_new]
                success = True
                message = "Exchange Created!"
        else:
            print(exchange_code)
            print(exchange.exchange_code)
            if exchange_code == exchange.exchange_code:
                exchange.exchange_name = exchange_name   
                exchange.exchange_country = exchange_country   
                exchange.exchange_timezone = exchange_timezone   
                exchange.exchange_timezone_short = exchange_timezone_short   
                exchange.timezone_gmt_off_milliseconds = timezone_gmt_off_milliseconds   
                exchange.save()
                success = True
                message = "Exchange Updated!"
                output = [exchange]
            else:
                error = True
                success = False
                error_message_list.append('exchnage code cant be changed exists')
                message = "Exchange code cant be changed"
                output = [exchange]
    else:
        message = "Errors | Refer Error List!"

    return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

def delete_exchange(request):
    error = False
    success = False
    error_message_list = []
    data_id      = get_param(request, 'data_id', None)
    output = Exchange.objects.none()
    message = "Request Recieved"
    if data_id:
        try:
            exchange = Exchange.objects.get(id=data_id)
        except:
            error=True
            error_message_list.append('Incorrect data_id')
    else:
        error = True
        error_message_list.append('Missing data_id')
    if not error: 
        if exchange:
            exchange.delete()
            message = "Exchange Deleted"
            success = True
        else:
            message = "Exchange not found"
            success = False
    else:
        message = "Errors | Refer Error List!"

    return {'output':output,'message':message,'error':error,'error_message_list':error_message_list,'success':success}

def read_exchange(request):
    error = False
    success = False
    error_message_list = []
    message = "Request Recieved!"
    filters = {}
    num_pages = 1
    total_records = 0 
    tranObjs = Exchange.objects.none()
    page_num = get_param(request, 'page_num', "1")
    page_size = get_param(request, 'page_size', "10")
    search = get_param(request,'search',None) 
    sort_by = get_param(request,'sort_by',None) 
    order = get_param(request,'order_by',None)    
    exchange_country = get_param(request,'exchange_country',None) 
    data_id = get_param(request,'data_id',None)    
    
    if data_id != None and data_id != "":
        tranObjs = Exchange.objects.filter(id=data_id)
    else:
        tranObjs = Exchange.objects.all()

        if exchange_country !=None and exchange_country !="" and exchange_country != "none":
            exchange_country_list = exchange_country.split(",")
            tranObjs = tranObjs.filter(exchange_country__in=exchange_country_list)

        # Filters/Sorting Start
        if search !=None and search !="":
            tranObjs = tranObjs.filter(Q(exchange_code__icontains=search) | Q(exchange_name__icontains=search))

        if sort_by !=None and sort_by !="" and sort_by != "none":
            if order == "asc":
                tranObjs = tranObjs.order_by(sort_by)
            else:
                tranObjs = tranObjs.order_by("-" + sort_by)
        # Filters/Sorting End
    # pagination variable

    total_records = tranObjs.count()    
    if page_num != None and page_num != "":
        page_num = int(page_num)
        tranObjs = Paginator(tranObjs, int(page_size))
        try:
            tranObjs = tranObjs.page(page_num)
        except:
            tranObjs = tranObjs
        num_pages = int(math.ceil(total_records / float(int(page_size))))
    # data = list(tranObjs)
    message  = "Success!"
    success = True
    
    exchange_country_list = Exchange.objects.all()
    filters['exchange_country'] = []
    for item in exchange_country_list:
        filters['exchange_country'].append({
            'value':item.exchange_country,
            'label':(item.exchange_country).title()
            })
    filters['exchange_country'] = {v['value']:v for v in filters['exchange_country']}.values()
    filters['exchange_country'] = sorted(filters['exchange_country'], key=operator.itemgetter('value'))

    filters['sort_by'] = [
                        {'value':'exchange_country','label':'Exchange Country'},
                        {'value':'exchange_name','label':'Exchange Name'},
                        {'value':'exchange_code','label':'Exchange Code'}
                       ]
                

    filters['order_by'] = [{'value':'asc','label':'Ascending'},
                           {'value':'desc','label':'Descending'}]

    return({
        'output':tranObjs,
        'num_pages':num_pages,
        'total_records':total_records,
        'error':error,
        'error_message_list':error_message_list,
        'filter':filters,
        'message':message,
        'success':success
    })

def crud_exchange(request):
    obj = {}
    status = False
    result = []
    message = "Request Recieved"
    filters = {}
    tranObjs = Exchange.objects.none()
    operation = get_param(request, 'operation', None)
    error = False
    error_message_list = []
    num_pages = 1
    total_records = 0 
    
    check_operation = listvar_check(variable_name='operation',value=operation,allowedlist=operations_allowed_default)
    if not check_operation['error']:
        if operation == "read":
            out_read_exchange = read_exchange(request) 
            message = out_read_exchange['message']               
            tranObjs = out_read_exchange['output']
            error_message_list.extend(out_read_exchange['error_message_list'])               
            error = out_read_exchange['error']     
            status = out_read_exchange['success']     
            num_pages     = out_read_exchange['num_pages']          
            filters       = out_read_exchange['filter']     
            total_records = out_read_exchange['total_records']          

        if operation in ["create","update"]:
            out_create_update_exchange = create_update_exchange(request) 
            message = out_create_update_exchange['message']               
            tranObjs = out_create_update_exchange['output']
            error_message_list.extend(out_create_update_exchange['error_message_list'])               
            error = out_create_update_exchange['error']   
            status = out_create_update_exchange['success']          

        if operation == "delete":
            out_delete_exchange = delete_exchange(request) 
            message = out_delete_exchange['message']               
            tranObjs = out_delete_exchange['output']               
            error_message_list.extend(out_delete_exchange['error_message_list'])               
            error = out_delete_exchange['error']     
            status = out_delete_exchange['success']           

        if not error:
            for trans in tranObjs:
                result.append({
                    'id':trans.id
                    ,'exchange_name':trans.exchange_name
                    ,'exchange_code':trans.exchange_code
                    ,'exchange_country':trans.exchange_country
                    ,'exchange_timezone':trans.exchange_timezone
                    ,'exchange_timezone_short':trans.exchange_timezone_short
                    ,'timezone_gmt_off_milliseconds':trans.timezone_gmt_off_milliseconds
                    ,'created_at':str(trans.created_at)[:19]
                    ,'modified_at':str(trans.modified_at)[:19]
                })
    
    else:
        error = check_operation['error']
        message = "Operation Not Specified"
        error_message_list.append(check_operation['errormessage'])

    obj['result'] = result
    obj['filter'] = filters
    obj['num_pages'] = num_pages
    obj['total_records'] = total_records
    obj['message'] = message
    obj['status'] = status
    obj['error'] = error
    obj['error_list'] = error_message_list
    return HttpResponse(json.dumps(obj), content_type='application/json')


