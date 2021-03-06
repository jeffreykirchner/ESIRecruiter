from django import forms
from main.models import Traits
from django.db.models.functions import Lower

import logging

#form
class traitReportForm(forms.Form):
    traits = forms.ModelMultipleChoiceField(label="",
                                                queryset=Traits.objects.all().order_by(Lower("name")),
                                                widget = forms.CheckboxSelectMultiple(attrs={}))


    