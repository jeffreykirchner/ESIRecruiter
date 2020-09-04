from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.decorators import user_is_staff
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from decimal import *
from django.db.models import Q,F
import random
import csv
from django.http import HttpResponse
from datetime import datetime, timedelta,timezone

from main.models import experiment_session_days,experiment_session_day_users,profile

@login_required
@user_is_staff
def experimentSessionRunView(request,id=None):
    logger = logging.getLogger(__name__) 
        
    # logger.info("some info")

    if request.method == 'POST':       

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "getSession":
            return getSession(data,id)
        elif data["action"] == "attendSubject":
            return attendSubject(data,id)
        elif data["action"] == "bumpSubject":
            return bumpSubject(data,id)
        elif data["action"] == "noShowSubject":
            return noShowSubject(data,id)
        elif data["action"] == "savePayouts":
            return savePayouts(data,id)
        elif data["action"] == "completeSession":
            return completeSession(data,id)
        elif data["action"] == "fillDefaultShowUpFee":
            return fillDefaultShowUpFee(data,id)
        elif data["action"] == "backgroundSave":
            return backgroundSave(data,id)
        elif data["action"] == "bumpAll":
            return bumpAll(data,id)
        elif data["action"] == "autoBump":
            return autoBump(data,id)
        elif data["action"] == "payPalExport":
            return getPayPalExport(data,id)
           
        return JsonResponse({"response" :  "error"},safe=False)       
    else:      
        esd = experiment_session_days.objects.get(id=id)
        return render(request,'staff/experimentSessionRunView.html',{"sessionDay":esd ,"id":id})  

#return the session info to the client
def getSession(data,id):    
    logger = logging.getLogger(__name__)
    logger.info("Get Session Day")
    logger.info(data)

    esd = experiment_session_days.objects.get(id=id)

    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#return paypal CSV
def getPayPalExport(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Pay Pal Export")
    logger.info(data)

    esd = experiment_session_days.objects.get(id=id)
    esdu = esd.experiment_session_day_users_set.filter(Q(show_up_fee__gt = 0) | Q(earnings__gt = 0))

    csv_response = HttpResponse(content_type='text/csv')
    csv_response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(csv_response)

    for u in esdu:
        writer.writerow(u.csv_payPal())  
    
    return csv_response

#automatically randomly bump exccess subjects
def autoBump(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Auto Bump")
    logger.info(data)

    esd = experiment_session_days.objects.get(id=id)

    esdu_attended = esd.experiment_session_day_users_set.filter(attended=True)

    attendedCount = esdu_attended.count()
    bumpsNeeded = attendedCount - esd.experiment_session.recruitmentParams.actual_participants

    esdu_attended_not_bumped=[]

    for e in esdu_attended:
        if not e.user.profile.bumped_from_last_session(e.id):
            esdu_attended_not_bumped.append(e)

    #logger.info(esdu_attended_not_bumped)

    if bumpsNeeded>len(esdu_attended_not_bumped):
            bumpsNeeded = len(esdu_attended_not_bumped)

    if bumpsNeeded > 0:        

        randomSample = random.sample(esdu_attended_not_bumped, bumpsNeeded)
        
        for u in randomSample:
            u.attended = False
            u.bumped = True
            u.save()    
    
    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#bump all subjects marked as attended
def bumpAll(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Bump All")
    logger.info(data)

    esd = experiment_session_days.objects.get(id=id)
    esd.experiment_session_day_users_set.filter(attended=True) \
                                        .update(attended = False,bumped = True) 

    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#save the payouts when user changes them
def backgroundSave(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Background Save")
    logger.info(data)

    payoutList = data['payoutList']

    #time_start = datetime.now()

    esdu_list=[]

    for p in payoutList:
        #logger.info(p)
        esdu  = experiment_session_day_users.objects.get(id = p['id'])

        try:
            esdu.earnings = max(0,Decimal(p['earnings']))
            esdu.show_up_fee = max(0,Decimal(p['showUpFee']))
        except (ValueError, DecimalException):
            logger.info("Background Save Error : ")
            logger.info(p)
            esdu.earnings = 0
            esdu.show_up_fee = 0
        
        esdu_list.append(esdu)

    experiment_session_day_users.objects.bulk_update(esdu_list, ['earnings','show_up_fee'])

    status="success"

    #time_end = datetime.now()
    #time_span = time_end-time_start

    #logger.info("SQL Run time: " + str(time_span.total_seconds()))

    return JsonResponse({"status" :status }, safe=False)

#save the currently entered payouts
def savePayouts(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Save Payouts")
    logger.info(data)

    payoutList = data['payoutList']

    esdu_list = []

    for p in payoutList:
        #logger.info(p)
        esdu  = experiment_session_day_users.objects.get(id = p['id'])

        try:
            esdu.earnings = max(0,Decimal(p['earnings']))
            esdu.show_up_fee = max(0,Decimal(p['showUpFee']))

        except (ValueError, DecimalException):
            logger.info("Background Save Error : ")
            logger.info(p)
            esdu.earnings = 0
            esdu.show_up_fee = 0
        
        esdu_list.append(esdu)
    
    experiment_session_day_users.objects.bulk_update(esdu_list, ['earnings','show_up_fee'])

    esd = experiment_session_days.objects.get(id=id)

    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#close session and prevent further editing
def completeSession(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Complete Session")
    logger.info(data)

    esd = experiment_session_days.objects.get(id=id)

    esd.complete = not esd.complete
    esd.save()

    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#fill subjects with default bump fee set in the experiments model
def fillDefaultShowUpFee(data,id):
    logger = logging.getLogger(__name__)
    logger.info("Fill Default Show Up Fee")
    logger.info(data)

    esd = experiment_session_days.objects.get(id=id)

    showUpFee = esd.experiment_session.experiment.showUpFee

    esd.experiment_session_day_users_set.filter(Q(attended=True)|Q(bumped=True)) \
                                        .update(show_up_fee = showUpFee)


    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#mark subject as attended
def attendSubject(data,id):    
    logger = logging.getLogger(__name__)
    logger.info("Attend Subject")
    logger.info(data)

    esdu = experiment_session_day_users.objects.get(id=data['id'])

    esdu.attended=True
    esdu.bumped=False
    esdu.save()

    esd = experiment_session_days.objects.get(id=id)

    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#mark subject as bumped
def bumpSubject(data,id):    
    logger = logging.getLogger(__name__)
    logger.info("Bump Subject")
    logger.info(data)

    esdu = experiment_session_day_users.objects.get(id=data['id'])

    esdu.attended=False
    esdu.bumped=True
    esdu.save()

    esd = experiment_session_days.objects.get(id=id)

    return JsonResponse({"sessionDay" : esd.json_runInfo() }, safe=False)

#mark subject as no show
def noShowSubject(data,id):    
    logger = logging.getLogger(__name__)
    logger.info("No Show")
    logger.info(data)

    esdu = experiment_session_day_users.objects.get(id=data['id'])

    esdu.attended=False
    esdu.bumped=False
    esdu.save()

    esd = experiment_session_days.objects.get(id=id)

    return JsonResponse({"sessionDay" : esd.json_runInfo()  }, safe=False)