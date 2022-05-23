'''
admin site
'''

from datetime import datetime, timedelta

import pytz
import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ngettext
from django.contrib import messages
from django.conf import settings
from django.db.models import Q,F,Value as V,Count
from django.contrib.auth.hashers import make_password
from django.db.models.functions import Lower
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from main.models import *

from main.globals import send_mass_email_verify
from main.globals import todays_date

from main.forms import parametersForm
from main.forms import faqForm
from main.forms import helpDocForm
from main.forms import frontPageNoticeForm
from main.forms import InvitationEmailTemplateForm


admin.site.register(accounts)
admin.site.register(departments)
admin.site.register(genders)
admin.site.register(institutions)
admin.site.register(majors)
admin.site.register(schools)
admin.site.register(email_filters)
admin.site.register(subject_types)
admin.site.register(ConsentForm)


admin.site.site_header = settings.ADMIN_SITE_HEADER

class helpDocAdmin(admin.ModelAdmin):
            
      form = helpDocForm

      ordering = [Lower('title')]

      actions = []
      list_display = ['title','path']

admin.site.register(help_docs,helpDocAdmin)

class frontPageNoticeAdmin(admin.ModelAdmin):
            
      form = frontPageNoticeForm

      ordering = [Lower('subject_text')]

      actions = []
      list_display = ['subject_text','enabled']

admin.site.register(Front_page_notice,frontPageNoticeAdmin)

class invitationEmailTemplateAdmin(admin.ModelAdmin):
            
      form = InvitationEmailTemplateForm

      ordering = [Lower('name')]

      actions = []
      list_display = ['name','enabled']

admin.site.register(Invitation_email_templates,invitationEmailTemplateAdmin)

class faqAdmin(admin.ModelAdmin):
            
      form = faqForm

      actions = []
      list_display = ['__str__','active']

admin.site.register(faq,faqAdmin)

class parametersadmin(admin.ModelAdmin):
      def has_add_permission(self, request, obj=None):
            return False
      
      def has_delete_permission(self, request, obj=None):
            return False
      
      form = parametersForm

      actions = []

admin.site.register(parameters, parametersadmin)

@admin.register(Traits)
class traitsAdmin(admin.ModelAdmin):
      ordering = [Lower('name')]

@admin.register(profile_trait)
class profile_traitAdmin(admin.ModelAdmin):
      ordering = [Lower('my_profile__user__last_name'),Lower('my_profile__user__first_name'),Lower('trait__name')]
      fields = ['value']

      search_fields = ['my_profile__user__first_name','my_profile__user__last_name','my_profile__studentID']


#instruction set page
class ProfileConsentFormInline(admin.TabularInline):
      '''
      profile consent form inline
      '''
      def has_add_permission(self, request, obj=None):
        return False

      def has_change_permission(self, request, obj=None):
        return False

      extra = 0  
      model = ProfileConsentForm
      can_delete = True

class UserAdmin(DjangoUserAdmin):

      ordering = ['-date_joined']
      search_fields = ['last_name', 'first_name', 'email']
      list_display = ['last_name', 'first_name', 'email', 'date_joined', 'last_login']
      actions = []
      list_filter = ['profile__type', 'is_superuser']

class NoLoginIn400Days(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('no login in last N days')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'user__last_login'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('400', _('400 days')),
            ('300', _('300 days')),
            ('200', _('200 days')),
            ('100', _('100 days')),
        )

    def queryset(self, request, queryset):
      """
      Returns the filtered queryset based on the value
      provided in the query string and retrievable via
      `self.value()`.
      """

      if self.value() == '400':
            today_minus_400 =  todays_date() - timedelta(days=400)

            return queryset.filter(
                  user__last_login__lte=today_minus_400,
            )

      if self.value() == '300':
            today_minus_300 =  todays_date() - timedelta(days=300)

            return queryset.filter(
                  user__last_login__lte=today_minus_300,
            )
      
      if self.value() == '200':
            today_minus_200 =  todays_date() - timedelta(days=200)

            return queryset.filter(
                  user__last_login__lte=today_minus_200,
            )
      
      if self.value() == '100':
            today_minus_100 =  todays_date() - timedelta(days=100)

            return queryset.filter(
                  user__last_login__lte=today_minus_100,
            )
        
@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
      
      def activate_all(self, request, queryset):

            user_list = User.objects.filter(profile__in = queryset).exclude(is_staff = True)
            updated_users = user_list.update(is_active = True)

            self.message_user(request, ngettext(
                  '%d user was activated.',
                  '%d users were activated.',
                  updated_users,
            ) % updated_users, messages.SUCCESS)
      activate_all.short_description = "Activate selected subjects"

      def pause_all(self, request, queryset):

            profile_list = queryset.exclude(user__is_staff=True) 

            #queryset_active_profile = list(queryset.filter(user__is_active=True).exclude(user__is_staff=True).select_related('user'))
            profile_list.update(paused=True)

            #updated3 = send_mass_email_verify(profile_list, request)         

            self.message_user(request, ngettext(
                  '%d user was paused.',
                  '%d users were paused.',
                  len(profile_list),
            ) % len(profile_list), messages.SUCCESS)

            #self.message_user(request, "Emails Sent: " + str(updated3['mail_count']) + " " + updated3['error_message'], messages.SUCCESS)

      pause_all.short_description = "Paused selected accounts"

      #clear everyone from blackballs status
      def clear_blackBalls(self, request, queryset):

            updated = queryset.exclude(user__is_staff = True).update(blackballed=0)

            self.message_user(request, ngettext(
                  '%d user was updated.',
                  '%d users were updated.',
                  updated,
            ) % updated, messages.SUCCESS)
      clear_blackBalls.short_description = "Remove blackballs"

      #confirm all active user's emails
      def confirm_active_email(self, request, queryset):

            updated = queryset.filter(user__is_active = True).update(email_confirmed="yes")

            self.message_user(request, ngettext(
                  '%d user was updated.',
                  '%d users were updated.',
                  updated,
            ) % updated, messages.SUCCESS)
      confirm_active_email.short_description = "Manually confirm selected active user's emails"

      #un confirm all selected email address
      def un_confirm_emails(self, request, queryset):

            updated = queryset.exclude(user__is_staff = True).update(email_confirmed='no')

            self.message_user(request, ngettext(
                  '%d user was updated.',
                  '%d users were updated.',
                  updated,
            ) % updated, messages.SUCCESS)
      un_confirm_emails.short_description = "Un-confirm selected email addresses"

      #apply email filter to profile
      def apply_email_filter(self,request,queryset):

            c = 0
            for p in queryset:
                  c +=  p.setup_email_filter()
            
            self.message_user(request, ngettext(
                  '%d user was updated.',
                  '%d users were updated.',
                  c,
            ) % c, messages.SUCCESS)
      apply_email_filter.short_description = "Apply email filters to selected profiles" 

      #activate users who were attended within last two years
      def activate_recent_users(self, request, queryset):
            logger = logging.getLogger(__name__)
            logger.info("activate_recent_users")

            d_now_minus_two_years = datetime.now(pytz.utc) - timedelta(days=730)

            qs = experiment_session_day_users.objects.filter(Q(attended = True) | Q(bumped = True))\
                                             .filter(experiment_session_day__date__gte = d_now_minus_two_years)\
                                             .values_list("user__id",flat=True)

            logger.info("Number of users found: " + str(len(qs)))

            q_list = queryset.filter(user__id__in = qs)
            updated = User.objects.filter(profile__in = q_list).update(is_active = True)

            self.message_user(request, ngettext(
                  '%d user was updated.',
                  '%d users were updated.',
                  updated,
            ) % updated, messages.SUCCESS)
      activate_recent_users.short_description = "Activate users who attended in past two years"   

      #set selected users up to be test subejects
      def setup_test_users(self, request, queryset):
            logger = logging.getLogger(__name__)
            logger.info("setup_test_users")

            updated = queryset.exclude(user__is_staff = True).update(blackballed=False,
                                                                     email_confirmed='yes',
                                                                     paused=False)
            
            pw =  make_password("esi2008esi")
            for p in queryset.exclude(user__is_staff = True):
                  p.user.password = pw
                  p.user.is_active=True
                  p.user.save()
                 
            self.message_user(request, ngettext(
                  '%d user was updated.',
                  '%d users were updated.',
                  updated,
            ) % updated, messages.SUCCESS)
      setup_test_users.short_description = "Setup users as test subjects, pw = 'esi2008esi'."

      ordering = ['user__last_name','user__first_name']
      search_fields = ['user__last_name','user__first_name','studentID','user__email']
      actions = [clear_blackBalls, confirm_active_email, un_confirm_emails, apply_email_filter,
                 pause_all, activate_all, activate_recent_users]

      if settings.DEBUG:
            actions.append(setup_test_users)

      list_display = ['__str__', 'paused', 'email_filter', 'updated', 'last_login']
      list_filter = ('blackballed', 'email_filter', 'paused', 'user__last_login', 'type', NoLoginIn400Days)
      readonly_fields = ['user', 'password_reset_key']
      inlines = [ProfileConsentFormInline,]

      def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields['type'].widget.can_change_related = False
        form.base_fields['type'].widget.can_add_related = False

        form.base_fields['school'].widget.can_change_related = False
        form.base_fields['school'].widget.can_add_related = False

        form.base_fields['major'].widget.can_change_related = False
        form.base_fields['major'].widget.can_add_related = False

        form.base_fields['gender'].widget.can_change_related = False
        form.base_fields['gender'].widget.can_add_related = False

        form.base_fields['subject_type'].widget.can_change_related = False
        form.base_fields['subject_type'].widget.can_add_related = False

        form.base_fields['email_filter'].widget.can_change_related = False
        form.base_fields['email_filter'].widget.can_add_related = False

        return form

class DailyEmailReportAdmin(admin.ModelAdmin):
      def has_add_permission(self, request, obj=None):
            return False

      readonly_fields=('text',)

      ordering = ['-date']
admin.site.register(DailyEmailReport, DailyEmailReportAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)