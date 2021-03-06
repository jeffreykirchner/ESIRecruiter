from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.decorators import user_is_staff
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import CharField,Q,F,Value as V
from django.db.models.functions import Lower
from django.http import Http404
from django.db import IntegrityError
import logging
from main.models import profile_note,help_docs

@login_required
@user_is_staff
def userInfo(request,id=None):

    if request.method == 'POST':       

        data = json.loads(request.body.decode('utf-8'))

        if data["status"] == "getInvitations":
            return getInvitations(data,id)
        elif data["status"] == "getSessions":
            return getSessions(data,id)  
        elif data["status"] == "makeNote":
            return makeNote(request,data,id) 
        elif data["status"] == "deleteNote":
            return deleteNote(request,data,id)       
        elif data["status"] == "getTraits":
            return getTraits(data,id)  
                   
    else:     
        try:
            helpText = help_docs.objects.annotate(rp = V(request.path,output_field=CharField()))\
                                    .filter(rp__icontains = F('path')).first().text

        except Exception  as e:   
             helpText = "No help doc was found."

        u=User.objects.get(id=id) 
        return render(request,'staff/userInfo.html',{"u":u,
                                                     "id":id,
                                                     "helpText":helpText,
                                                     "experiments":u.ESDU.all() })  

#store a note about the user
def makeNote(request,data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Make a note")
    logger.info(data)

    u=User.objects.get(id=id)

    n = profile_note()
    n.my_profile = u.profile
    n.noteMaker = request.user
    n.text = data["text"].strip().capitalize()

    if n.text != "":
        n.save()

    return getSessions(data,id)

#delete the selected note
def deleteNote(request,data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Delete Note")
    logger.info(data)

    note_id = data["id"]
    n = profile_note.objects.get(id=note_id)

    if request.user.is_superuser:
        n.delete()

    return getSessions(data,id)

#get full is of subject invitions
def getInvitations(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Get invitations")
    logger.info(data)

    u=User.objects.get(id=id)

    return JsonResponse({"invitations" :  u.profile.sorted_session_day_list_full(),
                                },safe=False)

#get the session and notes subject has participated in
def getSessions(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("User Info: Get sessions")
    logger.info(data)

    u=User.objects.get(id=id)

    return JsonResponse({"session_day_attended" :  u.profile.sorted_session_day_list_earningsOnly(),
                         "session_day_upcoming" :  u.profile.sorted_session_day_list_upcoming(True),
                         "institutions" : u.profile.get_institution_list(),
                         "notes" : u.profile.get_notes(),
                            },safe=False,
                        )

#get the traits for this subject
def getTraits(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("User Info: Get Traits")
    logger.info(data)

    u=User.objects.get(id=id)

    return JsonResponse({"subject_traits" :  u.profile.sorted_trait_list(),
                            },safe=False,
                        )
