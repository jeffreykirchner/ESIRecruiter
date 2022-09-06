from datetime import datetime, timedelta

import json
import logging
import pytz

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, F, Value, CharField
from django.db.models import Count
from django.views import View
from django.utils.decorators import method_decorator

from main.models import help_docs
from main.models import experiments
from main.models import experiment_sessions
from main.models import parameters

from main.decorators import user_is_staff

from main.forms import IrbReportForm

class IrbReport(View):
    '''
    irb report view
    '''

    template_name = "staff/irb_report.html"

    @method_decorator(login_required)
    @method_decorator(user_is_staff)
    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        logger = logging.getLogger(__name__)

        try:
            helpText = help_docs.objects.annotate(rp = Value(request.path,output_field=CharField()))\
                                        .filter(rp__icontains = F('path')).first().text

        except Exception  as e:   
             helpText = "No help doc was found."

        form_ids=[]
        for i in IrbReportForm():
            form_ids.append(i.html_name)

        param = parameters.objects.first()
        tmz = pytz.timezone(param.subjectTimeZone)
        d_today = datetime.now(tmz)

        #start of fiscal year
        d_fisical_start = d_today
        d_fisical_start = d_fisical_start.replace(month=6, day=1)

        return render(request, self.template_name, {"helpText":helpText,
                                                    "form_ids":form_ids,
                                                    "d_today" : d_today.date().strftime("%Y-%m-%d"),
                                                    "d_fisical_start" : d_fisical_start.date().strftime("%Y-%m-%d"),
                                                    "irb_report_form":IrbReportForm()})
    
    @method_decorator(login_required)
    @method_decorator(user_is_staff)
    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''

        logger = logging.getLogger(__name__) 

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "getIrbForm":
            return getIrbForm(data)
        
        return JsonResponse({"status" :  "error"},safe=False)    

#get a list of all open sessions
def getIrbForm(data):
    logger = logging.getLogger(__name__)
    logger.info(f"Get IRB Form: {data}")

    form_data_dict = {}

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]
    
    form = IrbReportForm(form_data_dict)

    if form.is_valid():
        irb_study = form.cleaned_data['irb_study']

        irb_report = {}
        irb_report['irb_study'] = irb_study.json()
        irb_report['start_range'] = form.cleaned_data['start_range'].strftime("%-m-%-d-%Y")
        irb_report['end_range'] = form.cleaned_data['end_range'].strftime("%-m-%-d-%Y")

        irb_report['PIs'] = {}

        for consent_form in irb_study.consent_forms.all():
            for session in consent_form.ES_c.all():
                subject_count = session.ESD.first().ESDU_b.filter(attended=True).count()

                if session.budget:
                   
                    if not session.budget.id in irb_report['PIs']:
                        irb_report['PIs'][session.budget.id] = {"name":f"{session.budget.last_name}, {session.budget.first_name}",
                                                                "experiments":{},
                                                                "subject_count":0}

                    irb_report['PIs'][session.budget.id]["subject_count"] += subject_count
                    irb_report['PIs'][session.budget.id]["experiments"][session.experiment.id] = {"id":session.experiment.id, "title":session.experiment.title}
                else:
                    if not "No Budget" in irb_report['PIs']:
                        irb_report['PIs']["No Budget"] = {"name":"No Budget",
                                                          "experiments":{},
                                                          "subject_count":0}

                    irb_report['PIs']["No Budget"]["subject_count"] += subject_count
                    irb_report['PIs']["No Budget"]["experiments"][session.experiment.id] = {"id":session.experiment.id, "title":session.experiment.title}


        return JsonResponse({"status":"success", "irb_report": irb_report}, safe=False)
    
    else:
        logger.info("invalid IRB report form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False) 
   