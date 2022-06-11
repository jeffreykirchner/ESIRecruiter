from datetime import datetime, timedelta

import json
import logging
import pytz

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import CharField, Q, F, Value as V
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from main.models import experiment_session_day_users
from main.models import parameters
from main.models import help_docs
from main.models import ConsentForm
from main.models import ProfileConsentForm
from main.models import experiment_sessions

from main.decorators import user_is_subject
from main.decorators import email_confirmed

@login_required
@user_is_subject
@email_confirmed
def subjectInvitation(request, id):
    logger = logging.getLogger(__name__) 
       
    # logger.info("some info")
    u=request.user  

    if request.method == 'POST':     

        data = json.loads(request.body.decode('utf-8'))
           
        return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        p = parameters.objects.first()

        labManager = p.labManager

        try:
            helpText = help_docs.objects.annotate(rp = V(request.path,output_field=CharField()))\
                                        .filter(rp__icontains = F('path')).first().text

        except Exception  as e:   
            helpText = "No help doc was found."

        try:
            subject_session_list = u.ESDU.values_list('experiment_session_day__experiment_session__id',flat=True)
            session = experiment_sessions.objects.filter(id__in=subject_session_list).filter(id=id)

            # logger.info(subject_session_list)
            # logger.info(session)

            if not session:
                raise Http404('Consent Form Not Found')

        except ObjectDoesNotExist :
            raise Http404('Consent Form Not Found')

        
        if (session_invitation := u.experiment_session_invitation_users.filter(experiment_session=session.first()).first()):
            invitation_text = session_invitation.get_message_text_filled(u)
        else:
            invitation_text = "Invitation text not found."
    
        return render(request,'subject/invitation.html',{"labManager":labManager,
                                                           "invitation_html": invitation_text,
                                                           "helpText":helpText})      

#subject accepts consent form
def acceptConsentForm(data, u):
    '''
    Subject accepts consent form
    
    :param data: Form data{} empty
    :type data: dict

    :param u: Subject User
    :type u: django.contrib.auth.models.User
    '''

    logger = logging.getLogger(__name__)
    logger.info("Accept consent form")    
    logger.info(data)

    failed = False

    try:

        consent_form = ConsentForm.objects.get(id=data["consent_form_id"])
        signature_points = data["consent_form_signature"]
        singnature_resolution = data["consent_form_signature_resolution"]

        profile_consent_form = ProfileConsentForm(my_profile=u.profile, 
                                                 consent_form=consent_form, 
                                                 signature_points=signature_points,
                                                 singnature_resolution=singnature_resolution)
        profile_consent_form.save()

    except Exception  as e:
        logger.warning("accept consent form error")             
        logger.warning("User: " + str(u.id))    
        logger.warning(e)
        failed = True

    return JsonResponse({"failed":failed,
                         "consent_form_subject_json": json.dumps(profile_consent_form.json(),cls=DjangoJSONEncoder) if profile_consent_form else json.dumps(None,cls=DjangoJSONEncoder),
                         }, safe=False)