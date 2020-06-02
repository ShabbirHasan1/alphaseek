from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse

import base64
import datetime
import re
import random
import string
import time
from datetime import datetime
import os

# Create your views here.

boolean_fields = ['0','1']
# Generic Functions
def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

# <---------------- Get parameters in an api from request  start ------------------->

def get_param(req, param, default):
    req_param = None
    if req.method == 'GET':
        q_dict = req.GET
        if param in q_dict:
            req_param = q_dict[param]
    elif req.method == 'POST':
        q_dict = req.POST
        if param in q_dict:
            req_param = q_dict[param]
    if not req_param and default != None:
        req_param = default
    return req_param

# <---------------- Set Cookie ------------------->

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

# Random String Generator

def random_str_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


    
def intvar_check(variable_name,value,missing_allowed=False):
    output = None
    error_message = "No Errors"
    error = False
    is_missing = False
    if value  != "" and value != None:
        try:
            if value != "":
                output = int(value)
            else:
                output = None
        except:
            error = True
            error_message = 'Incorrect '+variable_name + ' | values: integers'
    else:
        is_missing = True
        if not missing_allowed:
            error = True
            error_message = 'Missing '+ variable_name
        else:
            pass
    return {'output':output,'error': error, 'errormessage':error_message,'is_missing' : is_missing}

def floatvar_check(variable_name,value,missing_allowed=False):
    output = None
    error_message = "No Errors"
    error = False
    is_missing = False
    # print value
    if value  != "" and value != None:
        try:
            if value != "":
                output = float(value)
            else:
                output = None
        except:
            error = True
            error_message = 'Incorrect '+variable_name + ' | values: float'
    else:
        is_missing = True
        if not missing_allowed:
            error = True
            error_message = 'Missing '+ variable_name
        else:
            pass

    return {'output':output,'error': error, 'errormessage':error_message,'is_missing' : is_missing}


def listvar_check(variable_name,value,allowedlist,missing_allowed=False):
    output = None
    error_message = "No Errors"
    error = False
    is_missing = False
    if value  != "" and value != None:
        if value in allowedlist:
            output = str(value)
        else:
            error = True
            error_message = 'Incorrect '+variable_name + ' | values: ' + str(allowedlist)
    else:
        is_missing = True
        if not missing_allowed:
            error = True
            error_message = 'Missing '+ variable_name
        else:
            pass
    return {'output':output,'error': error, 'errormessage':error_message,'is_missing' : is_missing}



def booleanvar_check(variable_name,value):
    output = None
    error_message = "No Errors"
    error = False

    if value  != "" and value != None:
        if value in boolean_fields:
            if value == "1":
                output = True
            else:
                output = False
        else:
            error = True
            error_message = 'Incorrect '+variable_name + ' | values: ' + str(boolean_fields)
    else:
        error = True
        error_message = 'Missing '+ variable_name

    return {'output':output,'error': error, 'errormessage':error_message}


