'''
History of transanctions send to PayPal API.
'''
from datetime import datetime, timedelta

import json
import logging
import requests
import pytz
from requests.utils import quote

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import CharField, F, Value as V
from django.conf import settings

from main.decorators import user_is_staff

from main.models import parameters, help_docs
from main.globals import make_tz_aware_utc

@login_required
@user_is_staff
@staff_member_required
def PayPalHistory(request):
    '''
    Handle incoming requestst
    '''

    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "getHistory":
            return get_history(request, data)

        return JsonResponse({"error" : "error"}, safe=False)

    #get
    try:
        help_text = help_docs.objects.annotate(rp=V(request.path, output_field=CharField()))\
                                     .filter(rp__icontains=F('path')).first().text

    except Exception as exce:
        help_text = "No help doc was found."

    param = parameters.objects.first()
    tmz = pytz.timezone(param.subjectTimeZone)
    d_today = datetime.now(tmz)
    d_one_year = d_today - timedelta(days=1)

    return render(request, 'staff/payPalHistory.html', {"helpText" : help_text,
                                                        "d_today" : d_today.date().strftime("%Y-%m-%d"),
                                                        "d_one_year" : d_one_year.date().strftime("%Y-%m-%d")})     

#return list of users based on search criterion
def get_history(request, data):
    '''
    Get the paypal history in the given range.
    '''
    logger = logging.getLogger(__name__)
    logger.info(f"PayPal History {data}")

    #request.session['userSearchTerm'] = data["searchInfo"]            
    history = get_paypal_history_list(data["startDate"], data["endDate"])

    return JsonResponse({"history" : history['history'], "errorMessage":history['error_message']}, safe=False)

def get_paypal_history_list(start_date, end_date):
    '''
    return a formated list of paypal payments over the specficed date range
    date format YYYY-MM-DD

    '''
    logger = logging.getLogger(__name__)

    history = []
    error_message = ""

    param = parameters.objects.first()
    tmz = pytz.timezone(param.subjectTimeZone)

    try:

        #convert dates to UTC
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # start_date = make_tz_aware_utc(start_date, 0, 0, 0).date()
        # end_date = make_tz_aware_utc(end_date, 23, 59, 59).date()

        subject_time_zone_safe = quote(param.subjectTimeZone, safe='')

        req = requests.get(f'{settings.PPMS_HOST}/payments/{start_date}/{end_date}/{subject_time_zone_safe}',
                           auth=(str(settings.PPMS_USER_NAME), str(settings.PPMS_PASSWORD)))

        #logger.info(r.status_code)

        if req.status_code != 200:
            error_message = req.json().get("detail")
        else:
            history = req.json()            

            for hst in history:
                #convert earnings
                hst["amount"] = float(hst["amount"])
                hst["amount"] = f'${hst["amount"]:.2f}'

                #convert date
                hst["timestamp"] = datetime.strptime(hst["timestamp"], '%m/%d/%Y %H:%M:%S %Z')
                hst["timestamp"] = hst["timestamp"].astimezone(tmz).strftime("%#m/%#d/%Y %#I:%M %p")

    except Exception  as exce:
            logger.warning(f'PayPalHistory Error: {exce}')
            error_message = "Unable to retrieve history."
    
    return {'history' : history, 'error_message' : error_message}




