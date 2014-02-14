from django.contrib.gis import admin
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from sesar_mobile.models import UserProfile

admin.site.register(UserProfile)