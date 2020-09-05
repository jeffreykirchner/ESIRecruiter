from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.decorators import user_is_staff
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from main.models import experiments,experiment_session_days,schools,accounts,recruitmentParameters
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import Lower
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import redirect

@login_required
@user_is_staff
def experimentSearch(request):
    logger = logging.getLogger(__name__) 
    
    
    # logger.info("some info")

    if request.method == 'POST':       

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "searchExperiments":
            return searchExperiments(data)
        elif data["action"] == "getAllExperiments":
            return getAllExperiments(data)
        elif data["action"] == "getOpenExperiments":
            return getOpenExperiments(data)
        elif data["action"] == "createExperiment":
            return createExperiment(data)   
        elif data["action"] == "deleteExperiment":
            return deleteExperiment(data)     
           
        return JsonResponse({"status" :  "error"},safe=False)       
    else:      
        return render(request,'staff/experimentSearch.html',{"u":"" ,"id":""})      

#create experiment
def createExperiment(data):
    logger = logging.getLogger(__name__)
    logger.info("Create Experiment")
    logger.info(data)

    rp = recruitmentParameters()

    e = experiments()
    e.school = schools.objects.first()
    e.account_default = accounts.objects.first()
    e.recruitmentParamsDefault = rp

    rp.save()
    e.save()    

    return JsonResponse({"experiments" : [e.json_search()]},safe=False)

#serach for an experiment
def searchExperiments(data):
    logger = logging.getLogger(__name__)
    logger.info("Search Experiments")
    logger.info(data)

    e_list_json = lookup(data["searchInfo"])

    return JsonResponse({"experiments" : e_list_json},safe=False)

#delete selected experiment
def deleteExperiment(data):
    logger = logging.getLogger(__name__)
    logger.info("Delete Experiment")
    logger.info(data)

    status = ""

    id = data["id"]

    e = experiments.objects.get(id=id)

    title = e.title

    if e.allowDelete():
        e.delete()
        status="success"
    else:
        status="fail"

    return JsonResponse({"status" : status,"title":title},safe=False)

#get a list of all experiments
def getAllExperiments(data):
    logger = logging.getLogger(__name__)
    logger.info("Get All Experiments")
    logger.info(data)

    e_list=experiments.objects.order_by(Lower("title"))         
    
    e_list_json = [e.json_search() for e in e_list]

    return JsonResponse({"experiments" : e_list_json},safe=False)

#get a list of all experiments
def getOpenExperiments(data):
    logger = logging.getLogger(__name__)
    logger.info("Get Open Experiments")
    logger.info(data)

    esd_open = experiment_session_days.objects.annotate(user_count = Count('experiment_session_day_users'))\
                                      .filter(user_count__gt = 0)\
                                      .filter(complete=False)\
                                      .values_list('experiment_session__experiment__id',flat=True)

    # logger.info(list(esd_open))

    e_list=experiments.objects.filter(id__in=esd_open)\
                              .distinct()\
                              .order_by(Lower("title"))
    
    e_list_json = [e.json_search() for e in e_list]

    return JsonResponse({"experiments" : e_list_json},safe=False)

#search for users that back search criterion
def lookup(value):
    logger = logging.getLogger(__name__)
    logger.info("Experiment Lookup")
    logger.info(value)

    value = value.strip()

    e_list = experiments.objects.order_by(Lower('title')) \
                      .filter(Q(title__icontains = value) |
                              Q(experiment_manager__icontains = value) |
                              Q(notes__icontains = value))


    e_list_json = [e.json_search() for e in e_list]

    return e_list_json