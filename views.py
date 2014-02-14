# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, FormView, RedirectView

import json
from lxml import etree
import requests
from random import randint
import geojson

from sesar_mobile import models

class IndexView(TemplateView):
    template_name = 'sesar_mobile/index.bootstrap.html'


class RecordIngestView(View):
    def __init__(self, *args, **kwargs):
        super(RecordIngestView, self).__init__(*args, **kwargs)
        self.data = {}

    def dispatch(self, *args, **kwargs):
        return super(RecordIngestView, self).dispatch(*args, **kwargs)

    def field_or_comment(self, request, sample, field, validator=lambda x: True, blank=False):
        if field in request.POST and (request.POST[field] != '' or blank):
            if not validator(request.POST[field]):
                raise ValidationError("Validation failed for {field}: {value}".format(field=field, value=request.POST[field]))

            elt = etree.SubElement(sample, field)
            elt.text = request.POST[field]
            self.data[field] = request.POST[field]
        else:
            sample.append(etree.Comment("<{field}></{field}>".format(field=field)))


    def field_or_fail(self, request, sample, field, validator=lambda x: True, blank=False):
        value = request.POST.get(field, '').strip()

        if not blank and value == '':
            raise ValidationError('Validation failed because {field} wasnt in the data'.format(field=field))
        if not validator(value):
            raise ValidationError("Validation failed for {field}: {value}".format(field=field, value=value))
        else:
            elt = etree.SubElement(sample, field)
            elt.text = value
            self.data[field] = value
            return elt

    def var_fields(self, request, sample, field, validator=lambda x: True):
        if field in request.POST:
            elts = []
            for value in request.POST.getlist(field):
                if not validator(value):
                    raise ValidationError("Validation failed for {field}: {value}".format(field=field, value=request.POST[field]))
                else:
                    elt = etree.SubElement(sample, field)
                    elt.text = value
                    elts.append(elt)
            return elts

    def field_or_default(self, request, sample, field, validator=lambda x: True, default=None):
        if field in request.POST and request.POST[field] != '':
            if not validator(request.POST[field]):
                raise ValidationError("Validation failed for {field}: {value}".format(field=field, value=request.POST[field]))

            elt = etree.SubElement(sample, field)
            elt.text = request.POST[field]
            self.data[field] = elt.text
        else:
            elt = etree.SubElement(sample, field)
            elt.text = default
            self.data[field] = elt.text
        return elt

    def post(self, request, *args, **kwargs):
        sample = etree.Element('sample')

        try:
            self.field_or_fail(request, sample, "sample_type")
            self.field_or_default(request, sample, "igsn", default='')
            self.field_or_fail(request, sample, "user_code")
            self.field_or_fail(request, sample, "name")
            self.field_or_comment(request, sample, "sample_other_name")
            self.field_or_comment(request, sample, "parent_igsn")
            self.field_or_comment(request, sample, "parent_sample_type")
            self.field_or_comment(request, sample, "parent_name")
            self.field_or_fail(request, sample, "is_private")
            self.field_or_comment(request, sample, "publish_date")
            self.field_or_fail(request, sample, "material")
            self.field_or_comment(request, sample, "classification")
            self.field_or_fail(request, sample, "field_name", blank=True)
            self.field_or_fail(request, sample, "description", blank=True)
            self.field_or_comment(request, sample, "age_min")
            self.field_or_comment(request, sample, "age_max")
            self.field_or_comment(request, sample, "age_unit")
            self.field_or_comment(request, sample, "geological_age")
            self.field_or_comment(request, sample, "geological_unit")
            self.field_or_comment(request, sample, "collection_method")
            self.field_or_comment(request, sample, "collection_method_descr")
            self.field_or_comment(request, sample, "size")
            self.field_or_comment(request, sample, "size_unit")
            self.field_or_comment(request, sample, "sample_comment")
            self.field_or_comment(request, sample, "latitude")
            self.field_or_comment(request, sample, "longitude")
            self.field_or_comment(request, sample, "latitude_end")
            self.field_or_comment(request, sample, "longitude_end")
            self.field_or_comment(request, sample, "elevation")
            self.field_or_comment(request, sample, "elevation_end")
            self.field_or_comment(request, sample, "primary_location_type")
            self.field_or_comment(request, sample, "primary_location_name")
            self.field_or_comment(request, sample, "location_description")
            self.field_or_comment(request, sample, "locality")
            self.field_or_comment(request, sample, "locality_description")
            self.field_or_comment(request, sample, "country")
            self.field_or_comment(request, sample, "province")
            self.field_or_comment(request, sample, "county")
            self.field_or_comment(request, sample, "city")
            self.field_or_comment(request, sample, "cruise_field_prgm")
            self.field_or_comment(request, sample, "platform_type")
            self.field_or_comment(request, sample, "platform_name")
            self.field_or_comment(request, sample, "platform_descr")
            self.field_or_comment(request, sample, "collector")
            self.field_or_comment(request, sample, "collector_detail")
            self.field_or_comment(request, sample, "current_archive")
            self.field_or_comment(request, sample, "current_archive_contact")
            self.field_or_comment(request, sample, "original_archive")
            self.field_or_comment(request, sample, "original_archive_contact")
            self.field_or_comment(request, sample, "depth_min")
            self.field_or_comment(request, sample, "depth_max")
            self.field_or_comment(request, sample, "depth_scale")
            self.var_fields(request, sample, "other_names")
            self.var_fields(request, sample, "urls")
        except ValidationError as e:
            return HttpResponseBadRequest(json.dumps([str(e).split("'")[1]]))

        xml = etree.tostring(sample, xml_declaration=True, pretty_print=True)
        with open('/opt/django/last_registered.xml', 'w') as out:
           out.write(xml)
   
        result = requests.post("http://sesar3.geoinfogeochem.org/webservices/uploadservice.php", data={
            "username" : request.POST.get('geopass_user', "jefferson.r.heard@gmail.com"),
            "password" : request.POST.get('geopass_password', "renci42"),
            "content" : xml
        })
         
        return HttpResponse(result.text, status = result.status_code)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RecordIngestView, self).dispatch(*args, **kwargs)

class RegistrationView(TemplateView):
    template_name = 'sesar_mobile/register.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        geopass_username = request.POST['username']
        geopass_password = request.POST['password']
        geopass_usercode = request.POST['geopass_user_code']
        user = User.objects.create_user(username, email=geopass_username, password=password)
        models.UserProfile.objects.create(user=user, geopass_password=geopass_password, geopass_username=geopass_username, geopass_usercode=geopass_usercode)
        user = authenticate(username = username, password=password)
        login(request, user)
        return HttpResponseRedirect('/sesar_mobile/index/')

class LoginView(TemplateView):
    template_name = 'sesar_mobile/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect("/sesar_mobile/index/")
        else:
            return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/sesar_mobile/index/')
        else:
            return self.get(request, *args, **kwargs)

class LogoutView(RedirectView):
    url = '/sesar_mobile/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


