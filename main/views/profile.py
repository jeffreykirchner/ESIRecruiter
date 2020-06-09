from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import profileFormUpdate
from .profileCreate import profileCreateSendEmail

from django.conf import settings

import requests
import logging

#user account info
@login_required
def profile(request):
    logger = logging.getLogger(__name__)     

    try:
        status="update"            #either filling out the form or 
        u=request.user
        
        if request.method == 'POST':
            form = profileFormUpdate(request.POST,user=request.user)

            print(request.POST)

            if form.is_valid():                           

                emailVerificationRequired=False

                if u.email != form.cleaned_data['email'].lower():
                    emailVerificationRequired=True
                
                u.first_name=form.cleaned_data['first_name']
                u.last_name=form.cleaned_data['last_name']
                u.email=form.cleaned_data['email'].lower()
                u.username=u.email
                u.profile.chapmanID=form.cleaned_data['chapman_id']
                u.profile.gender=form.cleaned_data['gender']

                if form.cleaned_data['password1']:
                    if form.cleaned_data['password1'] != "":               
                        u.set_password(form.cleaned_data['password1'])                    

                if emailVerificationRequired:
                    u.is_active=False                                
                    profileCreateSendEmail(request,u)

                u.save()
                status="done"
        else:
            form = profileFormUpdate(
                initial={'first_name': request.user.first_name,
                         'last_name': request.user.last_name,
                         'chapman_id': request.user.profile.chapmanID,
                         'email':request.user.email,
                         'gender':request.user.profile.gender.id}
            )

    except u.DoesNotExist:
        raise Http404('Profile not found')

    logger.info("Profile fitbit test:")
    logger.info(r)

    fitBitAttached = False
    if 'weight' in r:
        fitBitAttached = True
    
    logger.info("Profile fitbit attached:")
    logger.info(fitBitAttached)

    return render(request,'profile.html',{'form': form,
                                          'status':status,
                                          'fitBitLink' : fitBitLink,
                                          'fitBitAttached' : fitBitAttached})    



