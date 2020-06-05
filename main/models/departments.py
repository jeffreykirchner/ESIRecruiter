from django.db import models
import logging
import traceback

#ESI,ASBE, etc
class departments(models.Model):
    name = models.CharField(max_length = 300)
    charge_account= models.CharField(max_length = 100)
    petty_cash = models.IntegerField()

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    def json(self):
        return{
            "id":self.id,
            "name":self.name,
        }