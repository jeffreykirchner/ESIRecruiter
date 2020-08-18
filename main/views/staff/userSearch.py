from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.decorators import user_is_staff
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import CharField,Q,F,Value as V
from django.db.models.functions import Lower,Concat
from django.urls import reverse
from main import views
import logging
from django.db.models import OuterRef, Subquery
from django.db.models import Count
from main.models import parameters
from datetime import datetime, timedelta,timezone

@login_required
@user_is_staff
def userSearch(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "getUsers":
            logger = logging.getLogger(__name__)
            logger.info("User Search")
            logger.info(data)

            request.session['userSearchTerm'] = data["searchInfo"]            
            activeOnly = data["activeOnly"] 

            users = lookup(data["searchInfo"],False,activeOnly)            

            errorMessage=""

            if(len(users) >= 1000):
                errorMessage = "Narrow your search"
                users=[]          

            return JsonResponse({"users" : json.dumps(users,cls=DjangoJSONEncoder),"errorMessage":errorMessage},safe=False)
        elif data["action"] == "getBlackBalls":
            logger = logging.getLogger(__name__)
            logger.info("Black Balls")
            logger.info(data)

            errorMessage=""
            activeOnly = data["activeOnly"] 

            users=User.objects.order_by(Lower('last_name'),Lower('first_name')) \
                      .filter(profile__blackballed=True) \
                      .select_related('profile') \
                      .values("id","first_name","last_name","email","profile__chapmanID","profile__type__name","is_active","profile__blackballed")
           
            if activeOnly:
                users = users.filter(is_active = True)

            u_list = list(users)

            return JsonResponse({"users" :  json.dumps(u_list,cls=DjangoJSONEncoder),"errorMessage":errorMessage},safe=False)
        elif data["action"] == "getNoShows":
            logger = logging.getLogger(__name__)
            logger.info("Get no show blocks")
            logger.info(data)

            p = parameters.objects.get(id=1)
            d = datetime.now(timezone.utc) - timedelta(days=p.noShowCutoffWindow)

            errorMessage = ""
            activeOnly = data["activeOnly"] 

            users=User.objects.order_by(Lower('last_name'),Lower('first_name')) \
                      .filter(Q(ESDU__confirmed = True) &
                            Q(ESDU__attended = False) &
                            Q(ESDU__bumped = False) & 
                            Q(ESDU__experiment_session_day__experiment_session__canceled = False) &
                            Q(ESDU__experiment_session_day__date__gte = d))\
                      .annotate(noShows = Count('id'))\
                      .filter(noShows__gte = p.noShowCutoff)\
                      .values("id","first_name","last_name","email","profile__chapmanID","profile__type__name","is_active","profile__blackballed")

            #logger.info(users.query)

            if activeOnly:
                users = users.filter(is_active = True)

            u_list = list(users)

            return JsonResponse({"users" :  json.dumps(u_list,cls=DjangoJSONEncoder),"errorMessage":errorMessage},safe=False)

    else:
        activeCount = User.objects.filter(is_active = True,profile__subjectType__id = 1).count()
        return render(request,'staff/userSearch.html',{"activeCount":activeCount})      



def lookup(value,returnJSON,activeOnly):
    logger = logging.getLogger(__name__)
    logger.info("User Lookup")
    logger.info(value)

    users=User.objects.order_by(Lower('last_name'),Lower('first_name')) \
                      .filter(Q(last_name__icontains = value) |
                              Q(first_name__icontains = value) |
                              Q(email__icontains = value) |
                              Q(profile__chapmanID__icontains = value) |
                              Q(profile__type__name__icontains = value))\
                      .select_related('profile')\
                      .values("id","first_name","last_name","email","profile__chapmanID","profile__type__name","is_active","profile__blackballed")


    if activeOnly:
        users = users.filter(is_active = True)

    u_list = list(users)

    logger.info(str(len(u_list)) + " results found.")

    for u in u_list:
        u['first_name'] = u['first_name'].capitalize()
        u['last_name'] = u['last_name'].capitalize()

    if returnJSON:
        #print(json.dumps(list(users),cls=DjangoJSONEncoder))
        return json.dumps(u_list,cls=DjangoJSONEncoder)
    else:
        return u_list
