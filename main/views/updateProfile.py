from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from main.forms import profileFormUpdate
from main.globals.sendEmail import profileCreateSendEmail
from django.db.models import CharField,Q,F,Value as V
from main.models import help_docs

from django.conf import settings

import requests
import logging

#user account info
@login_required
def updateProfile(request):
    logger = logging.getLogger(__name__)     

    try:
        status="update"            #either filling out the form or 
        emailVerificationRequired=False
        u=request.user
        
        if request.method == 'POST':
            form = profileFormUpdate(request.POST,user=request.user)

            #print(request.POST)

            if form.is_valid():                         

                if u.email != form.cleaned_data['email'].lower():
                    emailVerificationRequired=True
                
                u.first_name=form.cleaned_data['first_name'].strip().capitalize()
                u.last_name=form.cleaned_data['last_name'].strip().capitalize()
                u.email=form.cleaned_data['email'].strip().lower()
                u.username=u.email

                u.profile.studentID=form.cleaned_data['chapman_id'].strip()
                u.profile.gender=form.cleaned_data['gender']
                u.profile.subjecType = form.cleaned_data['subject_type']
                u.profile.studentWorker = form.cleaned_data['studentWorker']
                u.profile.phone = form.cleaned_data['phone'].strip()
                u.profile.major = form.cleaned_data['major']
                u.profile.paused = form.cleaned_data['paused']

                if form.cleaned_data['password1']:
                    if form.cleaned_data['password1'] != "":               
                        u.set_password(form.cleaned_data['password1'])                    

                if emailVerificationRequired:
                    #u.is_active=False     
                    u.profile.email_confirmed="no"                           
                    profileCreateSendEmail(request,u)

                u.save()
                u.profile.save()
                u.profile.setup_email_filter()
                status="done"
        else:
            logger.info("show profile")

            form = profileFormUpdate(
                initial={'first_name': request.user.first_name,
                         'last_name': request.user.last_name,
                         'chapman_id': request.user.profile.studentID,
                         'email':request.user.email,
                         'gender':request.user.profile.gender.id,
                         'phone':request.user.profile.phone,
                         'major':request.user.profile.major.id,
                         'subject_type':request.user.profile.subject_type.id,
                         'studentWorker':"Yes" if request.user.profile.studentWorker else "No",
                         'paused':"Yes" if request.user.profile.paused else "No"}
            )

    except u.DoesNotExist:
        raise Http404('Profile not found')

    try:
        helpText = help_docs.objects.annotate(rp = V(request.path,output_field=CharField()))\
                                .filter(rp__icontains = F('path')).first().text

    except Exception  as e:   
        helpText = "No help doc was found."

    return render(request,'profile.html',{'form': form,
                                          'status':status,
                                          'helpText':helpText,
                                          'emailVerificationRequired':emailVerificationRequired})    



