from django.db import models
import logging
import traceback
from datetime import datetime
from datetime import timedelta  
from django.utils import timezone
from django.db.models import F
from django.db.models import Q
import pytz
from django.db.models.functions import Lower
import json
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from . import experiment_sessions,locations,accounts,parameters
import main
from django.utils.timezone import now

from pytz import timezone


#one day of a session
class experiment_session_days(models.Model):
    experiment_session = models.ForeignKey(experiment_sessions,on_delete=models.CASCADE,related_name='ESD')
    location = models.ForeignKey(locations,on_delete=models.CASCADE)
    account = models.ForeignKey(accounts,on_delete=models.CASCADE)

    date = models.DateTimeField(default=now)                            #date and time of session 
    length = models.IntegerField(default=60)                            #length of session in minutes
    date_end = models.DateTimeField(default=now)                        #date and time of session end, calculated from date and length   
    auto_reminder = models.SmallIntegerField (default=1)                #finanical account used to pay subjects from
    complete = models.BooleanField(default=False)                       #locks the session day once the user has pressed the complete button
    reminderEmailSent = models.BooleanField(default=False)              #true once the reminder email is sent to subjects

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return "ID: " + str(self.id)

    class Meta:
        verbose_name = 'Experiment Session Days'
        verbose_name_plural = 'Experiment Session Days'

    #get list of user and confirmed status
    def getListOfUserIDs(self):
        u_list=[]

        for u in self.experiment_session_day_users_set.all():
            u_list.append({'user':u.user,'confirmed':u.confirmed})

        #u_list.sort()

        return u_list

    #add user to session day
    def addUser(self,userID,staffUser,manuallyAdded):
        esdu = main.models.experiment_session_day_users()

        esdu.experiment_session_day = self
        esdu.user = User.objects.get(id=userID)
        esdu.addedByUser = staffUser
        esdu.manuallyAdded = manuallyAdded

        esdu.save()

    #sets up session day with defualt parameters
    def setup(self,es,u_list):
        self.experiment_session=es
        self.location = locations.objects.first()
        self.length=es.experiment.length_default
        self.account = es.experiment.account_default    
        self.date = now()

        self.save()

        #add list of session users if multiday
        for u in u_list:
            esdu = main.models.experiment_session_day_users()
            esdu.user = u['user']
            esdu.confirmed = u['confirmed']
            esdu.experiment_session_day = self
            esdu.save()

    #check if this session day can be deleted
    def allowDelete(self):

        # ESDU = self.experiment_session_day_users_set.filter((Q(attended = 1) & (Q(earnings__gt = 0) | Q(show_up_fee__gt = 0))) | 
        #                                                     (Q(bumped = 1) & Q(show_up_fee__gt = 0)))\
        #                                             .exists()

        ESDU = self.experiment_session_day_users_set.filter(confirmed = True).exists()

        if ESDU:
            return False
        else:
            return True  

    #get user readable string of session date
    def getDateString(self):
        p = parameters.objects.first()
        return  self.date.astimezone(timezone(p.subjectTimeZone)).strftime("%#m/%#d/%Y %#I:%M %p") + " " + p.subjectTimeZone
    
    #get user readable string of session date with timezone offset
    def getDateStringTZOffset(self):
        p = parameters.objects.first()
        return  self.date.astimezone(timezone(p.subjectTimeZone)).strftime("%#m/%#d/%Y %#I:%M %p %z")

    #get the local time of experiment start
    def getStartTimeString(self):
        p = parameters.objects.first()
        return  self.date.astimezone(timezone(p.subjectTimeZone)).strftime("%-I:%M %p")

    #get the local time of experiment end
    def getEndTimeString(self):
        p = parameters.objects.first()
        endTime = self.date + timedelta(minutes = self.length)
        return  endTime.astimezone(timezone(p.subjectTimeZone)).strftime("%-I:%M %p")    

    #hours until start
    def hoursUntilStart(self):
        #time remaining until start
        d_now = datetime.now(pytz.utc)
        timeRemaining = self.date - d_now

        return timeRemaining.total_seconds()/60/60
        #return str(timeRemaining)

    #get a list of session who's room and time overlap this one
    def getRoomOverlap(self):
        startTime = self.date
        endTime = self.date + timedelta(minutes = self.length)

        esd = main.models.experiment_session_days.objects.filter(location=self.location)\
                                                         .filter(date__lte=self.date_end)\
                                                         .filter(date_end__gte=self.date)\
                                                         .exclude(experiment_session__canceled = True)\
                                                         .exclude(id=self.id)
       

        return [i.json_min() for i in esd]

    #get user readable string of session lengths in mintues
    def getLengthString(self):
       
        return str(self.length) + " minutes"

    #send a reminder email to all subjects in session day
    def sendReminderEmail(self):

        self.reminderEmailSent=True
        self.save()

        logger = logging.getLogger(__name__)
        p = parameters.objects.first()
        logger.info("Send Reminder emails to: session " + str(self.experiment_session) + ", session day " + str(self.id))
        
        subjectText =  p.reminderTextSubject
        messageText = self.experiment_session.getReminderEmail()

        users_list = self.experiment_session_day_users_set.filter(confirmed = True).select_related("user")

        logger.info(users_list)
        emailList = []
        
        for i in users_list:
            emailList.append({"email":i.user.email,"first_name":i.user.first_name})        

        logger.info(emailList)

        mailResult = main.views.staff.sendMassEmail(emailList,subjectText, messageText)
        logger.info(mailResult)

    #get small json object
    def json_min(self):
        confirmedCount = self.experiment_session_day_users_set.filter(confirmed=True).count()
        totalCount = self.experiment_session_day_users_set.count()               
                       

        return{
            "id":self.id,
            "date":self.date,
            "name":self.experiment_session.experiment.title,
            "session_id":self.experiment_session.id,
            "confirmedCount": confirmedCount,
            "totalCount": totalCount,
        }

    #info to send to session run page
    def json_runInfo(self):       

        return{
            "id":self.id,
            "location":self.location.json(),
            "date":self.getDateString(),
            "date_raw":self.date,
            "length":self.length,
            "experiment_session_days_user" : self.json_runInfoUserList(),            
            "defaultShowUpFee": f'{self.experiment_session.experiment.showUpFee:.2f}',
            "complete":self.complete,
            "confirmedCount": self.experiment_session_day_users_set.filter(confirmed=True).count(),
            "attendingCount" : self.experiment_session_day_users_set.filter(attended=True).count(),
            "requiredCount" : self.experiment_session.recruitment_params.actual_participants,
            "bumpCount" : self.experiment_session_day_users_set.filter(bumped=True).count(),
        }
    
    #json info for run session
    def json_runInfoUserList(self):
        u_list_c = self.experiment_session_day_users_set.\
                       filter(confirmed=True).\
                       order_by(Lower('user__last_name'),Lower('user__first_name'))
        
        return [i.json_runInfo() for i in u_list_c]

    #json object of model
    def json(self,getUnconfirmed):

        logger = logging.getLogger(__name__)
        logger.info("Experiment Session Days JSON")
        logger.info("Get un-confirmed: " + str(getUnconfirmed))

        u_list_c = self.experiment_session_day_users_set.\
                       filter(confirmed=True).\
                       select_related('user').\
                       order_by(Lower('user__last_name'),Lower('user__first_name'))

        u_list_u = self.experiment_session_day_users_set.\
                       filter(confirmed=False).\
                       select_related('user').\
                       order_by(Lower('user__last_name'),Lower('user__first_name'))      

        u_list_u_json =[]

        if getUnconfirmed:  

            #get list of valid users        
            u_list_u2_json = [{"id" : i.user.id} for i in u_list_u]                   

            user_list_valid_clean=[]
            if u_list_u2_json != []:
                # user_list_valid = self.experiment_session.getValidUserList(u_list_u2_json,False,0,0,[],False) 

                # #check that attending will violate other experiments already attending
                # for u in user_list_valid:
                #     if not u.profile.check_for_future_constraints(self.experiment_session):
                #         user_list_valid_clean.append(u)
                user_list_valid_clean = self.experiment_session.getValidUserList_forward_check(u_list_u2_json,False,0,0,[],False)

            logger.info("Valid List")
            logger.info(user_list_valid_clean)       

            u_list_u_json = [{"id":i.id,            
                "confirmed":i.bumped,
                "user":{"id" : i.user.id,
                        "first_name":i.user.first_name.capitalize(),   
                        "last_name":i.user.last_name.capitalize(),},  
                "allowDelete" : i.allowDelete(),
                "allowConfirm" : i.allowConfirm(),
                "alreadyAttending":i.getAlreadyAttended(),
                "valid" :  0}
                    for i in u_list_u]

            #mark users that do not violate recruitment parameters
            for u in u_list_u_json:
                for uv in user_list_valid_clean:
                    if u['user']['id'] == uv.id:
                        u['valid'] = 1
                        break

        return{
            "id":self.id,
            "location":self.location.id,
            "date":self.getDateString(),
            "date_raw":self.date,
            "length":self.length,
            "account":self.account.id,
            "auto_reminder":self.auto_reminder,
            "experiment_session_days_user" : [{"id":i.id,            
                                                "confirmed":i.bumped,
                                                "user":{"id" : i.user.id,
                                                        "first_name":i.user.first_name.capitalize(),   
                                                        "last_name":i.user.last_name.capitalize(),},  
                                                "allowDelete" : i.allowDelete(),
                                                "alreadyAttending":i.getAlreadyAttended(),
                                                "allowConfirm" : i.allowConfirm(),}
                                                    for i in u_list_c],

            "experiment_session_days_user_unconfirmed" : u_list_u_json,
            "confirmedCount": len(u_list_c),
            "unConfirmedCount": len(u_list_u),  
            "roomOverlap":self.getRoomOverlap(),
            "allowDelete":self.allowDelete(),   
            "complete":self.complete,  
        }
        